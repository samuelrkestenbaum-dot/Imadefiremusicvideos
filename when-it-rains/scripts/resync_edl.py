#!/usr/bin/env python3
"""resync_edl.py — deterministic, re-runnable EDL section-sync.

WHAT THIS IS (and is NOT)
-------------------------
This is a SECTION-SYNC, *not* a sub-beat quantization. It rescales each cut's
``duration`` so that every section spans the user-CONFIRMED section times, and
so the back-to-back concat resolves on the 274s mix end. It does NOT snap cuts
to the 0.97524s beat grid (61.5234375 BPM): true beat-snapping needs a rigorous
downbeat phase reference (a confirmed first-downbeat offset) that we do not have
here, so per-cut sub-beat quantization would be guesswork. We therefore change
ONLY the ``duration`` column.

  * clips (``clip_key``), seek offsets (``in_point``), ``section`` labels and
    ``note`` text are left UNTOUCHED, byte-for-byte.
  * ``data/edl_original_backup.csv`` is the SOURCE OF TRUTH. On first run we copy
    the current ``data/edl.csv`` to it (only if it does not already exist); every
    run reads the BACKUP, never the (possibly already-synced) ``edl.csv``. That
    makes this transform idempotent: re-running reproduces the same output and
    never re-derives from already-synced data, and never overwrites the backup.

THE MODEL
---------
``data/edl.csv`` columns: index,clip_key,in_point,duration,section,note.
It is a back-to-back concat — a section's start time on the timeline is the
cumulative sum of all prior cuts' ``duration``. ``in_point`` is a seek-into-
source offset, NOT a timeline position, so it is left alone.

Per section we compute OLD span = sum of that section's cuts' original
durations (computed from the data, never hardcoded), and NEW span = the gap to
the next confirmed section start. Each cut's duration is scaled by
new_span/old_span, rounded to 2 decimals, and the LAST cut of each section
absorbs the rounding residual so the section sums EXACTLY to its target span
(no float drift in the cumulative section starts).
"""

import csv
import io
import os
import shutil
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
EDL = os.path.join(DATA, "edl.csv")
BACKUP = os.path.join(DATA, "edl_original_backup.csv")

# Confirmed section START times, in seconds (from the user's confirm of
# SECTION_TIMES.md). END=274 closes FINAL; FINAL's span (274-261=13) folds in
# the ~2s trim so the 276s back-to-back EDL resolves on the 274s mix end.
CONFIRMED_STARTS = OrderedDict([
    ("INTRO", 0.0),
    ("V1", 18.0),
    ("V2", 41.25),
    ("PRE1", 69.75),
    ("CH1", 89.25),
    ("V3", 128.0),
    ("V4", 144.5),
    ("PRE2", 173.0),
    ("CH2", 214.0),
    ("BRIDGE", 238.0),
    ("FINAL", 261.0),
    ("END", 274.0),
])

# OLD spans we EXPECT to compute from the backup (asserted, not used as input).
EXPECTED_OLD_SPANS = OrderedDict([
    ("INTRO", 18.0), ("V1", 30.0), ("V2", 30.0), ("PRE1", 25.0),
    ("CH1", 25.0), ("V3", 31.0), ("V4", 30.0), ("PRE2", 25.0),
    ("CH2", 24.0), ("BRIDGE", 23.0), ("FINAL", 15.0),
])

TOL = 1e-6


def target_spans():
    """new span per section = next confirmed start - this confirmed start."""
    keys = list(CONFIRMED_STARTS.keys())
    spans = OrderedDict()
    for i in range(len(keys) - 1):  # last key is END (closes FINAL)
        spans[keys[i]] = CONFIRMED_STARTS[keys[i + 1]] - CONFIRMED_STARTS[keys[i]]
    return spans


def read_backup_lines():
    """Return (header_line, [raw_data_line, ...]) from the backup, verbatim."""
    with open(BACKUP, newline="") as fh:
        raw = fh.read()
    lines = raw.split("\n")
    header = lines[0]
    data = [ln for ln in lines[1:] if ln != ""]
    return header, data


def parse_line(line):
    """Split a raw data line into (index, clip_key, in_point, duration, rest).

    ``rest`` is the verbatim ``section,note`` tail (preserving original quoting).
    Columns index/clip_key/in_point/duration never contain commas or quotes, so
    splitting on the first 4 commas is exact and loss-free.
    """
    parts = line.split(",", 4)
    if len(parts) != 5:
        raise ValueError("malformed EDL row: %r" % line)
    idx, clip_key, in_point, duration, rest = parts
    section = rest.split(",", 1)[0]
    return idx, clip_key, in_point, duration, section, rest


def build_groups(data_lines):
    """Group raw lines by section IN FILE ORDER. Returns OrderedDict[sec]->[rows].

    Each row is the parse_line tuple plus its 0-based position in the file.
    """
    groups = OrderedDict()
    for pos, line in enumerate(data_lines):
        idx, clip_key, in_point, duration, section, rest = parse_line(line)
        groups.setdefault(section, []).append(
            (pos, idx, clip_key, in_point, float(duration), section, rest)
        )
    return groups


def resync():
    # 1. Ensure backup exists (byte-for-byte copy of current edl.csv), then
    #    always read the backup as source of truth.
    if not os.path.exists(BACKUP):
        shutil.copyfile(EDL, BACKUP)
        print("created backup: %s" % os.path.relpath(BACKUP, HERE))
    else:
        print("backup already present (not overwritten): %s"
              % os.path.relpath(BACKUP, HERE))

    header, data_lines = read_backup_lines()
    assert len(data_lines) == 76, "expected 76 cuts, got %d" % len(data_lines)

    groups = build_groups(data_lines)
    new_spans = target_spans()

    # 3. Compute OLD spans from the data and assert they match expectations.
    old_spans = OrderedDict(
        (sec, sum(r[4] for r in rows)) for sec, rows in groups.items()
    )
    assert list(old_spans.keys()) == list(EXPECTED_OLD_SPANS.keys()), (
        "section order changed: %s vs %s"
        % (list(old_spans.keys()), list(EXPECTED_OLD_SPANS.keys())))
    for sec, exp in EXPECTED_OLD_SPANS.items():
        assert abs(old_spans[sec] - exp) < TOL, (
            "old span mismatch for %s: %r != %r" % (sec, old_spans[sec], exp))

    # 4. Scale each cut's duration; last cut of each section absorbs residual.
    new_dur_by_pos = {}
    table = []  # (sec, old_span, new_span, scale, new_sum)
    for sec, rows in groups.items():
        old_span = old_spans[sec]
        new_span = new_spans[sec]
        scale = new_span / old_span
        scaled = [round(r[4] * scale, 2) for r in rows]
        # residual so the section sums EXACTLY to its target span
        residual = round(new_span - sum(scaled), 2)
        scaled[-1] = round(scaled[-1] + residual, 2)
        for r, nd in zip(rows, scaled):
            new_dur_by_pos[r[0]] = nd
        table.append((sec, old_span, new_span, scale, sum(scaled)))

    # 5 & 6. Re-emit lines: change ONLY the duration token; everything else
    #        verbatim from the backup row.
    out_lines = [header]
    for pos, line in enumerate(data_lines):
        idx, clip_key, in_point, _dur, _sec, rest = parse_line(line)
        nd = new_dur_by_pos[pos]
        # format duration without trailing-zero noise but keep it numeric/plain
        dur_str = ("%g" % nd)
        out_lines.append(",".join([idx, clip_key, in_point, dur_str, rest]))
    out_text = "\n".join(out_lines) + "\n"

    with open(EDL, "w", newline="") as fh:
        fh.write(out_text)

    # ---- Self-test (exit non-zero on any failure) --------------------------
    self_test(header, data_lines, out_text, new_spans)

    # ---- Report ------------------------------------------------------------
    print()
    print("section   old->new span   scale     new sum")
    print("-" * 48)
    for sec, old_s, new_s, scale, new_sum in table:
        print("%-8s  %5.2f -> %6.2f  x%6.4f  %7.2f"
              % (sec, old_s, new_s, scale, new_sum))
    print()
    print("cumulative section starts (s):")
    cum = 0.0
    for sec, _o, new_s, _sc, _ns in table:
        print("  %-8s start %8.3f  (confirmed %8.3f)"
              % (sec, cum, CONFIRMED_STARTS[sec]))
        cum += new_s
    print("  %-8s start %8.3f  (confirmed %8.3f)  TOTAL"
          % ("END", cum, CONFIRMED_STARTS["END"]))
    print()
    print("OK: 76 cuts, section starts == confirmed, total == 274.000")


def self_test(header, backup_data_lines, out_text, new_spans):
    out_lines = out_text.split("\n")
    out_lines = [ln for ln in out_lines if ln != ""]
    out_header, out_data = out_lines[0], out_lines[1:]

    # (a) exactly 76 cuts, row order unchanged
    assert out_header == header, "header changed"
    assert len(out_data) == 76, "expected 76 output cuts, got %d" % len(out_data)

    # (e) every non-duration field byte-identical to backup, row-for-row
    for i, (b_line, o_line) in enumerate(zip(backup_data_lines, out_data)):
        b = parse_line(b_line)
        o = parse_line(o_line)
        # index, clip_key, in_point, section, rest(section,note) verbatim
        assert b[0] == o[0], "index changed at row %d" % i      # index
        assert b[1] == o[1], "clip_key changed at row %d" % i   # clip_key
        assert b[2] == o[2], "in_point changed at row %d" % i   # in_point
        assert b[5] == o[5], "section,note changed at row %d" % i  # rest

    # rebuild per-section sums and cumulative starts from the OUTPUT
    cum = 0.0
    starts = OrderedDict()
    sec_sum = OrderedDict()
    cur_sec = None
    for o_line in out_data:
        _idx, _ck, _ip, dur, section, _rest = parse_line(o_line)
        if section != cur_sec:
            starts[section] = cum
            cur_sec = section
        sec_sum.setdefault(section, 0.0)
        sec_sum[section] += float(dur)
        cum += float(dur)

    # (b) each section's new durations sum to its target span
    for sec, span in new_spans.items():
        assert abs(sec_sum[sec] - span) < TOL, (
            "section %s sum %r != target %r" % (sec, sec_sum[sec], span))

    # (c) cumulative section starts == confirmed starts
    for sec, start in starts.items():
        assert abs(start - CONFIRMED_STARTS[sec]) < TOL, (
            "section %s start %r != confirmed %r"
            % (sec, start, CONFIRMED_STARTS[sec]))

    # (d) total == 274
    assert abs(cum - CONFIRMED_STARTS["END"]) < TOL, (
        "total %r != 274" % cum)


if __name__ == "__main__":
    try:
        resync()
    except AssertionError as exc:
        sys.stderr.write("SELF-TEST FAILED: %s\n" % exc)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("ERROR: %s\n" % exc)
        sys.exit(1)
