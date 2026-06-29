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

- **Last closed packet:** **P-001 — Install Build OS + seed memory** (qa GREEN,
  reviewer PASS; receipt `build-os/receipts/P-001.md`). Build OS engine + real
  project memory are now installed and committed locally (not pushed).
- **Now:** no active build packet — **awaiting a human-eye render review** of the
  regenerated footage. Next real work is off-machine + user-driven.
- **Next:** user renders the rough cut on their Mac + reviews it → confirms the
  ambiguous mid-song section times (V2/PRE1/CH1, V4/PRE2) → on their word,
  regenerate `data/edl.csv` to snap cuts to the beat grid and trim ~2s from the
  FINAL section.

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section. IDs +
  CDN URLs live in `when-it-rains/data/clips.csv` (26 clips), `stills.csv` (42
  stills), `assets.json`.
- **Edit kit:** `data/edl.csv` = **76 cuts ≈ 4:34 runtime** (sums to 276s; the
  Jun-27 mix targets 274s, so the FINAL hold is currently truncated ~2s — fix in
  the beat-lock pass).
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
- **Creative invariants:** the man = fair freckled skin, reddish beard, short
  cropped red-blonde hair with a receding hairline (NOT bald/shaved/buzzed); the
  woman = one brunette, long dark wavy hair, only ever memory/reflection. Look =
  16:9, 35mm grain, 1970s cinematic; performance = warm amber/wood, story = cool
  blue-grey rain. One narrative motion per clip.

---
_Updated by the archivist on close. Seeded from `when-it-rains/HANDOFF.md`,
`FOOTAGE_AUDIT.md`, `README.md`, and `data/` on 2026-06-29. P-001 closed
2026-06-29._
