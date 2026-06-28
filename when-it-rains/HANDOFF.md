# HANDOFF — resume context for a new session

Read this first, then `README.md` → `REVIEW.md` → `EDIT_MAP.md` → `data/assets.json`.

## Where the project stands
- **Concept/edit locked.** 1970s rain drama: warm band-performance world intercut
  with a cool blue-grey breakup-memory story; one brunette woman only, as
  memory/reflection. Target runtime **4:34** (this Jun-27 mix; music resolves ~4:33.8).
- **Assets generated on Higgsfield:** 42 stills + 26 animated clips (Kling v3.0,
  silent 5s, start-frame, one motion each) covering every section. IDs + CDN URLs
  are in `data/clips.csv`, `data/stills.csv`, `data/assets.json`.
- **Assembly kit built:** `data/edl.csv` (76 cuts = 4:34), `scripts/fetch_assets.sh`,
  `scripts/assemble_rough_cut.sh`. The user renders the rough cut on their Mac
  (the cloud session can't: Higgsfield CDN is egress-blocked, no system ffmpeg).
- **Song analyzed:** `analysis/` — file 4:44.4, music ends ~4:33.8, ~61.5 BPM,
  climaxes ~1:22–1:40 / 2:43–3:04 / 3:48–end.

## NOT in git (will not survive into a new session)
- **The song MP3** (gitignored, lives only in this session's uploads dir). If audio
  work is needed again, the user must re-attach `When_It_Rains__Jun_27_mix.mp3`.
- **Downloaded clips/stills** (gitignored). Re-create locally with `fetch_assets.sh`;
  the source of truth is the Higgsfield account.

## Open threads (next actions, in order)
1. **User renders + reviews** the rough cut, flags failures by timecode (REVIEW.md).
2. **User confirms mid-song section times** (V2/PRE1/CH1, V4/PRE2 are ambiguous from
   energy). On their word → regenerate `data/edl.csv` to snap cuts to the beat grid.
3. **Band-coverage batch (REVIEW.md §7)** — ~8 clips (drummer CU, guitar hands, keys,
   bass, push-in, singer profile, 2nd front CU, detail inserts). Staged, NOT generated.
   Fire only after the rough cut confirms thinness (C02 is overused 11×).
4. **Do NOT yet:** upscale (do last), or regenerate the brunette (only if she reads
   as multiple women on playback).

## Higgsfield working context (for regeneration)
- Account: private workspace, ultra plan, ~2,600 credits left at last check.
- Still recipe: `nano_banana_2`, 16:9, 1k. Clip recipe: `generate_video` model
  `kling3_0`, `mode:"std"`, `sound:"off"`, `duration:5`, role `start_image`.
- Dark/rain prompts trigger the "IN THE DARK" preset intercept — pass
  `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"` to generate literally.
- Man's reference selfies (uploaded media IDs): `fd3902a2-34d6-41a8-92c4-cb1082cb633d`,
  `81d923ee-cc81-41ea-9dc0-39d40b3d8cd4`, `bb1fa35c-6c75-42ad-93f5-48de485e35b6`.
  On-model likeness = short cropped red-blonde hair, receding hairline, reddish
  beard, NOT bald (earlier "buzzed" stills 22e02845/b0f3fd47/26443c5f/ff3797c3 are
  off-model and unused).
- Re-list past generations anytime via Higgsfield MCP `show_generations`.
