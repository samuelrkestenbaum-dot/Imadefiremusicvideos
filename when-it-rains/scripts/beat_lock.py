#!/usr/bin/env python3
"""beat_lock.py — beat-lock analysis + a gated, beat-aware EDL variant.

NON-DESTRUCTIVE to the live edit. This tool NEVER touches data/edl.csv,
clips.csv, stills.csv, assets.json, or any render/preflight script. It produces:

  analysis/beats.json        the derived beat/downbeat map (durable; committed so
                             it survives after the gitignored song.mp3 is gone)
  analysis/beat_vs_cut.md    a diagnostic of the LIVE data/edl.csv against the grid
  data/edl_beatlocked.csv    (variant path only) a beat-aware EDL variant with the
                             SAME schema as edl.csv

Method
------
The song's true beat is ~61.52 BPM (period 0.97524 s), established in
analysis/song.json. librosa's raw beat tracker locks onto the eighth/triplet
subdivision (~184.6 BPM = 3x), so instead of trusting its wobbly onset-following
beats we build a *uniform* grid at the known period and phase-lock it by
maximizing onset-envelope energy at the grid points. This yields a stable,
deterministic, snappable reference. librosa's raw beats are still computed and
kept as a corroboration cross-check. A pure-numpy onset-envelope fallback is
provided (guarded by the import) but is not needed when librosa is present.

Downbeats are the every-4th-beat subgrid (4/4 assumption). The phase (which of
the four beats is the "one") is chosen to best align with the EDL's section
starts, but the alignment is weak (see caveats in beats.json / beat_vs_cut.md):
downbeat phase is genuinely uncertain and the variant treats it as advisory only.

The variant snaps each cut BOUNDARY toward the nearest grid beat under hard
constraints: it preserves every section START time exactly, keeps the total
within 274.0 +/- 1.0 s, never lets in_point+duration exceed the 5.0 s source
length, keeps every clip_key resolvable in clips.csv, and never creates
back-to-back identical clip_key adjacency (a snap that would is skipped). The
snap is deliberately conservative.

Usage
-----
  python3 scripts/beat_lock.py --analyze-only          # map + diagnostic only
  python3 scripts/beat_lock.py                          # map + diagnostic + variant
  python3 scripts/beat_lock.py --edl data/edl.csv       # target a specific EDL
  python3 scripts/beat_lock.py --validate <edl.csv>     # constraint-check an EDL

Deterministic + idempotent: a re-run produces byte-identical beats.json and
edl_beatlocked.csv.
"""
import sys, os, json, csv, argparse, subprocess

import numpy as np

try:
    import librosa
    _HAVE_LIBROSA = True
except Exception:  # pragma: no cover - librosa is installed in this env
    _HAVE_LIBROSA = False

try:
    import imageio_ffmpeg
    _HAVE_FFMPEG = True
except Exception:  # pragma: no cover
    _HAVE_FFMPEG = False

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SONG      = os.path.join(ROOT, "song.mp3")
SONG_JSON = os.path.join(ROOT, "analysis", "song.json")
BEATS_JSON = os.path.join(ROOT, "analysis", "beats.json")
DIAG_MD    = os.path.join(ROOT, "analysis", "beat_vs_cut.md")
EDL_LIVE   = os.path.join(ROOT, "data", "edl.csv")
EDL_VARIANT = os.path.join(ROOT, "data", "edl_beatlocked.csv")
CLIPS      = os.path.join(ROOT, "data", "clips.csv")

SR = 22050
SRC_LEN = 5.0          # a cut may not read past the source length
TARGET  = 274.0        # master length target (4:34)
TOL     = 1.0          # +/- seconds allowed on the total

# Known-good tempo established in analysis/song.json. We deliberately anchor the
# grid to this rather than to librosa's octave-ambiguous estimate.
DEFAULT_BPM = 61.5234375
DEFAULT_MUSIC_END = 273.75


# --------------------------------------------------------------------------- #
# audio + grid
# --------------------------------------------------------------------------- #
def _decode(path):
    """Decode an mp3 to mono float32 PCM at SR via the bundled ffmpeg."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    raw = subprocess.run(
        [ff, "-v", "quiet", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        stdout=subprocess.PIPE,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def _numpy_onset_env(x):
    """Pure-numpy onset-strength envelope + its frame times (fallback path)."""
    hop = 512
    win = 1024
    nf = max(0, (len(x) - win) // hop)
    fe = np.array([np.sum(x[i * hop:i * hop + win] ** 2) for i in range(nf)])
    on = np.diff(fe, prepend=fe[:1])
    on[on < 0] = 0.0
    if on.max() > 0:
        on = on / on.max()
    times = np.arange(len(on)) * (hop / SR)
    return on, times


def _onset_env(x):
    """Onset-strength envelope + frame times; librosa when present, else numpy."""
    if _HAVE_LIBROSA:
        oenv = librosa.onset.onset_strength(y=x, sr=SR)
        times = librosa.times_like(oenv, sr=SR)
        return oenv, times
    return _numpy_onset_env(x)


def _phase_lock_grid(oenv, times, period, music_end, n_search=200):
    """Pick the phase in [0, period) whose uniform grid maximizes onset energy."""
    best_phi, best_score = 0.0, -1.0
    for i in range(n_search):
        phi = (i / n_search) * period
        grid = np.arange(phi, music_end, period)
        if len(grid) == 0:
            continue
        idx = np.clip(np.searchsorted(times, grid), 0, len(oenv) - 1)
        score = float(oenv[idx].sum())
        if score > best_score:
            best_score, best_phi = score, phi
    return best_phi, best_score


def _pick_downbeat_phase(beats, section_starts):
    """Choose which of the four beat phases best aligns with section starts."""
    best_k, best_err = 0, None
    for k in range(4):
        db = beats[k::4]
        if len(db) == 0:
            continue
        err = float(np.mean([np.min(np.abs(db - s)) for s in section_starts]))
        if best_err is None or err < best_err:
            best_err, best_k = err, k
    return best_k, best_err


def compute_beats():
    """Decode the song and derive the beat/downbeat map. Returns a dict."""
    if not _HAVE_FFMPEG:
        raise RuntimeError("imageio_ffmpeg unavailable; cannot decode song.mp3")
    if not os.path.isfile(SONG):
        raise FileNotFoundError(
            f"{SONG} not found (it is gitignored). beats.json is the durable map; "
            f"regenerate only with the audio present."
        )

    bpm, music_end = DEFAULT_BPM, DEFAULT_MUSIC_END
    if os.path.isfile(SONG_JSON):
        sj = json.load(open(SONG_JSON))
        bpm = float(sj.get("tempo_bpm", bpm))
        music_end = float(sj.get("music_end", music_end))

    x = _decode(SONG)
    source_duration_s = round(len(x) / SR, 6)
    period = 60.0 / bpm

    oenv, times = _onset_env(x)
    phi, _score = _phase_lock_grid(oenv, times, period, music_end)

    beats = np.arange(phi, music_end + period / 2.0, period)
    beats = beats[beats <= music_end + 1e-9]

    # librosa raw beats — corroboration cross-check (not used for snapping)
    method = "librosa_onset_phase_grid" if _HAVE_LIBROSA else "numpy_onset_phase_grid"
    corroboration = {}
    if _HAVE_LIBROSA:
        raw_tempo, raw_beats = librosa.beat.beat_track(
            y=x, sr=SR, units="time", trim=False
        )
        raw_tempo = float(np.atleast_1d(raw_tempo)[0])
        corroboration = {
            "librosa_raw_tempo_bpm": round(raw_tempo, 4),
            "librosa_raw_beat_count": int(len(raw_beats)),
            "librosa_first_beat_s": round(float(raw_beats[0]), 4) if len(raw_beats) else None,
            "note": ("librosa's raw tracker locks the ~3x subdivision "
                     "(~184.6 BPM); the committed grid uses the song.json "
                     "beat period and phase-locks it to onset energy."),
        }

    # downbeat phase from the live EDL section starts (advisory only)
    section_starts = _section_starts(_load_edl(EDL_LIVE)) if os.path.isfile(EDL_LIVE) else []
    if section_starts:
        db_k, db_err = _pick_downbeat_phase(beats, np.array(section_starts))
    else:
        db_k, db_err = 0, None
    downbeats = beats[db_k::4]

    return {
        "method": method,
        "tempo_bpm": round(bpm, 7),
        "beat_period_s": round(period, 7),
        "phase_reference_note": (
            f"uniform grid, period {period:.6f}s, phase {phi:.4f}s chosen by "
            f"maximizing onset-strength energy at grid points over [0,period); "
            f"grid spans [phase, music_end={music_end}]."
        ),
        "source_duration_s": source_duration_s,
        "music_end_s": round(music_end, 4),
        "beat_count": int(len(beats)),
        "downbeat_count": int(len(downbeats)),
        "downbeat_phase_index": int(db_k),
        "downbeat_phase_confidence": (
            "low — mean section-start-to-downbeat error "
            f"{db_err * 1000:.0f}ms; treat downbeat 'one' as advisory, not exact"
            if db_err is not None else "unknown — no EDL available"
        ),
        "beat_times": [round(float(b), 6) for b in beats],
        "downbeat_times": [round(float(d), 6) for d in downbeats],
        "corroboration": corroboration,
    }


# --------------------------------------------------------------------------- #
# EDL helpers
# --------------------------------------------------------------------------- #
EDL_FIELDS = ["index", "clip_key", "in_point", "duration", "section", "note"]


def _load_edl(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _section_starts(rows):
    """Cumulative start time of each section, in EDL order (first occurrence)."""
    t = 0.0
    seen = None
    starts = []
    for r in rows:
        if r["section"] != seen:
            starts.append(t)
            seen = r["section"]
        t += float(r["duration"])
    return starts


def _load_beats(path=BEATS_JSON):
    d = json.load(open(path))
    return np.array(d["beat_times"], dtype=float)


def _fmt_num(v):
    """Format a number the way edl.csv does: integers stay integer-like."""
    f = float(v)
    if abs(f - round(f)) < 1e-9:
        return str(int(round(f)))
    return f"{f:.2f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------- #
# variant generation
# --------------------------------------------------------------------------- #
def build_variant(beats):
    """Produce the beat-aware EDL variant rows under all hard constraints.

    Strategy (conservative): keep every cut's clip_key, in_point, section and
    note unchanged. Adjust ONLY durations so that cut boundaries land closer to
    grid beats, while (a) preserving each section's START time exactly, (b)
    never letting in_point+duration exceed SRC_LEN, and (c) keeping the total
    within TARGET +/- TOL. Because in_point is untouched, every clip_key stays
    resolvable and no new adjacency is introduced (the sequence order and keys
    are identical to the live EDL), so the no-repeat constraint holds by
    construction.
    """
    live = _load_edl(EDL_LIVE)

    # All arithmetic is done in INTEGER MILLISECONDS so section starts and the
    # grand total are preserved *exactly* (no float drift). Live durations are
    # multiples of 10 ms, so this is lossless for the live values.
    def ms(x):
        return int(round(float(x) * 1000.0))

    # Boundaries live on a 10 ms grid (the live EDL uses 0.01 s durations), so
    # 2-decimal formatting is lossless and per-section duration sums are exact.
    GRID_MS = 10

    def q10(v_ms):
        return int(round(v_ms / GRID_MS)) * GRID_MS

    beats_ms = np.array([q10(ms(b)) for b in beats])
    SRC_MS = ms(SRC_LEN)
    MIN_CUT_MS = 500                     # keep every cut >= 0.5 s

    def nearest_beat_ms(x_ms):
        j = int(np.argmin(np.abs(beats_ms - x_ms)))
        return int(beats_ms[j])

    # Group cuts by section, in EDL order, capturing each section's exact live
    # START and END (in ms). Only INTERIOR boundaries of a section move; the
    # start and end are pinned to live values, so every section start and the
    # grand total are preserved by construction.
    sections = []            # (section, [row,...], start_ms, end_ms)
    start_ms = 0
    i = 0
    n = len(live)
    while i < n:
        sec = live[i]["section"]
        group = []
        seg_start = start_ms
        while i < n and live[i]["section"] == sec:
            group.append(live[i])
            start_ms += ms(live[i]["duration"])
            i += 1
        sections.append((sec, group, seg_start, start_ms))

    out = []
    for sec, group, seg_start, seg_end in sections:
        m = len(group)
        # live cumulative boundaries within the section (interior cut ends), ms
        live_ends = []
        c = seg_start
        for r in group:
            c += ms(r["duration"])
            live_ends.append(c)

        # snap each interior boundary toward a grid beat, clamped to keep every
        # cut >= MIN_CUT, leave room for later cuts, and never over-read source.
        bounds = [seg_start]
        for j in range(m - 1):
            ip_ms = ms(group[j]["in_point"])
            raw_end = live_ends[j]
            snapped = nearest_beat_ms(raw_end)
            lo = bounds[-1] + MIN_CUT_MS
            hi = seg_end - MIN_CUT_MS * (m - 1 - j)
            over_read_cap = bounds[-1] + (SRC_MS - ip_ms)   # in_point+dur <= SRC
            hi = min(hi, over_read_cap)
            if lo > hi:                       # no legal room -> keep live boundary
                snapped = raw_end
            elif snapped < lo or snapped > hi:
                snapped = min(max(raw_end, lo), hi)
            bounds.append(int(snapped))
        bounds.append(seg_end)                # pinned section END (exact)

        # Ensure the LAST cut (its duration = seg_end - bounds[m-1]) is safe. If
        # not, pull bounds[m-1] back to the live boundary (known-safe) rather than
        # ever moving the pinned section end.
        last_ip = ms(group[-1]["in_point"])
        if m > 1:
            last_dur = seg_end - bounds[m - 1]
            if last_dur < MIN_CUT_MS or last_ip + last_dur > SRC_MS:
                bounds[m - 1] = seg_end - ms(group[-1]["duration"])
                if bounds[m - 1] < bounds[m - 2] + MIN_CUT_MS:
                    bounds[m - 1] = bounds[m - 2] + ms(group[-1]["duration"])

        for j, r in enumerate(group):
            ip_ms = ms(r["in_point"])
            dur_ms = bounds[j + 1] - bounds[j]
            # interior safety net (last cut already guaranteed above)
            if j < m - 1 and (dur_ms < MIN_CUT_MS or ip_ms + dur_ms > SRC_MS):
                dur_ms = ms(r["duration"])
                bounds[j + 1] = bounds[j] + dur_ms
            out.append({
                "index": str(len(out) + 1),
                "clip_key": r["clip_key"],
                "in_point": _fmt_num(ip_ms / 1000.0),
                "duration": _fmt_num(dur_ms / 1000.0),
                "section": sec,
                "note": r["note"],
            })

    return out


def write_edl(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EDL_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# --------------------------------------------------------------------------- #
# diagnostic
# --------------------------------------------------------------------------- #
def write_diagnostic(beats, edl_path=EDL_LIVE):
    rows = _load_edl(edl_path)
    lines = []
    lines.append("# Beat-vs-cut diagnostic")
    lines.append("")
    lines.append(f"- Source EDL: `{os.path.relpath(edl_path, ROOT)}`")
    lines.append(f"- Beat grid: `analysis/beats.json` ({len(beats)} beats, "
                 f"period {60.0/DEFAULT_BPM:.5f}s @ {DEFAULT_BPM} BPM)")
    lines.append("- Offset = (cut boundary time) - (nearest beat time); "
                 "positive = cut lands *after* the beat.")
    lines.append("")
    lines.append("| # | clip | section | cut end (s) | nearest beat (s) | offset (ms) |")
    lines.append("|---|------|---------|-------------|------------------|-------------|")

    t = 0.0
    offs = []
    for r in rows:
        t += float(r["duration"])
        j = int(np.argmin(np.abs(beats - t)))
        nb = float(beats[j])
        off = (t - nb) * 1000.0
        offs.append(off)
        lines.append(
            f"| {r['index']} | {r['clip_key']} | {r['section']} | "
            f"{t:.3f} | {nb:.3f} | {off:+.0f} |"
        )

    offs = np.array(offs)
    ab = np.abs(offs)
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Cuts analyzed: **{len(offs)}**")
    lines.append(f"- Mean |offset|: **{ab.mean():.1f} ms**")
    lines.append(f"- Median |offset|: **{np.median(ab):.1f} ms**")
    lines.append(f"- Max |offset|: **{ab.max():.1f} ms**")
    lines.append(f"- Cuts within +/-50 ms: **{int((ab <= 50).sum())} / {len(ab)}** "
                 f"({100 * (ab <= 50).mean():.1f}%)")
    lines.append(f"- Cuts within +/-100 ms: **{int((ab <= 100).sum())} / {len(ab)}** "
                 f"({100 * (ab <= 100).mean():.1f}%)")
    lines.append("")
    lines.append("## Reading this")
    lines.append("")
    lines.append(
        "The live edit was cut to section energy, not to the beat grid, so most "
        "boundaries sit well off the nearest beat (see the low within-50ms count). "
        "That is the motivation for the gated `data/edl_beatlocked.csv` variant. "
        "The variant snap is conservative: it preserves every section start, never "
        "over-reads the 5.0s source, and holds the 274.0s total, so it can only "
        "pull boundaries *within a section* toward beats — it does not re-cut the "
        "film. Downbeat phase is low-confidence (see `beats.json`), so the variant "
        "snaps to beats, not to the 'one'."
    )
    lines.append("")
    with open(DIAG_MD, "w") as f:
        f.write("\n".join(lines) + "\n")
    return offs


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #
def validate_edl(path):
    """Constraint-check an EDL (used for the variant; preflight_edl.py untouched)."""
    rows = _load_edl(path)
    # load clips.csv keys
    with open(CLIPS, newline="") as f:
        clip_keys = {r["clip_key"] for r in csv.DictReader(f)}

    live = _load_edl(EDL_LIVE)
    live_starts = _section_starts(live)
    var_starts = _section_starts(rows)

    problems = []
    total = 0.0
    overreads = 0
    unresolved = 0
    repeats = 0
    prev_key = None
    for r in rows:
        ip, dur = float(r["in_point"]), float(r["duration"])
        total += dur
        if ip + dur > SRC_LEN + 1e-6:
            overreads += 1
            problems.append(f"cut {r['index']} ({r['clip_key']}): "
                            f"in_point+dur = {ip + dur:.3f} > {SRC_LEN}")
        if r["clip_key"] not in clip_keys:
            unresolved += 1
            problems.append(f"cut {r['index']}: clip_key {r['clip_key']} "
                            f"not in clips.csv")
        if prev_key is not None and r["clip_key"] == prev_key:
            repeats += 1
            problems.append(f"cut {r['index']}: back-to-back identical "
                            f"clip_key {r['clip_key']}")
        prev_key = r["clip_key"]

    starts_ok = (len(live_starts) == len(var_starts) and
                 all(abs(a - b) < 1e-6 for a, b in zip(live_starts, var_starts)))
    if not starts_ok:
        problems.append(f"section starts differ: live={['%.3f' % s for s in live_starts]} "
                        f"variant={['%.3f' % s for s in var_starts]}")
    total_ok = abs(total - TARGET) <= TOL
    if not total_ok:
        problems.append(f"total {total:.3f}s off target {TARGET} by {total - TARGET:+.3f}")

    report = {
        "rows": len(rows),
        "total_s": round(total, 4),
        "total_ok": total_ok,
        "section_starts_preserved": starts_ok,
        "overreads": overreads,
        "unresolved_clip_keys": unresolved,
        "back_to_back_repeats": repeats,
        "section_starts": [round(s, 4) for s in var_starts],
        "problems": problems,
        "ok": not problems,
    }
    return report


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description="beat-lock analysis + gated variant")
    ap.add_argument("--analyze-only", action="store_true",
                    help="write beats.json + diagnostic only; DO NOT write the variant")
    ap.add_argument("--edl", default=EDL_LIVE,
                    help="EDL to run the diagnostic against (default: live edl.csv)")
    ap.add_argument("--validate", metavar="PATH",
                    help="constraint-check the given EDL and exit")
    args = ap.parse_args(argv)

    if args.validate:
        rep = validate_edl(args.validate)
        print(json.dumps(rep, indent=2))
        return 0 if rep["ok"] else 1

    # 1) derive + persist the beat map
    beat_map = compute_beats()
    with open(BEATS_JSON, "w") as f:
        json.dump(beat_map, f, indent=2)
        f.write("\n")
    beats = np.array(beat_map["beat_times"], dtype=float)
    print(f"wrote {os.path.relpath(BEATS_JSON, ROOT)}  "
          f"({beat_map['beat_count']} beats, {beat_map['downbeat_count']} downbeats, "
          f"method={beat_map['method']})")

    # 2) diagnostic over the chosen EDL
    offs = write_diagnostic(beats, args.edl)
    ab = np.abs(offs)
    print(f"wrote {os.path.relpath(DIAG_MD, ROOT)}  "
          f"(mean|off| {ab.mean():.1f}ms, within50 {int((ab <= 50).sum())}/{len(ab)})")

    # 3) variant (gated)
    if args.analyze_only:
        print("--analyze-only: variant NOT written.")
        return 0

    rows = build_variant(beats)
    write_edl(rows, EDL_VARIANT)
    rep = validate_edl(EDL_VARIANT)
    print(f"wrote {os.path.relpath(EDL_VARIANT, ROOT)}  "
          f"({rep['rows']} rows, total {rep['total_s']}s, "
          f"starts_ok={rep['section_starts_preserved']}, "
          f"overreads={rep['overreads']}, unresolved={rep['unresolved_clip_keys']}, "
          f"repeats={rep['back_to_back_repeats']})")
    if not rep["ok"]:
        print("VARIANT CONSTRAINT FAILURE:")
        for p in rep["problems"]:
            print("  x", p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
