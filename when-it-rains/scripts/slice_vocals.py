#!/usr/bin/env python3
"""slice_vocals.py — Higgsfield-native lip-sync stage 1: line-map + vocal slices.

CODE ONLY. This tool spends ZERO credits, makes ZERO network calls, and never
calls Higgsfield. It prepares the *inputs* for an audio-driven lip-sync
(Higgsfield wan2_7) that a later, explicitly-gated step runs.

What it produces
----------------
  analysis/line_map.json          DURABLE, committed. The deterministic lyric
                                  line-map {line_id, section, start_s, end_s,
                                  lyric, target_perf_key, in_scope}. Covers the
                                  WHOLE song and flags which lines are sung by an
                                  IN-SCOPE performance shot. It also embeds the 3
                                  in-scope still job_ids so the pipeline survives
                                  a fresh session after the gitignored song.mp3
                                  is gone.
  audio_segments/<line_id>.wav    (full run only) one mono 24 kHz WAV per
                                  IN-SCOPE line, cut from song.mp3 with the
                                  bundled ffmpeg. This dir is gitignored.
  audio_segments/segments_manifest.json
                                  (full run only) line_id -> {path, sha256,
                                  duration_s, target_perf_key, still_id, model}.

Why only IN-SCOPE lines are sliced
----------------------------------
Only three performance shots are front-facing singing and will be lip-synced:
PERF_hook (the hook), PERF_lookup (choruses/pre-choruses, face up), PERF_window
(verses, seated). Their still job_ids are the wan2_7 start_image. The other
performance shots (profile / outside / reach / listen) won't lip-sync and are
left as-is. Non-performance imagery (memory / atmosphere) is never lip-synced.

Determinism
-----------
The line-map is a fixed, hand-authored lyric table (times from TREATMENT.md's
beat sheet) whose starts are snapped to the committed downbeat grid
(analysis/beats.json) purely arithmetically, so `--analyze-only` writes a
byte-identical line_map.json on every run. The slice is idempotent: WAVs are
written with a fixed ffmpeg invocation and the manifest is JSON-sorted, so a
re-run yields a byte-identical segments_manifest.json.

Usage
-----
  python3 scripts/slice_vocals.py --analyze-only   # write line_map.json only
  python3 scripts/slice_vocals.py                  # line_map.json + slice + manifest

The `--analyze-only` path needs NO audio and is the Commit-1 green-in-isolation
path; the full slice needs song.mp3 present.
"""
import sys, os, json, argparse, subprocess, hashlib, wave

try:
    import imageio_ffmpeg
    _HAVE_FFMPEG = True
except Exception:  # pragma: no cover
    _HAVE_FFMPEG = False

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SONG      = os.path.join(ROOT, "song.mp3")
BEATS_JSON = os.path.join(ROOT, "analysis", "beats.json")
SONG_JSON  = os.path.join(ROOT, "analysis", "song.json")
LINE_MAP   = os.path.join(ROOT, "analysis", "line_map.json")
SEG_DIR    = os.path.join(ROOT, "audio_segments")
MANIFEST   = os.path.join(SEG_DIR, "segments_manifest.json")

SEG_SR = 24000            # mono 24 kHz WAV — a safe, standard lip-sync input rate
LIPSYNC_MODEL = "wan2_7"  # Higgsfield audio-driven lip-sync model (start_image + audio)

# The three IN-SCOPE performance shots and their STILL job_ids (the wan2_7
# start_image). Durable copy so the pipeline survives a fresh session.
IN_SCOPE_STILLS = {
    "PERF_hook":   "8ec708fb-d76e-4d97-9d9b-5b383b81fd84",
    "PERF_lookup": "fbafd3d8-25bf-4897-9623-d4b2b66dbb46",
    "PERF_window": "da50c7fb-6dd0-4206-89ba-6f8aed9201ca",
}

# Section boundaries (start times) derived from analysis/song.json transitions.
# (name, start_s). The end of each section is the next section's start; the last
# ends at music_end. These match the treatment's section labels.
SECTIONS = [
    ("INTRO", 0.0),
    ("V1", 19.25),
    ("V2", 41.25),
    ("PRE1", 69.75),
    ("CH1", 89.25),
    ("V3", 130.5),
    ("V4", 144.5),
    ("PRE2", 173.0),
    ("CH2", 210.75),
    ("BRIDGE", 236.25),
    ("FINAL", 256.5),
]

# The lyric line table. Each entry is (raw_start_s, lyric, target_perf_key).
# raw_start_s comes from TREATMENT.md's beat sheet; it is snapped to the nearest
# committed downbeat at build time. target_perf_key names the performance shot
# whose mouth sings the line: only PERF_hook / PERF_lookup / PERF_window are
# IN SCOPE (front-facing singing that will be lip-synced). Lines carried by any
# other shot (profile/outside/reach/listen) or by memory/atmosphere imagery are
# tagged with their nearest performance intent but flagged out-of-scope by the
# in_scope rule below (in_scope == target_perf_key in IN_SCOPE_STILLS).
LYRIC_LINES = [
    # V1 — seated at the window (PERF_window carries the verse openers)
    (19.0,  "I think I feel you",                    "PERF_window"),
    (23.0,  "soft touch upon my skin",               "PERF_profile"),
    (31.0,  "my heart had crossed the ocean",        "PERF_window"),
    (35.0,  "where the rivers bend",                 "PERF_profile"),
    # V2 — verse, seated
    (43.0,  "I look for you beyond my shoulder",     "PERF_window"),
    (48.0,  "somewhere between the drops",           "PERF_profile"),
    (55.0,  "the sky still holds your whisper",      "PERF_window"),
    (60.0,  "and I need my world to stop",           "PERF_listen"),
    # PRE1 — build (hook shot enters; look-up on the rise)
    (70.0,  "don't know if you still feel it",       "PERF_window"),
    (74.0,  "I lose my breath",                      "PERF_lookup"),
    (78.0,  "the trees are moving",                  "PERF_profile"),
    (82.0,  "like you never left",                   "PERF_lookup"),
    # CH1 — the hook (PERF_hook + face-up PERF_lookup)
    (90.0,  "when it rains you're in the water",     "PERF_hook"),
    (94.0,  "like the thunder",                      "PERF_lookup"),
    (98.0,  "you're in the water",                   "PERF_hook"),
    (102.0, "like the thunder rolls",                "PERF_lookup"),
    (111.0, "when it rains you're in the water",     "PERF_hook"),
    (116.0, "like the thunder",                      "PERF_lookup"),
    (120.0, "you're always in the water",            "PERF_hook"),
    # V3 — fast, breathy (out-of-scope perf shots)
    (131.0, "I think I hear you",                    "PERF_listen"),
    (135.0, "the wind is howling",                   "PERF_profile"),
    (139.0, "every storm a reminder",                "PERF_window"),
    (142.0, "near but out of sight",                 "PERF_listen"),
    # V4 — denial, seated
    (145.0, "I hide your face in every mirror",      "PERF_window"),
    (152.0, "fold your memory in a drawer",          "PERF_profile"),
    (160.0, "clouds would pass me",                  "PERF_window"),
    (164.0, "like they always had before",          "PERF_profile"),
    # PRE2 — failed suppression, biggest build
    (173.0, "I'm trying to forget you",             "PERF_profile"),
    (183.0, "but I see you in the sky",              "PERF_lookup"),
    (195.0, "I still want you",                      "PERF_reach"),
    (203.0, "and I don't know why",                  "PERF_lookup"),
    # CH2 — second hook
    (211.0, "when it rains you're in the water",     "PERF_hook"),
    (215.0, "like the thunder",                      "PERF_lookup"),
    (219.0, "you're in the water",                   "PERF_hook"),
    (223.0, "like the thunder rolls",                "PERF_lookup"),
    (227.0, "always in the water",                   "PERF_hook"),
    # BRIDGE — surrender, outside
    (237.0, "this is where you landed",              "PERF_outside"),
    (241.0, "the words you said",                    "PERF_outside"),
    (247.0, "the sun won't shine if you're not mine","PERF_outside"),
    (251.0, "a flood I can't defend",                "PERF_outside"),
    # FINAL — haunt, quieter hook
    (257.0, "when it rains you're in the water",     "PERF_hook"),
    (263.0, "like the thunder",                      "PERF_lookup"),
    (269.0, "and I still wonder",                    "PERF_window"),
]


# --------------------------------------------------------------------------- #
# line-map derivation (deterministic, no audio)
# --------------------------------------------------------------------------- #
def _load_downbeats():
    d = json.load(open(BEATS_JSON))
    return [float(x) for x in d["downbeat_times"]]


def _music_end():
    if os.path.isfile(SONG_JSON):
        return float(json.load(open(SONG_JSON)).get("music_end", 273.75))
    return 273.75


def _snap(t, grid):
    """Nearest grid time to t (arithmetic, deterministic)."""
    return min(grid, key=lambda d: (abs(d - t), d))


def _section_for(t):
    """Section label whose [start, next_start) contains t."""
    sec = SECTIONS[0][0]
    for name, start in SECTIONS:
        if t >= start - 1e-9:
            sec = name
        else:
            break
    return sec


def build_line_map():
    """Derive the durable line-map dict. Pure arithmetic; no audio needed."""
    downbeats = _load_downbeats()
    music_end = _music_end()

    # Snap every raw line start to the nearest downbeat, in order. If a snap
    # collides with (or precedes) the previous line's start, advance to the
    # first downbeat strictly after it — this keeps starts strictly increasing
    # while staying fully deterministic (no audio, pure arithmetic).
    snapped = []
    for raw, _lyr, _k in LYRIC_LINES:
        s = round(_snap(raw, downbeats), 6)
        if snapped and s <= snapped[-1]:
            later = [d for d in downbeats if d > snapped[-1] + 1e-9]
            s = round(later[0], 6) if later else round(snapped[-1] + 1e-6, 6)
        snapped.append(s)

    lines = []
    n = len(LYRIC_LINES)
    for i, (raw, lyric, key) in enumerate(LYRIC_LINES):
        start = snapped[i]
        # end = next line's snapped start, else music_end; clamp to keep > start
        nxt = snapped[i + 1] if i + 1 < n else music_end
        if nxt <= start:
            nxt = min(start + 2.0, music_end)
        end = round(min(nxt, music_end), 6)
        in_scope = key in IN_SCOPE_STILLS
        lines.append({
            "line_id": f"L{i + 1:02d}",
            "section": _section_for(start),
            "raw_start_s": round(float(raw), 6),
            "start_s": start,
            "end_s": end,
            "duration_s": round(end - start, 6),
            "lyric": lyric,
            "target_perf_key": key,
            "still_id": IN_SCOPE_STILLS.get(key),   # None for out-of-scope
            "in_scope": in_scope,
        })

    return {
        "note": (
            "Deterministic lyric line-map for the Higgsfield-native lip-sync "
            "pipeline (P-017). Line starts are TREATMENT.md beat-sheet times "
            "snapped to the committed downbeat grid (analysis/beats.json). "
            "Only in_scope lines (target_perf_key in in_scope_stills) are sliced "
            "and lip-synced; they are sung by a front-facing performance shot. "
            "still_id is the wan2_7 start_image. This file is durable/committed "
            "so the pipeline survives after the gitignored song.mp3 is gone."
        ),
        "lipsync_model": LIPSYNC_MODEL,
        "segment_sample_rate": SEG_SR,
        "music_end_s": round(music_end, 4),
        "downbeat_grid": "analysis/beats.json:downbeat_times",
        "in_scope_stills": dict(IN_SCOPE_STILLS),
        "line_count": len(lines),
        "in_scope_line_count": sum(1 for l in lines if l["in_scope"]),
        "lines": lines,
    }


def write_line_map(m):
    with open(LINE_MAP, "w") as f:
        json.dump(m, f, indent=2, sort_keys=False)
        f.write("\n")


# --------------------------------------------------------------------------- #
# slicing (needs audio + bundled ffmpeg)
# --------------------------------------------------------------------------- #
def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _wav_duration(path):
    with wave.open(path, "rb") as w:
        return round(w.getnframes() / float(w.getframerate()), 6)


def _slice_one(start, end, out_path):
    """Cut [start, end) of song.mp3 to a mono SEG_SR WAV via bundled ffmpeg.

    Fully deterministic: fixed codec (pcm_s16le), fixed rate, -map_metadata -1 and
    -fflags +bitexact so the WAV bytes are reproducible across runs/machines.
    """
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    dur = max(0.0, end - start)
    cmd = [
        ff, "-v", "error", "-y",
        "-ss", f"{start:.6f}", "-t", f"{dur:.6f}",
        "-i", SONG,
        "-ac", "1", "-ar", str(SEG_SR),
        "-c:a", "pcm_s16le",
        "-map_metadata", "-1",
        "-fflags", "+bitexact", "-flags:a", "+bitexact",
        out_path,
    ]
    subprocess.run(cmd, check=True)


def slice_segments(line_map):
    """Slice every IN-SCOPE line to a WAV and build the deterministic manifest."""
    if not _HAVE_FFMPEG:
        raise RuntimeError("imageio_ffmpeg unavailable; cannot slice song.mp3")
    if not os.path.isfile(SONG):
        raise FileNotFoundError(
            f"{SONG} not found (it is gitignored). Slicing needs the audio present; "
            f"line_map.json is the durable artifact and survives without it."
        )
    os.makedirs(SEG_DIR, exist_ok=True)

    segments = []
    for l in line_map["lines"]:
        if not l["in_scope"]:
            continue
        rel = os.path.join("audio_segments", f"{l['line_id']}.wav")
        out = os.path.join(ROOT, rel)
        _slice_one(l["start_s"], l["end_s"], out)
        segments.append({
            "line_id": l["line_id"],
            "section": l["section"],
            "path": rel,
            "sha256": _sha256(out),
            "duration_s": _wav_duration(out),
            "start_s": l["start_s"],
            "end_s": l["end_s"],
            "lyric": l["lyric"],
            "target_perf_key": l["target_perf_key"],
            "still_id": l["still_id"],
            "model": LIPSYNC_MODEL,
        })

    segments.sort(key=lambda s: s["line_id"])
    manifest = {
        "note": (
            "Per-line vocal slices for the in-scope performance shots. Each WAV is "
            "the wan2_7 audio input; still_id is the start_image. Deterministic: "
            "re-running produces a byte-identical manifest."
        ),
        "lipsync_model": LIPSYNC_MODEL,
        "sample_rate": SEG_SR,
        "segment_count": len(segments),
        "segments": segments,
    }
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=False)
        f.write("\n")
    return manifest


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="line-map + per-line vocal slices for Higgsfield wan2_7 lip-sync")
    ap.add_argument("--analyze-only", action="store_true",
                    help="write analysis/line_map.json only; DO NOT slice audio")
    args = ap.parse_args(argv)

    m = build_line_map()
    write_line_map(m)
    print(f"wrote {os.path.relpath(LINE_MAP, ROOT)}  "
          f"({m['line_count']} lines, {m['in_scope_line_count']} in-scope, "
          f"model={m['lipsync_model']})")

    if args.analyze_only:
        print("--analyze-only: audio NOT sliced.")
        return 0

    manifest = slice_segments(m)
    total = sum(s["duration_s"] for s in manifest["segments"])
    print(f"wrote {os.path.relpath(MANIFEST, ROOT)}  "
          f"({manifest['segment_count']} segments, {total:.2f}s total vocal)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
