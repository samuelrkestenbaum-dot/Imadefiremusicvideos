#!/usr/bin/env python3
"""Insert band-coverage cuts C25-C34 into the EDL and re-balance PRE2 / CH1.

Packet P-007. Deterministic, self-asserting, idempotent.

What it does:
  1. If data/edl_pre_bandcoverage_backup.csv is absent, copy the CURRENT
     data/edl.csv to it. Then read the BACKUP as the source-of-truth EDL
     (so re-runs are idempotent and never compound).
  2. Insert each new cut immediately AFTER its slot_after_row existing cut
     (the row's `index` in the source EDL).
  3. Re-time, Option (a): within PRE2 and CH1 ONLY, keep each section's span
     FIXED. New cuts take their target_dur; existing cuts scale by
     factor = (span - sum(new target_dur)) / sum(existing original dur),
     rounded to 2 dp; the LAST cut of each section absorbs the residual so the
     section sum is EXACT.
  4. All other sections are byte-unchanged (raw lines preserved; only the
     leading index column is renumbered). Re-number index 1..86 contiguously.
  5. Write data/edl.csv; append 10 rows to clips.csv and stills.csv.
  6. Self-test (exit non-zero on any breach) and print PRE2/CH1 before/after.

NOTE on CSV handling: the source EDL contains unquoted commas in some `note`
fields (e.g. row 21 "reflection again, gone"). To guarantee byte-fidelity of
non-rebalanced rows, this script treats each EDL line as
`index,clip_key,in_point,duration,section,note` where the first five fields are
comma-free and `note` is the verbatim remainder of the line. It never round-
trips rows through csv.writer, so quoting/commas are preserved exactly.

Touches ONLY: edl.csv, clips.csv, stills.csv, edl_pre_bandcoverage_backup.csv.
"""
from __future__ import annotations

import csv
import os
import shutil
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

EDL = os.path.join(DATA, "edl.csv")
EDL_BACKUP = os.path.join(DATA, "edl_pre_bandcoverage_backup.csv")
CLIPS = os.path.join(DATA, "clips.csv")
STILLS = os.path.join(DATA, "stills.csv")

EDL_HEADER = "index,clip_key,in_point,duration,section,note"

# Asset map (P-006 output). Embedded so the script is self-contained and does
# not depend on a path outside the repo. Mirrors p006_assets.json.
ASSETS = [
    {"clip_key": "C25", "section": "PRE2", "still_id": "76c55142-0b83-4fe2-a6d9-9a116968cf8c",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041425_76c55142-0b83-4fe2-a6d9-9a116968cf8c.png",
     "job_id": "ca67e772-7825-4793-950b-2864a50b18c4",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041631_ca67e772-7825-4793-950b-2864a50b18c4.mp4",
     "slot_after_row": 51, "target_dur": 3.4,
     "prompt_summary": "Storm-lit drummer hands and sticks building a tom fill; blue-grey key light; film grain",
     "motion": "drummer hands accelerate a tom fill, sticks blur, lightning flickers"},
    {"clip_key": "C26", "section": "PRE2", "still_id": "3c48a26d-0c83-4fb4-9529-c23a82de1aca",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041427_3c48a26d-0c83-4fb4-9529-c23a82de1aca.png",
     "job_id": "34402db4-ac1d-45d6-8f03-5679ad13f191",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041633_34402db4-ac1d-45d6-8f03-5679ad13f191.mp4",
     "slot_after_row": 52, "target_dur": 3.4,
     "prompt_summary": "Slow push-in toward full band in a storm-lit room, rising build; 35mm cinematic",
     "motion": "slow dolly push-in toward the band leaning into the build"},
    {"clip_key": "C27", "section": "PRE2", "still_id": "a685bc64-58e3-41ca-a2b0-a8f7ac0b7778",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041430_a685bc64-58e3-41ca-a2b0-a8f7ac0b7778.png",
     "job_id": "1dfdd7cc-ea3d-4d1b-bf39-636f81e7f1e6",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041635_1dfdd7cc-ea3d-4d1b-bf39-636f81e7f1e6.mp4",
     "slot_after_row": 53, "target_dur": 3.4,
     "prompt_summary": "Side-lit profile of the male singer (short red-blonde hair, receding hairline, not bald) leaning into a vocal; storm light",
     "motion": "singer lifts chin and leans into a rising vocal in profile"},
    {"clip_key": "C28", "section": "PRE2", "still_id": "727357a7-6e1d-48f1-b916-12edf31e1b60",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041431_727357a7-6e1d-48f1-b916-12edf31e1b60.png",
     "job_id": "76997023-342c-495f-b765-16cce9fe8b3f",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041636_76997023-342c-495f-b765-16cce9fe8b3f.mp4",
     "slot_after_row": 54, "target_dur": 3.4,
     "prompt_summary": "Backlit bassist silhouette driving low strings in a storm-lit room; rim light",
     "motion": "bassist sways forward, hand driving low strings, rim light shifts"},
    {"clip_key": "C29", "section": "PRE2", "still_id": "589045f9-a971-4435-9a1f-cc06df021f1a",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041433_589045f9-a971-4435-9a1f-cc06df021f1a.png",
     "job_id": "dc84bdd5-c69d-4e06-93a4-cf2d684d7f3d",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041638_dc84bdd5-c69d-4e06-93a4-cf2d684d7f3d.mp4",
     "slot_after_row": 55, "target_dur": 3.4,
     "prompt_summary": "Hands driving hard chords on an electric piano under a lamp; lightning on the keys",
     "motion": "hands drive hard chords, lightning flash crosses the keys"},
    {"clip_key": "C30", "section": "PRE2", "still_id": "7bc97ef5-11cd-4f4d-bbd6-0909f675540e",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041434_7bc97ef5-11cd-4f4d-bbd6-0909f675540e.png",
     "job_id": "d5152734-b2ec-4209-8b62-839f7510214b",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041639_d5152734-b2ec-4209-8b62-839f7510214b.mp4",
     "slot_after_row": 56, "target_dur": 3.4,
     "prompt_summary": "Wide of the full band rising at the peak of a storm-build; arms and instruments lifting",
     "motion": "whole band rises together at the peak, arms and instruments lifting"},
    {"clip_key": "C31", "section": "CH1", "still_id": "2c9eb497-7028-4b87-bf0f-cd96699349cf",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041435_2c9eb497-7028-4b87-bf0f-cd96699349cf.png",
     "job_id": "833e7ed9-943c-4ec1-a365-223b3a58737c",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041640_833e7ed9-943c-4ec1-a365-223b3a58737c.mp4",
     "slot_after_row": 29, "target_dur": 3.2,
     "prompt_summary": "Drummer hard CU, backbeat hit, cymbal shimmer; warm wood-panelled room",
     "motion": "drummer strikes the backbeat hard, cymbal shimmers"},
    {"clip_key": "C32", "section": "CH1", "still_id": "150210b6-f284-4e16-9f13-fd1c28840eb9",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041437_150210b6-f284-4e16-9f13-fd1c28840eb9.png",
     "job_id": "06390892-c1c8-4b89-b395-2a5e478281dd",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041642_06390892-c1c8-4b89-b395-2a5e478281dd.mp4",
     "slot_after_row": 31, "target_dur": 3.2,
     "prompt_summary": "Guitar hands on the fretboard mid-strum; warm room; chorus rhythm",
     "motion": "hands strum and move along the fretboard, chorus rhythm"},
    {"clip_key": "C33", "section": "CH1", "still_id": "ef844001-cd00-41a3-af52-d4985fb328eb",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041440_ef844001-cd00-41a3-af52-d4985fb328eb.png",
     "job_id": "b23de5fd-fa07-49cf-9cd6-c18fa5272cc0",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041644_b23de5fd-fa07-49cf-9cd6-c18fa5272cc0.mp4",
     "slot_after_row": 33, "target_dur": 3.2,
     "prompt_summary": "Straight-to-lens CU of the male singer (short red-blonde hair, receding hairline, not bald) singing the chorus; warm key light",
     "motion": "singer sings the chorus with force into the mic, slight push-in"},
    {"clip_key": "C34", "section": "CH1", "still_id": "4e032f83-aae9-4d4c-ad2a-e565b34267c1",
     "still_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041441_4e032f83-aae9-4d4c-ad2a-e565b34267c1.png",
     "job_id": "5c2cdeaa-debd-4262-8f0e-c46f9de2eb32",
     "mp4_url": "https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR/hf_20260630_041645_5c2cdeaa-debd-4262-8f0e-c46f9de2eb32.mp4",
     "slot_after_row": 35, "target_dur": 3.2,
     "prompt_summary": "Hands on an electric piano under a warm lamp, lifting into the chorus",
     "motion": "hands lift into the chorus on the keys under warm lamp"},
]

# Re-balanced sections and their FIXED spans.
SECTION_SPAN = {"PRE2": 41.00, "CH1": 38.75}
SECTION_NEW_DUR = {"PRE2": 3.4, "CH1": 3.2}

# The 12 confirmed section start times (cumulative), in order.
CONFIRMED_STARTS = [
    ("INTRO", 0.0), ("V1", 18.0), ("V2", 41.25), ("PRE1", 69.75),
    ("CH1", 89.25), ("V3", 128.0), ("V4", 144.5), ("PRE2", 173.0),
    ("CH2", 214.0), ("BRIDGE", 238.0), ("FINAL", 261.0),
]
TOTAL_RUNTIME = 274.0
EXPECTED_CUTS = 86

# Confirmed re-balanced sequences (clip_key, duration) for verification.
EXPECTED_PRE2 = [
    ("C17", 4.12), ("C25", 3.4), ("C18", 3.30), ("C26", 3.4), ("C12", 3.30),
    ("C27", 3.4), ("C02", 3.30), ("C28", 3.4), ("C17", 3.30), ("C29", 3.4),
    ("C20", 3.30), ("C30", 3.38),
]
EXPECTED_CH1 = [
    ("C12", 4.15), ("C10", 3.11), ("C31", 3.2), ("C19", 3.11), ("C11", 3.11),
    ("C32", 3.2), ("C12", 3.11), ("C02", 3.11), ("C33", 3.2), ("C10", 3.11),
    ("C12", 3.11), ("C34", 3.23),
]

EPS = 1e-6


def read_edl_raw(path):
    """Read the EDL preserving each data row's raw text.

    Returns (header_line, list_of_row_dicts) where each dict has:
      index (int), clip_key, in_point, duration (float), section,
      note_raw (verbatim remainder, includes any quoting/commas),
      raw (the full original line WITHOUT trailing newline).
    Only the first five comma-separated fields are parsed; `note` is the
    remainder so unquoted commas in notes are preserved verbatim.
    """
    with open(path, "r", newline="") as f:
        lines = f.read().split("\n")
    # Drop a single trailing empty element from a final newline, if present.
    if lines and lines[-1] == "":
        lines = lines[:-1]
    header = lines[0]
    rows = []
    for ln in lines[1:]:
        parts = ln.split(",", 5)
        idx, key, inp, dur, sec = parts[0], parts[1], parts[2], parts[3], parts[4]
        note_raw = parts[5] if len(parts) > 5 else ""
        rows.append({
            "index": int(idx),
            "clip_key": key,
            "in_point": inp,
            "duration": float(dur),
            "section": sec,
            "note_raw": note_raw,
            "raw": ln,
        })
    return header, rows


def fmt_dur(d):
    """Format a duration the way the existing EDL does: whole numbers as ints,
    otherwise the minimal decimal (strip trailing zeros), matching source rows
    such as '4', '3.1', '6.56', '4.65', '3.38'."""
    if abs(d - round(d)) < EPS:
        return str(int(round(d)))
    s = ("%.2f" % d).rstrip("0").rstrip(".")
    return s


def render_line(idx, key, in_point, dur, section, note_raw):
    return "%d,%s,%s,%s,%s,%s" % (idx, key, in_point, fmt_dur(dur), section, note_raw)


def build_edl(header, src_rows):
    """Return (header, list_of_output_dicts) with inserts + re-time applied.

    Each output dict has keys: clip_key, in_point, duration, section, note_raw,
    is_new, src_raw (the original raw line for non-new rows, else None).
    """
    # Map slot_after_row (source index) -> list of new asset rows to insert.
    inserts = {}
    for a in ASSETS:
        inserts.setdefault(a["slot_after_row"], []).append(a)

    merged = []
    for r in src_rows:
        merged.append({
            "clip_key": r["clip_key"],
            "in_point": r["in_point"],
            "duration": r["duration"],
            "section": r["section"],
            "note_raw": r["note_raw"],
            "is_new": False,
            "src_raw": r["raw"],
        })
        for a in inserts.get(r["index"], []):
            merged.append({
                "clip_key": a["clip_key"],
                "in_point": "0.0",
                "duration": float(a["target_dur"]),
                "section": a["section"],
                "note_raw": a["motion"],
                "is_new": True,
                "src_raw": None,
            })

    # Re-time PRE2 and CH1 only, keeping section span fixed.
    sec_positions = OrderedDict()
    for pos, item in enumerate(merged):
        sec_positions.setdefault(item["section"], []).append(pos)

    for section, span in SECTION_SPAN.items():
        positions = sec_positions[section]
        new_dur = SECTION_NEW_DUR[section]
        existing_sum = sum(merged[p]["duration"] for p in positions if not merged[p]["is_new"])
        n_new = sum(1 for p in positions if merged[p]["is_new"])
        factor = (span - n_new * new_dur) / existing_sum
        for p in positions:
            if merged[p]["is_new"]:
                merged[p]["duration"] = round(new_dur, 2)
            else:
                merged[p]["duration"] = round(merged[p]["duration"] * factor, 2)
        cur = sum(merged[p]["duration"] for p in positions)
        resid = round(span - cur, 2)
        last = positions[-1]
        merged[last]["duration"] = round(merged[last]["duration"] + resid, 2)

    return header, merged


def render_edl(header, merged):
    """Render output lines. Non-rebalanced rows keep their raw source line with
    only the leading index renumbered, guaranteeing byte-fidelity of the rest
    of the line. Rebalanced and new rows are formatted explicitly."""
    out = [header]
    for n, item in enumerate(merged, start=1):
        if item["section"] not in SECTION_SPAN and not item["is_new"]:
            # Byte-preserve everything after the index column.
            rest = item["src_raw"].split(",", 1)[1]
            out.append("%d,%s" % (n, rest))
        else:
            out.append(render_line(n, item["clip_key"], item["in_point"],
                                    item["duration"], item["section"],
                                    item["note_raw"]))
    return "\n".join(out) + "\n"


def read_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def append_registry():
    """Append the 10 new rows to clips.csv and stills.csv (idempotent)."""
    c_header, c_rows = read_csv(CLIPS)
    assert c_header == ["clip_key", "job_id", "source_still", "section", "mp4_url", "motion"], \
        "clips.csv header mismatch: %r" % (c_header,)
    existing_keys = {r[0] for r in c_rows}
    for a in ASSETS:
        if a["clip_key"] in existing_keys:
            continue
        c_rows.append([
            a["clip_key"], a["job_id"], a["still_id"][:8], "band",
            a["mp4_url"], a["motion"],
        ])
    write_csv(CLIPS, c_header, c_rows)

    s_header, s_rows = read_csv(STILLS)
    assert s_header == ["still_id", "url", "prompt_summary"], \
        "stills.csv header mismatch: %r" % (s_header,)
    existing_sids = {r[0] for r in s_rows}
    for a in ASSETS:
        if a["still_id"] in existing_sids:
            continue
        s_rows.append([a["still_id"], a["still_url"], a["prompt_summary"]])
    write_csv(STILLS, s_header, s_rows)


def self_test(header, src_rows, merged):
    errs = []

    # 1. Cut count.
    if len(merged) != EXPECTED_CUTS:
        errs.append("cut count %d != %d" % (len(merged), EXPECTED_CUTS))

    # Group merged rows by section in order.
    sec_rows = OrderedDict()
    for item in merged:
        sec_rows.setdefault(item["section"], []).append(item)

    # 2. PRE2 / CH1 span sums exact.
    for section, span in SECTION_SPAN.items():
        s = sum(it["duration"] for it in sec_rows[section])
        if abs(s - span) > EPS:
            errs.append("%s sum %.6f != %.2f" % (section, s, span))

    # 3. Total runtime.
    total = sum(it["duration"] for it in merged)
    if abs(total - TOTAL_RUNTIME) > EPS:
        errs.append("total %.6f != %.2f" % (total, TOTAL_RUNTIME))

    # 4. Cumulative section starts unchanged vs the 12 confirmed.
    cum = 0.0
    seen = OrderedDict()
    for it in merged:
        if it["section"] not in seen:
            seen[it["section"]] = cum
        cum += it["duration"]
    for name, expected in CONFIRMED_STARTS:
        got = seen.get(name)
        if got is None or abs(got - expected) > EPS:
            errs.append("section %s start %s != %.2f" % (name, got, expected))

    # 5. Every non-PRE2/CH1 row identical to the backup (raw line minus index).
    src_other = [r["raw"].split(",", 1)[1] for r in src_rows
                 if r["section"] not in SECTION_SPAN]
    new_other = [it["src_raw"].split(",", 1)[1] for it in merged
                 if it["section"] not in SECTION_SPAN and not it["is_new"]]
    if src_other != new_other:
        if len(src_other) != len(new_other):
            errs.append("non-rebalanced row count changed %d -> %d"
                        % (len(src_other), len(new_other)))
        else:
            for a, b in zip(src_other, new_other):
                if a != b:
                    errs.append("non-rebalanced row changed: %r -> %r" % (a, b))
                    break

    # 6. The 10 new clip_keys present exactly once each.
    keys = [it["clip_key"] for it in merged]
    for a in ASSETS:
        c = keys.count(a["clip_key"])
        if c != 1:
            errs.append("new clip_key %s appears %d times (want 1)"
                        % (a["clip_key"], c))

    # 7. Match the confirmed re-balanced sequences exactly.
    def seq(section):
        return [(it["clip_key"], round(it["duration"], 2)) for it in sec_rows[section]]
    if seq("PRE2") != [(k, round(d, 2)) for k, d in EXPECTED_PRE2]:
        errs.append("PRE2 sequence mismatch: %r" % (seq("PRE2"),))
    if seq("CH1") != [(k, round(d, 2)) for k, d in EXPECTED_CH1]:
        errs.append("CH1 sequence mismatch: %r" % (seq("CH1"),))

    return errs, seen


def print_before_after(src_rows, merged):
    for section in ("PRE2", "CH1"):
        before = [(r["clip_key"], r["duration"]) for r in src_rows if r["section"] == section]
        after = [(it["clip_key"], it["duration"]) for it in merged if it["section"] == section]
        print("\n=== %s before/after (span %.2f) ===" % (section, SECTION_SPAN[section]))
        print("  BEFORE (%d): %s  sum=%.2f"
              % (len(before), " ".join("%s=%.2f" % (k, d) for k, d in before),
                 sum(d for _, d in before)))
        print("  AFTER  (%d): %s  sum=%.2f"
              % (len(after), " ".join("%s=%.2f" % (k, d) for k, d in after),
                 sum(d for _, d in after)))


def main():
    # Step 1: ensure backup exists, then read backup as source of truth.
    if not os.path.exists(EDL_BACKUP):
        shutil.copyfile(EDL, EDL_BACKUP)
        print("Wrote backup: %s" % EDL_BACKUP)
    else:
        print("Backup already present (idempotent): %s" % EDL_BACKUP)

    header, src_rows = read_edl_raw(EDL_BACKUP)

    # Step 2-4: build re-timed EDL.
    header, merged = build_edl(header, src_rows)

    # Self-test BEFORE writing anything.
    errs, starts = self_test(header, src_rows, merged)

    print_before_after(src_rows, merged)

    print("\n=== section starts (after) ===")
    for name, st in starts.items():
        print("  %-8s %7.2f" % (name, st))

    if errs:
        print("\nSELF-TEST FAILED:")
        for e in errs:
            print("  - " + e)
        sys.exit(1)

    # Write outputs only after self-test passes.
    with open(EDL, "w", newline="") as f:
        f.write(render_edl(header, merged))
    append_registry()

    print("\nSELF-TEST PASSED: %d cuts, PRE2=%.2f, CH1=%.2f, total=%.2f"
          % (len(merged), SECTION_SPAN["PRE2"], SECTION_SPAN["CH1"], TOTAL_RUNTIME))
    print("Wrote: %s, %s, %s" % (EDL, CLIPS, STILLS))


if __name__ == "__main__":
    main()
