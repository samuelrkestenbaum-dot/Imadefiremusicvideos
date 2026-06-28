# "When It Rains" — Music Video Production

A 1970s-cinematic rain drama built on **Higgsfield**. The band performs the song
in a warm wood-paneled room while the story shows a man moving through a rainy
world where every reflective surface, storm, and body of water seems to contain
the same brunette woman — a memory he can't escape. Performance and memory
intercut constantly until the bridge floods the two worlds together.

**Target runtime: 4:36** (the WAV runs ~4:54.9, but the usable musical edit lives
around 4:30–4:36 — build to 4:36 so the final *"and I still wonder"* lands before
the long silent tail).

---

## What's in this folder

| File | What it is |
|------|------------|
| `FOOTAGE_AUDIT.md` | **Per-clip audit of the actual footage** (via Higgsfield `video_analysis`): which clips are off-model / failed, with a ranked regeneration plan. Read this first. |
| `data/footage_findings.json` | Machine-readable version of the audit (per-clip flags + man/woman consistency verdicts). |
| `EDIT_MAP.md` | The shot-by-shot edit: every section, timecode, which clip, and the one narrative motion it carries. This is the assembly bible. |
| `data/assets.json` | Machine-readable catalog of every Higgsfield asset (reference uploads, stills, animated clips) with IDs and URLs. |
| `data/edl.csv` | The Edit Decision List the assembly script reads: `index, clip_key, in_point, duration, section, note`. Edit this to re-time the cut. |
| `data/clips.csv` | Flat list of animated clips: `clip_key, job_id, source_still, mp4_url, section, motion`. |
| `data/stills.csv` | Flat list of all stills: `still_id, url, beat, on_model, prompt_summary`. |
| `scripts/fetch_assets.sh` | Run **on your machine** (no egress block there): downloads every clip + still into `clips/` and `stills/`. |
| `scripts/assemble_rough_cut.sh` | Run **on your machine**: reads `edl.csv` + `clips/` + your `song.wav`, produces `when_it_rains_roughcut.mp4` cut to 4:36 with the song on top. Needs `ffmpeg`. |

---

## Why assembly happens on your machine, not here

Everything *generative* was done inside Higgsfield (stills + animated clips, all
stored on Higgsfield's CDN). Three things prevent the final cut from being
rendered in this cloud session:

1. **Egress policy** — this session's network proxy blocks Higgsfield's CDN
   hosts, so the rendered `.mp4` files can't be downloaded into this container.
2. **No timeline tool** — Higgsfield generates clips but has no
   multi-clip-to-a-provided-song timeline editor.
3. **The song** — the `When It Rains` WAV isn't in this repo.

So the deliverable here is **the complete clip library (already generated on
Higgsfield) + a precise, runnable assembly kit**. You run two scripts locally and
get the rough cut. Then fine-tune timing in your NLE.

---

## Quickstart (on your machine)

```bash
cd when-it-rains
# 1. Download every generated clip + still from Higgsfield
bash scripts/fetch_assets.sh
# 2. Drop your song in as song.wav (any audio ffmpeg reads works; rename to song.wav)
cp /path/to/when_it_rains.wav song.wav
# 3. Build the 4:36 rough cut with the song on top
bash scripts/assemble_rough_cut.sh
# -> when_it_rains_roughcut.mp4
```

Then open `when_it_rains_roughcut.mp4` to review, and edit `data/edl.csv` (change
durations / swap clip keys) and re-run step 3 to re-time. Nothing is locked.

---

## Creative rules baked into every asset

**The man (lead):** fair freckled skin, reddish beard, short cropped red-blonde
hair with a receding hairline — hair visible on top and sides, *not* bald, *not*
shaved. Emotionally restrained throughout.

**The woman (memory):** exactly **one** brunette woman, long dark wavy hair. She
is only ever a memory / reflection / distant presence. Never multiplied, never a
blonde, never a second woman in frame, never a literal ghost effect, never a
romantic reunion.

**Look:** widescreen 16:9, 35mm grain, 1970s cinematic. Performance world = warm
amber/wood. Story world = cool blue-grey rain.

**Motion rule:** each clip carries **one** action (he turns, the reflection
breaks, the room floods) — deliberately *not* generic "breathing" ambient motion,
which reads as AI wallpaper.

---

## Status

- ✅ Still library covering every beat (band, story, woman-as-memory, water/sky inserts).
- ✅ Animated clip backbone generated (one narrative motion per clip, silent so the song lays on top).
- ✅ Edit map + EDL + local assembly kit.
- ✅ **Footage audit complete (`FOOTAGE_AUDIT.md`)** — every clip inspected via Higgsfield `video_analysis`.
- ⚠️ **Reference identity NOT actually locked.** The audit found the lead renders
  **bald/shaved in the cool story clips** (on-model only in the warm performance
  clips) — ~22 of 76 cuts. Plus 4 content failures (C06/C07/C22/C23). **A
  regeneration pass on the lead is the top open item** — see `FOOTAGE_AUDIT.md` §5.
- ⏳ Regenerate off-model/failed clips → beat-lock the EDL → final song-synced cut → selective 2K/4K upscale.

See `FOOTAGE_AUDIT.md` for the failure list and `EDIT_MAP.md` for the full edit breakdown.
