#!/usr/bin/env python3
"""Tests for beat_lock.py — the P-015 "done" definition.

Run: python3 scripts/test_beat_lock.py
Exits 0 on all-pass, 1 on any failure. No third-party test runner needed.

Covers:
  1. --analyze-only writes beats.json + beat_vs_cut.md, does NOT write the
     variant, and leaves data/edl.csv byte-identical.
  2. beats.json regenerates byte-identically (determinism / idempotence).
  3. The full run produces the variant; edl.csv still byte-identical.
  4. Variant constraints: 86 rows + header, all live section starts preserved,
     total 274.0 +/- 1.0, zero over-reads, every clip_key in clips.csv, no
     back-to-back identical clip_key adjacency, same schema/header as edl.csv.
  5. Variant regenerates byte-identically (determinism).
"""
import os, sys, csv, hashlib, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT   = os.path.join(HERE, "beat_lock.py")
BEATS    = os.path.join(ROOT, "analysis", "beats.json")
DIAG     = os.path.join(ROOT, "analysis", "beat_vs_cut.md")
EDL      = os.path.join(ROOT, "data", "edl.csv")
VARIANT  = os.path.join(ROOT, "data", "edl_beatlocked.csv")
CLIPS    = os.path.join(ROOT, "data", "clips.csv")

PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args],
                          cwd=ROOT, capture_output=True, text=True)


def section_starts(rows):
    t, seen, starts = 0.0, None, []
    for r in rows:
        if r["section"] != seen:
            starts.append(round(t, 6)); seen = r["section"]
        t += float(r["duration"])
    return starts


def main():
    edl_md5_before = md5(EDL)

    # tidy any prior variant so we can prove --analyze-only doesn't create it
    if os.path.exists(VARIANT):
        os.remove(VARIANT)

    # --- 1. analyze-only ---
    r = run("--analyze-only")
    check("analyze-only exits 0", r.returncode == 0, r.stderr)
    check("analyze-only wrote beats.json", os.path.isfile(BEATS))
    check("analyze-only wrote beat_vs_cut.md", os.path.isfile(DIAG))
    check("analyze-only did NOT write variant", not os.path.exists(VARIANT))
    check("edl.csv byte-identical after analyze-only", md5(EDL) == edl_md5_before)

    beats_md5_1 = md5(BEATS)

    # --- 2. beats.json determinism ---
    r = run("--analyze-only")
    check("analyze-only re-run exits 0", r.returncode == 0, r.stderr)
    check("beats.json byte-identical across runs", md5(BEATS) == beats_md5_1)

    # --- 3. full run writes variant, edl untouched ---
    r = run()
    check("full run exits 0", r.returncode == 0, r.stderr)
    check("full run wrote variant", os.path.isfile(VARIANT))
    check("edl.csv byte-identical after full run", md5(EDL) == edl_md5_before)
    variant_md5_1 = md5(VARIANT)

    # --- 4. variant constraints ---
    with open(VARIANT, newline="") as f:
        rd = csv.reader(f)
        header = next(rd)
        var_rows = list(rd)
    with open(EDL, newline="") as f:
        edl_header = next(csv.reader(f))
    check("variant header matches edl.csv schema", header == edl_header,
          f"{header} vs {edl_header}")
    check("variant has exactly 86 data rows", len(var_rows) == 86, str(len(var_rows)))

    with open(VARIANT, newline="") as f:
        vrows = list(csv.DictReader(f))
    with open(EDL, newline="") as f:
        lrows = list(csv.DictReader(f))
    clip_keys = {r["clip_key"] for r in csv.DictReader(open(CLIPS, newline=""))}

    live_starts, var_starts = section_starts(lrows), section_starts(vrows)
    check("all section starts preserved", live_starts == var_starts,
          f"live={live_starts} var={var_starts}")

    total = sum(float(r["duration"]) for r in vrows)
    check("total within 274.0 +/-1.0", abs(total - 274.0) <= 1.0, f"{total:.3f}")

    overreads = [r["index"] for r in vrows
                 if float(r["in_point"]) + float(r["duration"]) > 5.0 + 1e-6]
    check("zero over-reads (in_point+dur<=5.0)", not overreads, str(overreads))

    unresolved = [r["clip_key"] for r in vrows if r["clip_key"] not in clip_keys]
    check("every clip_key resolvable in clips.csv", not unresolved, str(unresolved))

    prev, repeats = None, []
    for r in vrows:
        if prev == r["clip_key"]:
            repeats.append(r["index"])
        prev = r["clip_key"]
    check("no back-to-back identical clip_key", not repeats, str(repeats))

    # --- 5. variant determinism ---
    r = run()
    check("full re-run exits 0", r.returncode == 0, r.stderr)
    check("variant byte-identical across runs", md5(VARIANT) == variant_md5_1)
    check("beats.json still byte-identical after full runs", md5(BEATS) == beats_md5_1)

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
