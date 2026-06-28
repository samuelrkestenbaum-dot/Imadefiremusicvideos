# HANDOFF — resume context for a new session

Read this first, then `FOOTAGE_AUDIT.md` (newest, most important) → `README.md` →
`REVIEW.md` → `EDIT_MAP.md` → `data/assets.json`.

> **Branch note:** active work is now on `claude/when-it-rains-music-video-0qzesv`
> (a fresh clone may land on a different default branch — check `git branch`).

## ⭐ Newest result — footage audit done WITHOUT a render (this session)
All 26 clips were inspected via Higgsfield server-side `video_analysis` (free,
~16s each, bypasses the CDN block — no download). Findings in `FOOTAGE_AUDIT.md`
+ `data/footage_findings.json`. Two things you must know:
- **The male lead is rendered BALD/SHAVED in the cool story clips** (C01 buzz,
  C04, C07, C13, C15, C19, C23, EX2 bald/shaved) — on-model only in the warm
  performance clips (C02/C09/C12/C17/C20). **22 of 76 cuts** show an off-model
  lead. The prior claim that the on-model likeness was "used everywhere" was wrong.
- **4 hard content failures:** C07 (woman-reflection beat never renders), C06
  (two people, not an empty ocean), C22 (unwanted man), C23 (final shot missing
  its turn-to-camera). C16's woman drifts auburn.
- **Decision pending from the user:** regenerate scope (P1 content failures only,
  or P1+P2 bald-lead clips too). The regen→re-analyze→verify loop is closed and
  free, so a new session can execute and self-check once scope is confirmed.

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
1. **Regenerate the off-model lead + content failures** (`FOOTAGE_AUDIT.md` §5).
   This now outranks everything else — a bald lead in ~29% of cuts is worse than
   any pacing issue. Order: **P1** content failures (C07, C23, C06, C22) → **P2**
   bald story clips (C04, C13, C15, C19, ±C01) → **P3** polish (C16 auburn→brunette,
   C24 world-look, C10 pedestrian). Root-cause fix: lock the lead with a reference
   from a clean performance frame (C02/C12/C20), add "not bald/shaved/buzzed,
   visible hair + receding hairline" to every non-performance **still**, regen the
   still first → re-animate → re-run `video_analysis` to verify before accepting.
2. **User confirms mid-song section times** (V2/PRE1/CH1, V4/PRE2 ambiguous from
   energy). On their word → regenerate `data/edl.csv` to snap cuts to the beat grid.
   Also trim ~2s from the FINAL section: the EDL is 276s but the mix targets 274s,
   so the ending currently gets hard-truncated (`FOOTAGE_AUDIT.md` §6).
3. **User renders + reviews** the rough cut on their Mac (still needed for true
   timing feel + a final human eye on the regenerated clips).
4. **Band-coverage batch (REVIEW.md §7)** — ~8 clips. Lower priority than the
   likeness fix; fire after the lead is locked. (C02 is overused 11× but is itself
   on-model, so this is pacing, not quality.)
5. **Do NOT yet:** upscale (do last, after the cut is emotionally locked).

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
