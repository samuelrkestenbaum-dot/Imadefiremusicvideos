#!/usr/bin/env python3
"""preflight_edl.py — prove the edit is render-ready from the CSVs alone (no network).

Catches the failures that would otherwise only show up mid-render (or silently, as a
short/wrong master) when you run scripts/render_master.sh on a connected machine:

  CRITICAL (exit 1):
    - an EDL cut whose clip_key has no row in clips.csv          -> fetch/assemble drops
      the cut, master ends up short and mis-timed
    - a clips.csv row with an empty / non-http mp4_url           -> fetch can't download it
  WARN (exit 0, but printed):
    - a cut whose in_point + duration exceeds SRC_LEN (5.0s)     -> ffmpeg over-reads the
      source; the segment freezes/truncates
    - a clips.csv source_still not found in stills.csv           -> catalog drift
    - EDL total duration off the 274s (4:34) target

Run: python3 scripts/preflight_edl.py     (from the project root or anywhere)
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EDL    = os.path.join(ROOT, "data", "edl.csv")
CLIPS  = os.path.join(ROOT, "data", "clips.csv")
STILLS = os.path.join(ROOT, "data", "stills.csv")

SRC_LEN = 5.0      # kling3_0 std clips render at 5s; a cut may not read past that
TARGET  = 274.0    # master length (4:34), must match assemble_rough_cut.sh / render_master.sh
TOL     = 1.0      # +/- seconds allowed on the total before we warn

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def main():
    for p in (EDL, CLIPS, STILLS):
        if not os.path.isfile(p):
            print(f"CRITICAL: missing {p}"); return 1

    edl, clips, stills = load(EDL), load(CLIPS), load(STILLS)
    clip_by_key = {r["clip_key"]: r for r in clips}
    still_prefixes = {r["still_id"][:8] for r in stills}
    full_still_ids = {r["still_id"] for r in stills}

    crit, warn = [], []

    # --- CRITICAL: every EDL cut resolves to a clip row with a real URL ---
    total = 0.0
    for r in edl:
        idx, key = r["index"], r["clip_key"]
        try:
            ip, dur = float(r["in_point"]), float(r["duration"])
        except ValueError:
            crit.append(f"cut {idx} ({key}): non-numeric in_point/duration"); continue
        total += dur
        row = clip_by_key.get(key)
        if row is None:
            crit.append(f"cut {idx}: clip_key '{key}' has NO row in clips.csv (cut would be dropped)")
            continue
        url = (row.get("mp4_url") or "").strip()
        if not url.startswith("http"):
            crit.append(f"cut {idx} ({key}): clips.csv mp4_url is empty/invalid ('{url[:30]}')")
        if ip + dur > SRC_LEN + 1e-6:
            warn.append(f"cut {idx} ({key}): in_point {ip}+dur {dur} = {ip+dur:.2f}s > {SRC_LEN}s source (over-read)")

    # --- CRITICAL: no clips.csv row has an unusable URL (even if unused by EDL) ---
    for r in clips:
        url = (r.get("mp4_url") or "").strip()
        if not url.startswith("http"):
            warn.append(f"clips.csv '{r['clip_key']}': mp4_url empty/invalid (unused by EDL, but catalog issue)")

    # --- WARN: clips.csv source_still resolves into stills.csv catalog ---
    for r in clips:
        ss = (r.get("source_still") or "").strip()
        if ss and ss not in still_prefixes and ss not in full_still_ids:
            warn.append(f"clips.csv '{r['clip_key']}': source_still '{ss}' not found in stills.csv")

    # --- WARN: total duration vs target ---
    if abs(total - TARGET) > TOL:
        warn.append(f"EDL total {total:.2f}s is off target {TARGET}s by {total-TARGET:+.2f}s")

    # --- report ---
    print("=" * 60)
    print("preflight_edl — render-readiness check")
    print("=" * 60)
    print(f"EDL cuts        : {len(edl)}")
    print(f"clips catalog   : {len(clips)}")
    print(f"stills catalog  : {len(stills)}")
    print(f"EDL total       : {total:.2f}s (target {TARGET}s = 4:34)")
    print(f"distinct clips used by EDL: {len({r['clip_key'] for r in edl})}")
    print("-" * 60)
    if crit:
        print(f"CRITICAL ({len(crit)}):")
        for m in crit: print(f"  x {m}")
    if warn:
        print(f"WARN ({len(warn)}):")
        for m in warn: print(f"  ! {m}")
    if not crit and not warn:
        print("all checks passed — edit is render-ready.")
    print("=" * 60)

    if crit:
        print("RESULT: FAIL (critical issues would break the render)"); return 1
    print("RESULT: PASS" + (" (with warnings)" if warn else "")); return 0

if __name__ == "__main__":
    sys.exit(main())
