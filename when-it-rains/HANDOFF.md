# HANDOFF — resume context for a new session

Read this first, then `FOOTAGE_AUDIT.md` (newest, most important) → `README.md` →
`REVIEW.md` → `EDIT_MAP.md` → `data/assets.json`.

> **Branch note:** active work is now on `claude/when-it-rains-music-video-fetr0z`
> (a fresh clone may land on a different default branch — check `git branch`).

## ⭐ Newest result — band coverage added, edit re-timed to 86 cuts / 274s
The mid-song **section times are CONFIRMED and applied** (P-004 section-sync), and
a **band-coverage batch was generated and inserted** (C25–C34) to fix the
post-section-sync drag in PRE2/CH1.

- **Assets now on Higgsfield:** **52 source stills + 36 animated clips** (was
  42 + 26). The 10 new clips are band/performance coverage **C25–C34** (drummer,
  bassist, keys, guitar hands, two singer-facing shots).
- **Edit:** `data/edl.csv` is now **86 cuts = 4:34 / 274.0s** (was 76 cuts / 4:36).
  PRE2 and CH1 were **re-balanced** with the new band coverage to kill the drag
  that section-sync exposed (P-005 plan → P-006 generate → P-007 insert).
- **On-model verification (real result):** the 2 singer-facing new clips were
  checked via Higgsfield `video_analysis` and **BOTH read ON-MODEL**:
  - **C27** (PRE2, profile): "late-30s, fair complexion, very short thinning
    reddish hair, light beard".
  - **C33** (CH1, chorus CU): "mid-30s, freckles, short ginger hair, trimmed
    ginger beard".
  i.e. short reddish/ginger hair + beard, **NOT bald** — the bald root-cause fix
  (reference-anchoring the man-stills) held through this batch too.

### Earlier result — audit AND regeneration (prior session)
All clips were inspected via Higgsfield server-side `video_analysis` (free,
~16s each, bypasses the CDN block — no download). It found the lead rendered
**bald/shaved** in many cool story clips + content failures (C06, C07, C22, C23)
+ an auburn woman (C16). **Root cause:** the man-stills were generated with **no
reference image attached** (pure text), so he drifted bald. All flagged clips
were then **REGENERATED** reference-anchored (`5cc8239a` man / `1143614b` woman) →
re-animated → re-analyzed to verify. `data/clips.csv` points at the FIXED clips
(originals in `data/clips_original_backup.csv`). Full breakdown in
`FOOTAGE_AUDIT.md` §8 + `data/footage_findings.json`.

**Caveat:** verification was automated re-analysis, not a human eye (CDN is
egress-blocked here). A real render is the final confidence check. For a perfect
face-lock, train a Soul from the selfies + best frames and regen from it.

## Where the project stands
- **Concept/edit locked.** 1970s rain drama: warm band-performance world intercut
  with a cool blue-grey breakup-memory story; one brunette woman only, as
  memory/reflection. Target runtime **4:34** (this Jun-27 mix; music resolves ~4:33.8).
- **Assets generated on Higgsfield:** **52 stills + 36 animated clips** (Kling v3.0,
  silent 5s, start-frame, one motion each) covering every section, including the
  C25–C34 band coverage. IDs + CDN URLs are in `data/clips.csv`, `data/stills.csv`,
  `data/assets.json`.
- **Assembly kit built:** `data/edl.csv` (**86 cuts = 4:34 / 274.0s**),
  `scripts/fetch_assets.sh`, `scripts/assemble_rough_cut.sh`. The user renders the
  rough cut on their Mac (the cloud session can't: Higgsfield CDN is egress-blocked,
  no system ffmpeg).
- **Backup chain (history):** `data/edl_original_backup.csv` (pre-section-sync),
  `data/edl_pre_bandcoverage_backup.csv` (pre-band-coverage),
  `data/clips_original_backup.csv` (pre-regen).
- **Song analyzed:** `analysis/` — file 4:44.4, music ends ~4:33.8, ~61.5 BPM,
  climaxes ~1:22–1:40 / 2:43–3:04 / 3:48–end.

## NOT in git (will not survive into a new session)
- **The song MP3** (gitignored, lives only in this session's uploads dir). If audio
  work is needed again, the user must re-attach `When_It_Rains__Jun_27_mix.mp3`.
- **Downloaded clips/stills** (gitignored). Re-create locally with `fetch_assets.sh`;
  the source of truth is the Higgsfield account.

## Open threads (next actions, in order)
1. **User's render-review (the remaining open item).** Render on the Mac via
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `RENDER_REVIEW.md`, for overall pacing/aesthetic sign-off — including a human
   eye on the C25–C34 band coverage and the re-timed PRE2/CH1. (The on-model check
   on C27/C33 was automated analysis; the render is the final confidence check.)
2. **DONE — mid-song section-time confirmation** (V2/PRE1/CH1, V4/PRE2): confirmed
   and applied as the P-004 section-sync; `data/edl.csv` now snaps to that grid and
   targets 274s (no more hard end-truncation).
3. **DONE — band-coverage batch** (REVIEW.md §7): C25–C34 generated (P-006) and
   inserted with PRE2/CH1 re-balanced (P-007). On-model verified (C27, C33).
4. **Optional later:** sub-beat quantization of cuts to the beat grid.
5. **Do LAST:** upscale (only after the cut is emotionally locked and signed off).

## Higgsfield working context (for regeneration)
- Account: private workspace, ultra plan; check remaining credits via the MCP.
- Still recipe: `nano_banana_2`, 16:9, 1k. Clip recipe: `generate_video` model
  `kling3_0`, `mode:"std"`, `sound:"off"`, `duration:5`, role `start_image`.
- Dark/rain prompts trigger the "IN THE DARK" preset intercept — pass
  `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"` to generate literally.
- Man's reference selfies (uploaded media IDs): `fd3902a2-34d6-41a8-92c4-cb1082cb633d`,
  `81d923ee-cc81-41ea-9dc0-39d40b3d8cd4`, `bb1fa35c-6c75-42ad-93f5-48de485e35b6`.
  On-model likeness = short cropped red-blonde/ginger hair, receding hairline,
  reddish beard, NOT bald (earlier "buzzed" stills 22e02845/b0f3fd47/26443c5f/
  ff3797c3 are off-model and unused).
- Re-list past generations anytime via Higgsfield MCP `show_generations`.
