#!/usr/bin/env python3
"""swap_lipsync_clips.py — Higgsfield lip-sync stage 3: wire synced clips in.

Given the produced lip-sync clips (their job_ids/urls), NON-DESTRUCTIVELY:
  1. back up data/edl.csv  -> data/edl_pre_lipsync_backup.csv  (once, before any edit)
  2. add a synced *variant* row per in-scope perf key to data/clips.csv
     (clip_key `<PERF_key>_synced`, same source_still, the produced job_id + mp4_url)
  3. repoint every in-scope PERF_hook / PERF_lookup / PERF_window cut in
     data/edl.csv to its `_synced` variant (in_point/duration/section/note kept)

It touches ONLY the in-scope performance cuts; every memory/atmosphere/out-of-scope
cut is left exactly as-is. Deterministic + idempotent: re-running from the same
produced input does not double-append variants and yields byte-identical CSVs.
preflight_edl.py must still report RESULT PASS with 0 critical afterward (the
synced variants carry real http mp4_urls, so no cut is dropped).

This tool spends ZERO credits and makes ZERO network calls; it only rewrites CSVs.

Input JSON (--produced): {"produced": [
    {"target_perf_key": "PERF_hook", "job_id": "...", "mp4_url": "https://..."},
    ... one per in-scope key you generated ...
]}

Usage
-----
  python3 scripts/swap_lipsync_clips.py --produced produced.json
  python3 scripts/swap_lipsync_clips.py --produced produced.json --dry-run   # report only
"""
import sys, os, json, csv, argparse, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EDL     = os.path.join(ROOT, "data", "edl.csv")
EDL_BAK = os.path.join(ROOT, "data", "edl_pre_lipsync_backup.csv")
CLIPS   = os.path.join(ROOT, "data", "clips.csv")

# in-scope perf keys eligible for a synced variant (must match slice_vocals.py)
IN_SCOPE_KEYS = ("PERF_hook", "PERF_lookup", "PERF_window")
SYNC_SUFFIX = "_synced"

EDL_FIELDS   = ["index", "clip_key", "in_point", "duration", "section", "note"]
CLIPS_FIELDS = ["clip_key", "job_id", "source_still", "section", "mp4_url", "motion"]


def _read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _write(path, fields, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def load_produced(path):
    data = json.load(open(path))
    out = {}
    for p in data.get("produced", []):
        key = p["target_perf_key"]
        if key not in IN_SCOPE_KEYS:
            raise SystemExit(f"produced entry targets out-of-scope key {key!r}")
        url = (p.get("mp4_url") or "").strip()
        if not url.startswith("http"):
            raise SystemExit(f"produced {key}: mp4_url must be http(s) ('{url[:40]}')")
        out[key] = {"job_id": p.get("job_id", ""), "mp4_url": url}
    if not out:
        raise SystemExit("no produced lip-sync clips in --produced input")
    return out


def swap(produced, dry_run=False):
    """Perform (or, if dry_run, only report) the non-destructive swap."""
    clips = _read(CLIPS)
    clip_by_key = {c["clip_key"]: c for c in clips}

    # build the synced variant rows (idempotent: skip keys already present)
    new_clip_rows = []
    for key, info in sorted(produced.items()):
        synced_key = key + SYNC_SUFFIX
        base = clip_by_key.get(key)
        if base is None:
            raise SystemExit(f"in-scope key {key!r} not found in clips.csv")
        if synced_key in clip_by_key:
            continue                      # already added on a prior run — no double-append
        new_clip_rows.append({
            "clip_key": synced_key,
            "job_id": info["job_id"],
            "source_still": base.get("source_still", ""),
            "section": base.get("section", ""),
            "mp4_url": info["mp4_url"],
            "motion": (base.get("motion", "") + " [lip-synced]").strip(),
        })

    # repoint in-scope EDL cuts to their synced variant
    edl = _read(EDL)
    repointed, repoint_ids = 0, []
    new_edl = []
    for r in edl:
        r = dict(r)
        if r["clip_key"] in IN_SCOPE_KEYS and (r["clip_key"] in produced):
            r["clip_key"] = r["clip_key"] + SYNC_SUFFIX
            repointed += 1
            repoint_ids.append(r["index"])
        new_edl.append(r)

    report = {
        "produced_keys": sorted(produced),
        "synced_variants_added": [c["clip_key"] for c in new_clip_rows],
        "edl_cuts_repointed": repointed,
        "edl_cut_indices": repoint_ids,
        "dry_run": dry_run,
    }
    if dry_run:
        return report

    # --- mutate on disk, back up FIRST ---
    if not os.path.exists(EDL_BAK):
        shutil.copyfile(EDL, EDL_BAK)     # back up the pre-swap edl once
    _write(CLIPS, CLIPS_FIELDS, clips + new_clip_rows)
    _write(EDL, EDL_FIELDS, new_edl)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="wire produced lip-sync clips into clips.csv + edl.csv (non-destructive)")
    ap.add_argument("--produced", required=True, metavar="JSON",
                    help='JSON {"produced":[{target_perf_key,job_id,mp4_url},...]}')
    ap.add_argument("--dry-run", action="store_true",
                    help="report the swap without writing any file")
    args = ap.parse_args(argv)

    produced = load_produced(args.produced)
    rep = swap(produced, dry_run=args.dry_run)
    print(json.dumps(rep, indent=2))
    if not args.dry_run:
        print(f"backup: {os.path.relpath(EDL_BAK, ROOT)}  "
              f"(exists={os.path.isfile(EDL_BAK)})")
        print("run `python3 scripts/preflight_edl.py` to confirm RESULT PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
