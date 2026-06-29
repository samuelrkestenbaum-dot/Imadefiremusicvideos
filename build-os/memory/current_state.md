# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** "When It Rains" — a 1970s-cinematic rain-drama **music
  video** built on Higgsfield. A warm wood-paneled band-performance world is
  intercut with a cool blue-grey breakup-memory story; **exactly one brunette
  woman** appears, only ever as memory / reflection / distant presence. The
  deliverable is a **rendered video**, not software.
- **Primary branch / base:** `claude/when-it-rains-music-video-fetr0z` (this repo
  has **no trunk** — no `origin/main`; "green" is judged against the branch tip).
- **Build/test command:** _there is no software test suite._ The deliverable is a
  rendered rough cut, and **it must be rendered on the USER'S Mac** via
  `when-it-rains/scripts/fetch_assets.sh` then
  `when-it-rains/scripts/assemble_rough_cut.sh`. The **cloud session CANNOT
  render**: the Higgsfield CDN is egress-blocked here and there is no system
  ffmpeg. "Proof" for this project = the user eyeballing a real render.

## Where we are

- **Last closed packet:** **P-003 — Section-Time Proposal
  (`when-it-rains/SECTION_TIMES.md`)** (qa GREEN 9/9, reviewer PASS; receipt
  `build-os/receipts/P-003.md`). A data-driven confirm/correct worksheet now
  exists proposing the song's section starts — **6 KEEP** (INTRO, V1, V3, CH2,
  BRIDGE, FINAL) + **5 SUGGESTED** (V2 → 0:41, PRE1 → 1:10, CH1 → 1:29 [or 1:51],
  V4 → 2:24.5, PRE2 → 2:53); committed locally (`39f84d7`, not pushed). It feeds
  the future beat-lock packet but does NOT change the edit. (P-002 — Render-Review
  Checklist `when-it-rains/RENDER_REVIEW.md` — closed before it; P-001 — Install
  Build OS + seed memory — before that.)
- **Now:** no active build packet — **awaiting the user's confirm/correct of the
  section times** in `when-it-rains/SECTION_TIMES.md`. Key open question: the
  **CH1 chorus downbeat — 1:29 vs 1:51** — which also settles **PRE1**. (Also
  still open: the user's human-eye render review via `RENDER_REVIEW.md`, P-002.)
- **Next:** on the user's confirmed section times → **build the beat-lock script +
  apply it to `data/edl.csv`** — snap the 76 cuts to the **0.97524s** beat grid
  (61.5234375 BPM) **+ trim ~2s from FINAL** so the 276s EDL resolves on the 274s
  mix end; and/or targeted regen refinement; optional band-coverage batch (lower
  priority).

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section. IDs +
  CDN URLs live in `when-it-rains/data/clips.csv` (26 clips), `stills.csv` (42
  stills), `assets.json`.
- **Edit kit:** `data/edl.csv` = **76 cuts ≈ 4:34 runtime** (sums to 276s; the
  Jun-27 mix targets 274s, so the FINAL hold is currently truncated ~2s — fix in
  the beat-lock pass).
- **Song analysis (reproducible in-session):** `analyze_song.py` / `song.json` —
  `music_end 273.75`, `duration 284.4`, `tempo 61.5234375` BPM (→ **0.97524s**
  per beat), 12 transitions. The song MP3 has been **re-attached + staged**
  (gitignored) and the analysis re-verified reproducible this session; `numpy` +
  `imageio-ffmpeg` are installed. (The MP3 itself will NOT survive a new session.)
- **Footage audit + regeneration: DONE.** All 26 clips were inspected via
  Higgsfield server-side `video_analysis` (free, bypasses the CDN block). It
  found the lead rendered **bald/shaved in 22 of 76 cuts** (cool story clips) +
  4 content failures (C06, C07, C22, C23) + an auburn woman (C16). Root cause:
  the man-stills were generated with **no reference image attached**. All **11**
  flagged clips were **regenerated reference-anchored, re-animated, and
  re-analyzed to verify** (anchors `5cc8239a` man / `1143614b` woman); 10 fully
  accepted, C04 partial (hair + reflection fixed, head-turn still absent).
  `data/clips.csv` now points at the fixed clips (originals in
  `data/clips_original_backup.csv`). Spend ~106.5 credits; ~2,505 left.
- **Verification caveat:** the fixes were confirmed by **automated re-analysis,
  NOT a human eye** (canary on C13) — a real render is the final confidence check.
  `when-it-rains/RENDER_REVIEW.md` (P-002) is the structured instrument for that
  still-pending human review.
- **Creative invariants:** the man = fair freckled skin, reddish beard, short
  cropped red-blonde hair with a receding hairline (NOT bald/shaved/buzzed); the
  woman = one brunette, long dark wavy hair, only ever memory/reflection. Look =
  16:9, 35mm grain, 1970s cinematic; performance = warm amber/wood, story = cool
  blue-grey rain. One narrative motion per clip.

---
_Updated by the archivist on close. Seeded from `when-it-rains/HANDOFF.md`,
`FOOTAGE_AUDIT.md`, `README.md`, and `data/` on 2026-06-29. P-001 closed
2026-06-29; P-002 closed 2026-06-29; P-003 closed 2026-06-29._
