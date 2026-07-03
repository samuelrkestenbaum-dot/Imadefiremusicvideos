# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** "When It Rains" — a rain-drama **music video** built on
  Higgsfield. **AESTHETIC ADVANCED (P-016 director's cut):** the live edit is now
  a **late-90s / early-2000s** bleach-bypass rain-ballad — the artist as a
  **buzz-cut / fit / soaked 2000s frontman** intercut with a **consistent memory
  woman** + atmosphere. (The prior **1970s** wood-paneled band cut is preserved as
  `data/{edl,clips,stills}.70s.csv`, not deleted — history kept.) The deliverable
  is a **rendered video**, not software.
- **STYLE LOCKED (P-018 chorus lock):** the canonical production style is now
  the **LOCKED chorus** (`when-it-rains/scripts/render_chorus_v16.sh` →
  `when-it-rains/chorus_v16.mp4`) + **`when-it-rains/PRODUCTION_PLAYBOOK.md`**
  — the copy-paste bible for every remaining section. Identity is durable: a
  **trained Soul** of the artist (`07822e21-af62-44cc-a8b8-0b27dfe6de8a`) + two
  reference **elements** (`wir-him` / `wir-her`). Narrative source of truth is
  `when-it-rains/STORY.md`. The P-016 107-cut `data/edl.csv` director's cut
  **predates the playbook method** and will be superseded section by section.
- **INTRO LOCKED (P-018/P-019 intro pair, 2026-07-02):**
  `when-it-rains/scripts/render_intro_v6.sh` → `when-it-rains/intro_v6.mp4` is
  the **second reference cut** (user verdict: **"Amazing"**). **Double-bed
  canon**; `INTRO_SCENE_SPEC.md` LOCKED with all final asset IDs. The playbook
  gained **law 0 "DERIVE, DON'T DESCRIBE"** (every scene asset derives from the
  scene master, never a fresh text prompt) and **law 0b "SANDBOX EYES"** (the
  CI review-fetch loop — `scripts/fetch_review.sh` downloads `review_urls.txt`
  assets into `when-it-rains/review/`, videos as 2fps frame PNGs, so the
  sandbox inspects EVERY asset before spend/ship). Both laws bind every future
  scene packet. Combined receipt `build-os/receipts/P-018_P-019.md` (note: the
  id P-018 collides with the chorus-lock receipt — numbering resumes at P-020).
- **Primary branch / base:** **`claude/when-it-rains-handoff-l0u075`** (P-023;
  supersedes the fetr0z-era branches — same history; this repo has **no trunk**
  — no `origin/main`; "green" is judged against the branch tip). The CI relay
  workflow `render-chorus.yml` is **branch-agnostic** (follows
  `${{ github.ref_name }}`).
- **Build/test command:** _there is no software test suite._ The deliverable is a
  rendered rough cut, and **it must be rendered on the USER'S Mac** via
  `when-it-rains/scripts/fetch_assets.sh` then
  `when-it-rains/scripts/assemble_rough_cut.sh`. The **cloud session CANNOT
  render**: the Higgsfield CDN is egress-blocked here and there is no system
  ffmpeg. "Proof" for this project = the user eyeballing a real render. There is
  also `when-it-rains/preview.html` (P-011) — a self-contained, browser-playable
  in-browser review aid that streams the clip mp4s from the CDN (browser-reachable
  even though this cloud session's egress is blocked); silent + approximate-timing,
  but it lets the user review the rough cut in a browser without the Mac
  fetch+ffmpeg render. NOTE: `preview.html` predates P-016 and still reflects the
  older 86-cut edit — the authoritative live edit is now the P-016 **107-cut /
  274.00 s** 2000s director's cut (`data/edl.csv`).

## Where we are

- **Last closed packet:** **P-024 — PRE1 (70.3–89.8): the darkening walk —
  CLOSED 2026-07-03, final frame-QC = SHIP, PRE1 likeness 9/10.** Delivered
  **`pre1_v1.mp4`** (19.51s) + **`first90.mp4`** (89.79s, **frame-exact grid**,
  **July Reverb mix** bed) on `claude/when-it-rains-handoff-l0u075`. Board
  user-approved; masters user-gated: walk = W2 `4aaefb8b` + chain scrub →
  `361af0a5`; turn = T3 `d1688201` → LOCAL rotate90CW + chest-up crop
  (`turn_master_crop.png`, imported `b59d18d8`, ZERO nano passes — **user chose
  T3 over the recommended T4**); trees derived from the scrubbed walk
  (`b6f2262e`, law 0). Takes: walk-stop-breath kling `584f5e2b` (10s), gust
  kling `8543a623` (5s); sync wan RETRY `97a9771e` (8s) → 2K `c6888a50` (first
  take turned away from camera 4.5s mid-line + warped hand at exit — fixed
  first-retry by **wan behavioral pinning**: sings DIRECTLY INTO CAMERA, never
  turns away, exit confined to a stated final window, no hand near lens).
  **NEW LAWS:** (1) **July Reverb mix swap** — same clock, VERIFIED by envelope
  cross-correlation at 31.2/58.5/89.8/109.3 (all 0ms; rings to ~277s); always
  cross-correlate anchors before slicing a new mix; (2) **FRAME-EXACT STITCH
  LAW** — naive concat drifted ~0.3s EARLY by 70s; tpad+trim each seg to exact
  frame counts (`render_p024.sh`: 576/456/655/468) in every future stitch;
  (3) wan behavioral pinning (above); (4) soul_2 chest-up+facing-camera renders
  ROTATED 90° 4/4 — salvage locally (rotate+crop), don't reroll; kling
  `sound:"off"` must be explicit. Vocal-envelope verification used twice
  (breath-gap check; new-mix clock check). **Mid-packet: six-lens directors
  review → `DIRECTORS_NOTES.md`** (verdict: story works, demo → label-pitch
  after must-fixes) — **ROADMAP back-half section clock VERIFIED WRONG** (CH1
  really 42.9s, FINAL 16.2s; PRE1 unaffected) — re-time pending in P-025.
  Credits at close: **1371.75** (~34 spent vs 150–200 est). Commits `80f373f`→
  `057f739` (23: 15 relay + 8 CI) + close, base `2f791a8`; ≤2-commit contract
  acknowledged inapplicable (media-relay precedent). Receipt
  `build-os/receipts/P-024.md`; asset IDs + laws in `when-it-rains/HANDOFF.md`
  (P-024 addendum).
- **Last closed packet (prior):** **P-023 — first70 revision (mug grain, lip-sync
  timing, AI-look syncs, curb finale redesign) — CLOSED 2026-07-03, final
  frame-QC = SHIP.** Delivered **`first70.mp4` v2** (continuous 0–70.3, 70.0s)
  + recuts `v1_v2.mp4` (19.5s) / `v2_v2.mp4` (27.3s) on
  `claude/when-it-rains-handoff-l0u075`. The user's four notes on v1 ALL
  resolved: (1) grainy mugs → 2K-enhanced take `82720c7f`; (2) late lip-sync
  onset → onset-tight slices + new wan syncs (kitchen `552f47fe`→2K `c3cddeb8`,
  awning retry `ee8d1c61`→2K `ab86a6c8`; first awning wan `3397e6b4` rejected
  in frame-QC); (3) AI-look sung shots → realism stills `d52d9aeb`/`a919b037`
  (likeness 8.5/7.5); (4) curb finale → **12s CURB ZOOM SYNC** (wan
  `da598028`→2K `2ad7d2e3`, accelerating zoompan + vignette + desat ramp in
  `render_v2_v2.sh`). Curb frame saga → **NEW HARD RULE: no bare chest, ever**
  (delete on sight, history-purge repo copies, salvage-don't-reroll wardrobe
  fixes; 3 bare-chest rolls remain in the Higgsfield library for the USER to
  delete in the UI). New QC method: verify "mouth stops" flags against the
  slice's mid-band FFT energy envelope — wan honors breath gaps. Proof =
  frame-QC by vision subagent before every spend + final 140-frame SHIP pass
  (3 non-blocking caveats recorded). Credits at close: **1405.71**. Commits
  `c1e1efa`→`9992e95` (18: 11 relay + 7 CI) + close; ≤2-commit contract
  acknowledged inapplicable to the CI-relay media workflow (P-020/P-022
  precedent). Receipt `build-os/receipts/P-023.md`; full asset IDs + ops
  learnings in `when-it-rains/HANDOFF.md`.
- **Memory catch-up (P-020 → P-022 — memory/ had lagged at P-018/P-019 because
  the archivist hit usage-credit walls; receipts were main-loop fallback):**
  **P-020** — Verse 1 kitchen (23.5–43.0), `v1_v1.mp4` **USER LOCKED "Great"**
  + `first43.mp4`; ROLES LAW (wan2_7 needs exact roles
  `start_image`/`audio_references`); local ffmpeg via `imageio-ffmpeg`; receipt
  `P-020.md`. **P-021** — V2 board (43.0–70.3, street/look-back) → `v2_v1.mp4`,
  commits `def07ba`..`ecc9bc9` — **closed UNRECEIPTED** (receipt debt
  acknowledged in the P-023 receipt; superseded by the P-022 recut). **P-022**
  — likeness repair + `review/ANCHOR_BOARD.png` (permanent likeness reference)
  + ladder inserts; delivered **`first70.mp4` v1** + `v1_v2`/`v2_v2` recuts;
  receipt `P-022.md`. Also LOCKED since: `V1_SCENE_SPEC.md`. Story/plan canon:
  **`when-it-rains/ROADMAP.md`** (story ladder + likeness lock + packet plan).
- **Last closed packet:** **P-018/P-019 (intro pair) — INTRO LOCKED** —
  media-production pair (user-directed, playbook-driven), **21 commits**
  `f724323..25b8b80` (12 authored + 9 CI render commits; base **`f724323`** =
  the intro_v4 CI render; tip **`25b8b80`**; the branch auto-mirrors to
  origin). Unreceipted preceding context recorded in the receipt: the intro
  v1–v4 sprint `e9ff090..f724323`, incl. `2da7e93` — the CI **push trigger via
  `render_request.txt` line-1 + nonce** (github MCP dispatch now optional).
  **P-018 — regenerate bed setup (intro v5):** user feedback on intro_v4 — the
  nightstand insert was a DIFFERENT bedroom (sunny, wrong sheets) and the bed
  had to become a **DOUBLE bed** so the "her untouched side" beat works. Root
  cause: the insert was generated from a fresh text prompt instead of DERIVED
  from the scene master, and the sandbox cannot see CDN images (assets used
  blind). Built the **CI review-fetch path** (`scripts/fetch_review.sh` +
  `render-chorus.yml` commit-step, `eabfcd4`+`976f4bc`) — sandbox eyes on every
  asset BEFORE spending or shipping. New assets ALL derived from the
  user-approved soul_2 bed master job `2d080b77`: bed take kling 10s
  `eea03072` (still 0–6s, head-turn 6.5–7.5s, rise 8.5–10s — measured from
  frames), her-half tight insert nano chain `9924df64` → `f64ef24d` → kling 5s
  `8bd72a9d` (first attempt `9924df64` CAUGHT in frame QC — WHOLE bed empty,
  continuity bug — re-derived tighter). Output `render_intro_v5.sh` →
  `intro_v5.mp4`; user: "Looks great except [opening shot mismatch]".
  **P-019 — match opening rain shot (intro v6):** the opening rain-on-glass
  exterior didn't match the bedroom window; fixed BY DERIVATION — nano window
  close-up from the master (`c63df6d2`) → kling 8s `371791eb`, frame-QC'd
  (locked camera, same building/road as the master). Output
  `render_intro_v6.sh` → `intro_v6.mp4` — **USER LOCKED THE INTRO:
  "Amazing"**. Doc canon (`25b8b80`): `INTRO_SCENE_SPEC.md` LOCKED (final
  asset IDs, double-bed canon); `PRODUCTION_PLAYBOOK.md` laws 0 + 0b, section
  6 records intro_v6 as the second reference cut. **Proof = review-fetch frame
  QC + user verdicts on CI renders** (accepted process deviation, same as the
  chorus era); no formal qa/reviewer; Codex not run. Receipt
  `build-os/receipts/P-018_P-019.md`.
- **Last closed packet (prior):** **P-018 — CHORUS LOCK (the chorus-production era)** —
  media / creative sprint (user-directed, post-P-017), **32 commits**
  `8a5048c..bc9d4d7` on base **`90ce268`** (+ CI render commit **`8a2e88d`** =
  `chorus_v16.mp4`; the branch **auto-mirrors to origin**). Delivered: (1)
  **trained Soul of the artist** — soul_id
  `07822e21-af62-44cc-a8b8-0b27dfe6de8a` (8 real photos; photos REMOVED from
  the repo tree after training for privacy — still in git HISTORY, see
  residue); (2) **reference elements** `wir-him` =
  `1b581c11-e515-4d88-bb2c-b2b0af3b722d` (from de-ringed cafe still
  `32058bcb`) + `wir-her` = `38ebfd81-9ddb-4b11-b055-b95307d2d5ce` (from her
  anchor `65382e29`) — **PROVEN multi-likeness single-frame generation** via
  `<<<uuid>>>` placeholders (nano_banana_2 / kling3_0); (3) the **LOCKED
  chorus** `render_chorus_v16.sh` (v5..v15 = iteration trail): hero hook
  (ORIGINAL wan2_7 lip-sync clip `491e39d1`) → her puddle reflection
  (`b22edfc6`) → hero → cafe one-take notice (`c1ffc156` @1.0s) → composited
  POV reflection reveal (insert `6b3be8f1` @55% over empty plate `ec557078`,
  setpts-fixed) → same-take turn (@6.9s); (4) **PRODUCTION_PLAYBOOK.md** — the
  canonized method: spec-first staging (`CAFE_SCENE_SPEC.md` template),
  body-state law (his body in ONE take per setup), measured cuts via
  `video_analysis` timestamps, POV insert grammar, environment-mirrored
  reflections, surgical nano "ONE change only" edits, true ffmpeg composites
  (empty plate + GHOST_OPACITY, setpts both layers), wan2_7 lip-sync via
  IMPORTED media (NOT job ids — **P-017's mechanism question CLOSED: PROVEN**),
  vocal relay git → raw.githubusercontent → media_import_url, CI delivery
  (`.github/workflows/render-chorus.yml` renders + commits the mp4). Character
  bible hard rules: HIM buzz cut FULL hairline reddish stubble fit lean, BARE
  HANDS no ring (single, post-breakup); HER = his ex, pale, long dark wavy
  hair, oblique/reflections ONLY; NO text in any frame. **Proof = user eyeball
  verdicts on CI-rendered mp4s** (chorus_v12..v16 committed) — no formal
  qa/reviewer pass; ≤2-commit contract superseded by user direction (accepted
  process deviation, recorded). **User verdicts on record:** original hero clip
  is THE hero (never replace); v14-style environment-mirrored reflection
  preferred; composited v15/v16 ghost is the standard; likeness ALWAYS beats
  scene-cohesion. Receipt `build-os/receipts/P-018.md`.
- **Last closed packet (prior):** **P-017 — Higgsfield-native lip-sync pipeline (CODE
  ONLY)** — build (a coded pipeline under `when-it-rains/`; zero credits, zero
  Higgsfield calls, zero network in the default path), route orchestrator →
  builder → qa → reviewer → archivist. Commits **`8dd6c41`** (Commit-1:
  `scripts/slice_vocals.py` + the durable committed `analysis/line_map.json`
  [43 lyric lines, **27 in-scope**, embedding the 3 in-scope still job_ids for
  `PERF_hook` / `PERF_lookup` / `PERF_window`] + `scripts/test_slice_vocals.py`;
  4 files / 1215 ins; **green in isolation 23/0/4** — driver/swap checks SKIP,
  added in Commit 2) + **`eed8ed8`** (Commit-2 tip: `scripts/lipsync_driver.py`
  [the gated wan2_7 audio-driven call-plan — **DRY-RUN default = zero network**;
  `--go` refuses by `SystemExit`, spends nothing without a human `--go` + the
  live MCP; path-b mint+Mac-PUT+confirm or path-c web-app upload; emits
  `upload_segments.sh`] + `scripts/swap_lipsync_clips.py` [NON-DESTRUCTIVE:
  backs up `edl.csv` → `edl_pre_lipsync_backup.csv`, repoints only the in-scope
  cuts] + driver/swap checks now active; 3 files / 438 ins), base **`60b297d`**.
  `git diff --stat 60b297d..eed8ed8` = **6 files, +1653**. **qa GREEN:** suite
  **42/42/0** (full-slice branch executed); zero-network dry-run BOTH paths,
  `--go` refused; non-destructive swap with `preflight_edl` **PASS before AND
  after**; **Commit-1 green in isolation 23/0/4**; safety grep clean — no
  secrets, `song.mp3` gitignored, `audio_segments/` gitignored, `data/` empty of
  generated artifacts. **reviewer PASS** — gated-generation safety airtight, no
  hardcoded md5, reversible swap, honest about the assumed wan2_7
  `audio_references` shape, trajectory low-risk; **Codex UNAVAILABLE — reviewer
  ran SOLO**. Receipt `build-os/receipts/P-017.md`.
  **HONEST STATUS (critical):** the P-017 CODE is correct and **shelved-ready**,
  but the underlying **wan2_7 audio-driven lip-sync MECHANISM is UNPROVEN and SO
  FAR FAILING** — **3 wan2_7 render attempts FAILED outright** (inputs resolve:
  `start_image` + audio attach, but generation dies; tried durations 8/5/5 and
  long+short TTS audio); a **4th** attempt using `media_import_url`'d media_ids
  (image `686b2b8a`, audio `720e0e5a`) was **in flight at close**. If it also
  fails, the finding is: wan2_7 does not reliably produce audio-driven lip-sync
  for our stylized dark performance stills, and true lip-sync likely needs
  **filmed performance footage** (graded + intercut). The code is correct
  regardless; only the mechanism is unproven.
- **P-016 — director's cut, late-90s / 2000s aesthetic (RECEIPT DEBT CLEARED
  this close).** Commit **`60b297d`** (also P-017's base) — a full creative
  re-edit **replacing the 70s rough cut**: **24 new reference-anchored Higgsfield
  clips** (artist as buzz-cut / fit / soaked 2000s frontman + a consistent memory
  woman + atmosphere; bleach-bypass look; **~198 credits**), deterministically
  sequenced by `scripts/build_edit_v2.py` to the lyrics + beat grid into
  `data/edl.csv` = **107 cuts, 274.00 s, no clip repeating within an 8-cut
  window** (fixes the old C02-×11 recycling). **preflight PASS, 0 critical, 0
  warnings.** The **old 70s edit is preserved** as `data/{edl,clips,stills}.70s.csv`;
  `TREATMENT.md` is the director's treatment; frontman likeness corrected across
  3 anchor iterations (canonical still `00d037d0`). Verify via Higgsfield
  `video_analysis` (8 character clips on-model). **Caveats:** a few perf clips
  read "shaved" not "buzzed" (possible re-roll); AI lip-sync not frame-accurate
  (the motivation for P-017). Preceding commits this session (context): `3b4bc4d`
  (render_master verify fix) + `0320218` (treatment v1). Receipt
  `build-os/receipts/P-016.md`.
- **The live / authoritative edit is now the P-016 107-cut / 274.00 s 2000s
  director's cut** (`data/edl.csv`) — NOT the old 86-cut. The **24-clip 2000s
  asset library** lives in `data/clips.csv` (durable) with the 70s library kept as
  `data/clips.70s.csv`. **Render pipeline:** `scripts/render_master.sh`
  (validate → fetch → assemble → verify) gated on `scripts/preflight_edl.py`;
  `scripts/build_edit_v2.py` is the deterministic sequencer. **Lip-sync pipeline
  code (P-017) is shelved** pending wan2_7 validation (above).
- **Last closed packet (prior):** **P-015 — beat-lock analysis + gated beat-aware EDL
  variant** — build (in-session audio analysis + a NON-DESTRUCTIVE derived data
  artifact under `when-it-rains/`), route builder → qa → reviewer → archivist.
  Commits **`c65748e`** (Commit-1: `scripts/beat_lock.py` + `scripts/test_beat_lock.py`
  [20-check suite] + `analysis/beats.json` + `analysis/beat_vs_cut.md`; **4 files,
  1181 ins**, green in isolation) + **`9370af3`** (Commit-2 tip: `data/edl_beatlocked.csv`;
  **1 file, 87 ins**), base **`9ba310b`**. Decoded `when-it-rains/song.mp3` via the
  bundled `imageio_ffmpeg`, built a **uniform beat grid** at the `song.json` period
  (**61.5234375 BPM / 0.9752381 s**) **phase-locked to onset-envelope energy** (method
  `librosa_onset_phase_grid`; librosa 0.11.0's raw ~184.6 BPM 3×-subdivision kept only
  as labeled corroboration, **NOT** used for snapping). Produced the durable map
  `analysis/beats.json` (survives the gitignored `song.mp3` disappearing), the
  diagnostic `analysis/beat_vs_cut.md` over the live 86-cut edit, and the **gated,
  non-destructive** variant `data/edl_beatlocked.csv`. **qa GREEN 8/8** (suite **20/20**):
  **NON-DESTRUCTIVE INVARIANT HELD** — `git diff 9ba310b..9370af3` **EMPTY** for
  `data/edl.csv` / `clips.csv` / `stills.csv` / `assets.json` / `scripts/preflight_edl.py`
  / `scripts/render_master.sh`; `--stat` = **5 files, 1268 ins, 0 modifications**.
  **Variant integrity:** 86 rows + header (schema == `edl.csv`); **11 sections, all
  START times identical to live**; total **274.0 s**; **0 over-reads / 0 unresolved
  clip_keys / 0 back-to-back adjacency**; **84/86 cuts snapped**. **Determinism:**
  `beats.json` md5 `5fcf02866956d60c4bcb321f3a3cecb4`, `edl_beatlocked.csv` md5
  `876b38a640cfb787d0c647b7fd8f7bc1`, `beat_vs_cut.md` md5 `1a8e06484da640688de9ea1874175efd`
  — identical across 2 regens and == committed. **Commit-1 green in isolation** (throwaway
  worktree @ `c65748e` with `song.mp3` present: variant absent, `--analyze-only` regenerates
  `beats.json` byte-identically, `edl.csv` byte-identical, suite 20/20). `preflight_edl.py`
  (live `edl.csv`) still **RESULT: PASS, exit 0, 0 critical**. **Safety grep clean**
  (`subprocess` = bundled ffmpeg decode + self-invocation only; `os.remove` = variant
  file only; no secrets/network/destructive ops; `song.mp3` NOT committed [gitignored],
  `beats.json` IS tracked). **reviewer PASS** — non-destructive invariant confirmed,
  variant integrity + determinism independently checked, honest framing (beats not
  downbeats; librosa raw corroboration-only) accurate, scope airtight; **Codex UNAVAILABLE
  — reviewer ran SOLO** (single-reviewer). Receipt `build-os/receipts/P-015.md`.
  **Alignment gain (informational, only if promoted):** cuts within ±50 ms of a beat
  **8.1 % → 84.9 %**; mean `|offset|` **256.0 ms → 52.7 ms**; median **250.5 ms → 3.0 ms**.
  **Caveats:** downbeat-phase confidence LOW (best 4/4 phase ≈ 720 ms mean section-start
  error) → the variant snaps to **BEATS, not downbeats** (downbeat times in `beats.json`
  advisory only); one residual ~836 ms offset = the final cut end pinned by the 274.0 total
  + preserve-section-start constraints (intentional); Commit-1 isolation is
  **environment-dependent** — a bare checkout WITHOUT the gitignored `song.mp3` cannot
  regenerate (`FileNotFoundError`), by design (`beats.json` is the durable artifact — anyone
  re-running the suite needs `song.mp3` re-attached in `when-it-rains/`).
- **Render pipeline (recorded now — was unreceipted before P-015 close):** two commits
  landed this session as the shipped render pipeline (NOT their own packet): **`82ac71e`**
  — `scripts/render_master.sh`, a one-shot `validate → fetch → assemble → verify` wrapper
  (131 ins); **`9ba310b`** — `scripts/preflight_edl.py`, an offline render-readiness
  validator, + `render_master.sh` gated on it (113 ins / 2 files; `9ba310b` is also
  P-015's base). The **86-cut / 274.0 s live edit** (`data/edl.csv`) is
  **validated render-ready** (`preflight_edl.py` 0-critical).
- **Last closed packet (prior):** **P-014 — stills-catalog backfill (manifest now
  truthful)** — marketing-media (data / catalog edit on `when-it-rains/data/` +
  the inline manifest; user explicitly authorized — "yes do it"), route
  builder → reviewer → qa → archivist. Commits **`6005114`** (`stills.csv` **+11
  regen stills / −4 off-model**, net **+7 → 59 rows**; `clips.csv` **C04
  `source_still` `regenA1` → `2d0ba697`**, a single 1-line change with the other 35
  clip rows byte-identical; `assets.json` stills **52 → 59** + C04 + `counts.stills`
  59) + **`2223893`** (`HANDOFF.md` stills **52 → 59**), base **`00af4e3`**. The
  audit (D5-M3) found 10 reference-anchored regen stills generated on Higgsfield but
  never cataloged, C04's `source_still` a `regenA1` placeholder, and 4 superseded
  off-model stills lingering. P-014 retrieved the 11 stills' UUIDs / URLs **READ-ONLY
  from Higgsfield (no credits)**; **C04 → `2d0ba697` CONFIRMED** via the clip's
  `start_image` (job `297449bf` `medias.start_image` == `2d0ba697`; still ts 012553
  precedes clip ts 012654); added the 11 to `stills.csv` + `assets.json`; pruned the 4
  off-model (`22e02845` / `b0f3fd47` / `26443c5f` / `ff3797c3`); fixed counts.
  **Result: 34 / 36 clip `source_still`s now resolve (all C01–C34); only EX1 / EX2
  `'prior'` remain intentionally unresolved (a prior project — benign).** **qa GREEN
  9/9 + Commit-1 isolation** (stills.csv 59 rows × 3 cols clean; 11 present / 4 absent;
  clips.csv C04-only 1-line change, 35 others byte-identical; assets.json valid, stills
  59 / counts.stills 59 / C04 `2d0ba697` / parity all 36 / edl 86; 34/36 resolve;
  HANDOFF 59; safety clean). **reviewer PASS** — surgically exact (net +7, zero in-place
  mutations), C04 → `2d0ba697` corroborated, parity preserved, closes D5-M3 truthfully,
  no overreach; **Codex UNAVAILABLE** (single-reviewer); non-defect caveat — CloudFront
  URLs not live-hit (egress 403, expected — URLs came from the read-only Higgsfield
  source with the UUID embedded). Receipt `build-os/receipts/P-014.md`. **The stills
  catalog is now truthful — fully consistent with the live assets (59 stills; 34/36
  source_stills resolve); AUDIT-001 D5-M3 RESOLVED.**
- **Last closed packet (prior):** **P-013 — audit doc-coherence fix** —
  marketing-media (docs-consistency on `when-it-rains/README.md` +
  `when-it-rains/EDIT_MAP.md`; **no generation, no source-CSV / functional
  change**), route builder → reviewer → qa → archivist. Commits **`8981252`**
  (README.md — runtime 4:36→4:34/274; clips.csv schema column order fixed to
  the real `mp4_url`/`section` header; stills.csv schema fixed — phantom
  `beat`/`on_model` removed; overhang 2s→0.25s; 8 ins / 8 del) +
  **`0c88c54`** (EDIT_MAP.md — runtime→274/4:34; authority banner — `data/edl.csv`
  authoritative; 11 confirmed section starts; C25–C34 registry added; EX2 marked
  unused; 50 ins / 16 del), base **`1f5211f`**. **qa GREEN 9/9 + Commit-1
  isolation** (both files at 86/274/4:34; the two schema lines match the actual
  CSV headers byte-for-byte; section starts verified vs `edl.csv`; C25–C34 +
  EX2-unused present; narrative preserved; safety clean). **reviewer PASS** —
  every number verified vs live data; no overreach (the stills backfill was
  correctly NOT done — declined-P-010 territory); **Codex UNAVAILABLE**
  (single-reviewer). Receipt `build-os/receipts/P-013.md`. **Both project docs
  (README + EDIT_MAP) are now coherent with the 86/274 edit.**
- **System audit AUDIT-001 complete: ALIGNED to canonical** (zero structural /
  functional / process defects; doc / catalog drift only). 6 parallel auditors
  (D1–D6, read-only) vs a pinned canonical target — D1 engine fidelity ALIGNED
  (vendored `.claude/` byte-identical to source), D2 source coherence ALIGNED,
  D3 process fidelity PASS (all 11 closed packets have receipts; P-010 a proper
  DECLINE; qa/reviewer gate every close), D4 creative ALIGNED, D5 data substantially
  ALIGNED (counts agree everywhere, 0 functional EDL orphans), D6 music ALIGNED
  (~0.25s tail). P-013 closed the auto-fixable doc-coherence findings. Receipt
  `build-os/receipts/AUDIT-001.md`.
- **Last closed packet (prior):** **P-012 — RENDER_REVIEW.md refreshed to 86/274** —
  marketing-media (docs-consistency on `when-it-rains/RENDER_REVIEW.md`; **no
  generation, no source-CSV / functional change**), route builder → reviewer → qa
  → archivist. Commit **`59baa8b`** (base **`25a6a7f`**): `RENDER_REVIEW.md`
  rewritten — the **86-row per-cut table re-derived from `data/edl.csv`**
  (timecodes to **274.0s**, cut 86 = **4:34.0**), header → **86 / 274 / 4:34**,
  watch-points refreshed (band coverage C25–C34 added, C27/C33 on-model confirmed,
  section times marked CONFIRMED), a `preview.html` pointer added, and the stale
  **76 / 276 / 4:36** figures **demoted to explicit history** (not silently
  deleted). One file, **213 ins / 164 del**. **qa GREEN — 8/8 + Commit-1
  isolation**: table independently re-derived from `edl.csv` (**86/86 rows, 0
  timecode mismatches**, total **274.0**, cut 86 **4:34.0**); **zero** stale
  76/276/4:36 current-claims; **C02 11× band-coverage indices** verified; section
  starts consistent; Commit-1 isolation; safety clean. **reviewer PASS** — every
  timecode reproducible to the hundredth; watch-points truthful (C27/C33 faithfully
  reproduces P-008's `video_analysis`-confirmed on-model nuance; the FINAL ~0.25s
  tail arithmetically grounded; stale 76/276/2s demoted to explicit history, not
  silently deleted); usability of the review instrument preserved; scope clean.
  **Codex second-eyes UNAVAILABLE** (single-reviewer). Receipt
  `build-os/receipts/P-012.md`. **Both review instruments are now current at
  86/274** — `preview.html` (silent browser pass) + `RENDER_REVIEW.md` (audio-render
  checklist).
- **Last closed packet (prior):** **P-011 — browser preview tool (`preview.html`)** —
  build (read-only media-data input → HTML artifact; no generation, no source-CSV
  change), route builder → reviewer → qa → archivist. Commits **`645df31`**
  (`scripts/build_preview.py` — deterministic generator + embedded self-test, 700
  ins) + **`a4266c5`** (`preview.html` — self-contained 86-cut browser review
  tool, 1498 ins), base **`46adfc0`**. `build_preview.py` reads `data/edl.csv` +
  `data/clips.csv`, joins `clip_key → mp4_url`, and emits a **self-contained**
  `when-it-rains/preview.html` that plays all **86** EDL cuts in order, streaming
  the clip mp4s from the Higgsfield CDN. Per-cut overlay (n/86, section, cumulative
  timecode, clip, note); **C25–C34** highlighted + **C27/C33** badged on-model;
  per-cut PASS/FAIL + note marking (localStorage + export mirroring
  `RENDER_REVIEW.md`); play/pause/prev/next + click-to-jump list; graceful
  per-clip failure; a clear SILENT / approximate-timing banner naming the Mac
  render path. **qa GREEN — 10/10 + Commit-1 isolation**: 86 cuts in EDL order;
  all mp4_urls + notes verbatim from CSVs; timecodes monotonic ending **274.0**;
  new/on-model flags correct; self-contained (no external script/link/@import);
  deterministic (byte-identical re-runs; Commit-1 `645df31` regenerates the
  artifact identically); safety clean. **reviewer PASS** — generator deterministic,
  playback engine has no stall/double-advance bug (all paths traced; failed clips
  degrade not hang), self-contained + honest banner + XSS-safe, scope airtight.
  **Codex second-eyes UNAVAILABLE** (single-reviewer); the live play-test is the
  **user's** (CDN egress-blocked here). Receipt `build-os/receipts/P-011.md`.
  (Prior: **P-009 — assets.json reconciled to clips.csv** —
  marketing-media (manifest / docs-consistency sub-scope on
  `when-it-rains/data/assets.json`; **no generation, no CSV functional change**),
  route builder → reviewer → qa → archivist. Commit **`f59829b`** (base
  **`cb7610b`**): updated the **11 stale clip entries**
  (**C01, C04, C06, C07, C13, C15, C16, C19, C22, C23, C24**) in
  `data/assets.json` — `job_id` / `source_still` / `mp4_url` — to match the fixed
  `data/clips.csv` (the source of truth the render reads). One file, **33 ins /
  33 del**, one commit. qa GREEN 8/8 + Commit-1 isolation; reviewer PASS; the
  `source_still`↔`stills.csv` non-resolution is a **PRE-EXISTING id-format quirk**
  (clips.csv 8-char prefixes vs stills.csv full UUIDs) affecting all 36 clips both
  BEFORE and AFTER P-009 — NOT a P-009 defect (re-characterized as optional
  **P-010**). Receipt `build-os/receipts/P-009.md`.
  **P-008 — docs/manifest refresh + on-model verified** — marketing-media
  (docs-consistency on `when-it-rains/**`, no CSV change), commits **`71bf753`** +
  **`a07c5a0`** (base **`2925961`**): assets.json counts → **36/52/86**, runtime
  **274/"4:34"**, clips/stills arrays **+10 (C25–C34)**, inline `edl` array rebuilt
  to **86 == data/edl.csv**; `fetch_assets.sh` comment-only; `HANDOFF.md`
  refreshed. qa GREEN 10/10, reviewer PASS; receipt `build-os/receipts/P-008.md`.
  **On-model CONFIRMED:** C27 + C33 both verified **ON-MODEL** via Higgsfield
  `video_analysis` (short reddish/ginger hair + beard, NOT bald) — the
  reference-anchoring bald-fix held; **CLOSES the open on-model item from P-006**
  (no C27/C33 regen needed).
  **P-007 — band-coverage inserted + PRE2/CH1 re-timed** — commit
  **`1969435`** (base `ed046b5`): `scripts/insert_band_coverage.py` regenerated
  `data/edl.csv` to **86 cuts**, added `data/edl_pre_bandcoverage_backup.csv`,
  wrote **+10 rows each** into `clips.csv` / `stills.csv` (C25–C34); **PRE2 6→12 /
  41.00s**, **CH1 8→12 / 38.75s**, ~3.3s avg, total **274.0s**, all 12 section
  starts unchanged, no two new cuts back-to-back; qa GREEN 13/13, reviewer PASS,
  fully reversible; receipt `build-os/receipts/P-007.md`. **P-006 — band-coverage
  clips generated (C25–C34)** ~90 credits, balance ≈ 2,415.5, asset map in
  `build-os/receipts/P-006.md`; **P-005** — add-cuts plan; **P-004** — EDL
  section-sync; **P-003** — SECTION_TIMES.md; **P-002** — RENDER_REVIEW.md; **P-001**
  — Install Build OS. P-004's confirmed times stand: CH1 = 1:29 (89.25s),
  PRE1 = 1:09.75, V2 = 41.25, V4 = 144.5, PRE2 = 173.)
- **Now:** **P-024 is CLOSED → the film's first 89.8 seconds are DELIVERED at
  SHIP quality** — `first90.mp4` (frame-exact, July Reverb bed) containing the
  LOCKED intro_v6 (0–24), V1/V2, and PRE1, with the LOCKED chorus_v16 (CH1
  89.8–102) next downstream. Working branch
  `claude/when-it-rains-handoff-l0u075`; CI relay branch-agnostic;
  push-trigger via `render_request.txt` + nonce; sandbox eyes for all frame QC.
  Credits **1371.75 of 2415** (P-024 cost ~34 vs 150–200 est — well under).
  Read `when-it-rains/HANDOFF.md` (P-024 addendum FIRST), `DIRECTORS_NOTES.md`,
  `PRODUCTION_PLAYBOOK.md`, `ROADMAP.md` before any new packet. Standing user
  law: **no bare chest, ever**. **The ROADMAP back-half clock is VERIFIED
  WRONG — do NOT generate against it until P-025 re-times it.**
- **Next:** **PAPER PACKET P-025 — re-time ROADMAP to the verified section
  clock + write the APPARITION LEGIBILITY STANDARD + add the waterfront-photo
  plant to V3/V4** (DIRECTORS_NOTES.md must-fix #1/#2 + STRUCTURAL; verified
  clock table in its addendum — CH1 really 89.8–132.7, FINAL only 16.2s). Zero
  generation. The media packet formerly numbered P-025 in the old roadmap
  numbering shifts after it. Then the re-timed ladder: CH1-extension plan
  (102–132.7) → V3/V4 → PRE2 → CH2 → BRIDGE → FINAL → full assembly.
## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section, **PLUS
  the P-006 band-coverage batch: 10 new stills + 10 new clips (C25–C34)**, now
  **written into `data/`** by P-007. So `data/clips.csv` = 36 clip rows and
  `data/stills.csv` = **59 still rows** (52 after P-007; **P-014 backfilled +11
  regen stills and pruned −4 off-model → net +7 = 59**; IDs + CDN URLs; full P-006
  map + prompt/recipe in `build-os/receipts/P-006.md`). **P-008** reconciled the
  documentation / manifest layer to match: `data/assets.json` counts block =
  **36 / 52 / 86** at the time (**P-014 advanced stills 52 → 59**), runtime
  **274 / "4:34"**, clips & stills arrays carry C25–C34, and its inline `edl` array
  == `data/edl.csv` row-for-row. **P-009** then reconciled `assets.json`'s
  **pre-existing** clip entries for the 11 earlier-regenerated clips (job_id /
  source_still / mp4_url) to `clips.csv` — so the manifest fully matches the
  functional CSVs (the render reads the CSVs, not `assets.json`). **P-014 then made
  the stills catalog itself truthful** (AUDIT-001 D5-M3): the 10 reference-anchored
  regen stills generated on Higgsfield but never cataloged are now in `stills.csv` +
  `assets.json`, C04's `source_still` is resolved from the `regenA1` placeholder to
  its real still `2d0ba697` (CONFIRMED via the clip's `start_image`, job
  `297449bf`), and 4 superseded off-model stills (`22e02845` / `b0f3fd47` /
  `26443c5f` / `ff3797c3`) are pruned. **34 / 36** clip `source_still`s now resolve
  (all C01–C34); only **EX1 / EX2 `'prior'`** stay unresolved — they point at a
  **prior project** (intentional / benign / accepted, NOT an open gap).
- **Review instruments (both CURRENT at 86/274):**
  `when-it-rains/preview.html` (P-011, generated by `scripts/build_preview.py` from
  `edl.csv` + `clips.csv`) is a **self-contained** browser tool that plays all
  **86** cuts in EDL order, streaming the clip mp4s from the Higgsfield CDN —
  silent + approximate-timing; per-cut overlay, C25–C34/C27-C33 flags,
  click-to-jump, per-cut PASS/FAIL+note (localStorage + export); deterministic
  generator (byte-identical re-runs). `when-it-rains/RENDER_REVIEW.md` (P-002
  instrument, **refreshed to 86/274 by P-012**) is the structured timecode-keyed
  capture checklist for the **full Mac audio render** — 86-row per-cut table
  derived from `data/edl.csv` (274.0s, cut 86 = 4:34.0), watch-points current
  (band coverage, on-model confirmed, section times confirmed). Neither replaces
  the high-fidelity Mac render; both are review aids.
- **Edit kit:** `data/edl.csv` = **86 cuts, total 274.0s** (resolves on the
  Jun-27 mix end). It is section-synced to the confirmed section times (P-004)
  AND has the band-coverage inserted with PRE2/CH1 re-timed to ~3.3s avg (P-007:
  PRE2 41.00s / 12 cuts, CH1 38.75s / 12 cuts). Cut durations span ~1.6–5.0s
  (assembler-compatible; watchable mins 3.11/3.30s). **Reversibility chain:**
  `data/edl_pre_bandcoverage_backup.csv` = byte-exact pre-P-007 (76-cut,
  section-synced 274.0s) EDL; `data/edl_original_backup.csv` = byte-exact
  pre-section-sync (pre-P-004) original 276s EDL — **neither overwritten**.
  Re-timers `scripts/resync_edl.py` and inserter
  `scripts/insert_band_coverage.py` are both deterministic / idempotent. Note:
  the section-sync is coarse — it matches section spans, NOT a sub-beat beat grid.
  **P-015 produced a gated beat-aware alternative** `data/edl_beatlocked.csv` (86
  rows, section starts preserved, 274.0 s, 84/86 cuts snapped to the 0.9752381 s
  grid) — a NON-DESTRUCTIVE variant, NOT applied to `data/edl.csv`; promoting it is
  user-gated. **`scripts/preflight_edl.py`** (offline render-readiness validator,
  landed `9ba310b`) reports the live `edl.csv` **render-ready (0 critical)**, and
  **`scripts/render_master.sh`** (`82ac71e`) is the one-shot validate→fetch→assemble→verify
  wrapper gated on it.
- **Band-coverage plan (P-005, spec):** `when-it-rains/BAND_COVERAGE_PLAN.md`
  specified the 10 new band-only cuts (C25–C30 PRE2, C31–C34 CH1). **GENERATED
  (P-006)** + **INSERTED / re-timed (P-007)** — fully landed.
- **Song analysis (reproducible in-session):** `analyze_song.py` / `song.json` —
  `music_end 273.75`, `duration 284.4`, `tempo 61.5234375` BPM (→ **0.97524s**
  per beat), 12 transitions. The song MP3 has been **re-attached + staged**
  (gitignored) and the analysis re-verified reproducible this session; `numpy` +
  `imageio-ffmpeg` are installed. (The MP3 itself will NOT survive a new session.)
- **Beat-lock capability (P-015):** `scripts/beat_lock.py` (+ 20-check
  `scripts/test_beat_lock.py`) decodes `song.mp3` via the bundled `imageio_ffmpeg`
  and builds a uniform beat grid at the `song.json` period (61.5234375 BPM /
  0.9752381 s) **phase-locked to onset-envelope energy** (method
  `librosa_onset_phase_grid`; librosa 0.11.0's raw ~184.6 BPM 3×-subdivision is
  labeled corroboration only, NOT used for snapping). The **durable** artifact is
  `analysis/beats.json` (md5 `5fcf02866956d60c4bcb321f3a3cecb4`) — it survives the
  gitignored `song.mp3` disappearing; `analysis/beat_vs_cut.md` is the diagnostic
  over the live 86-cut edit. The grid snaps to **BEATS, not downbeats** (4/4
  downbeat-phase confidence LOW ≈ 720 ms section-start error — downbeat times in
  `beats.json` are advisory only). Re-running the suite from a bare checkout
  requires `song.mp3` re-attached in `when-it-rains/` (FileNotFoundError otherwise —
  by design; `beats.json` is the durable output).
- **Footage audit + regeneration: DONE.** All 26 clips were inspected via
  Higgsfield server-side `video_analysis` (free, bypasses the CDN block). It
  found the lead rendered **bald/shaved in 22 of 76 cuts** (cool story clips) +
  4 content failures (C06, C07, C22, C23) + an auburn woman (C16). Root cause:
  the man-stills were generated with **no reference image attached**. All **11**
  flagged clips were **regenerated reference-anchored, re-animated, and
  re-analyzed to verify** (anchors `5cc8239a` man / `1143614b` woman); 10 fully
  accepted, C04 partial (hair + reflection fixed, head-turn still absent).
  `data/clips.csv` now points at the fixed clips (originals in
  `data/clips_original_backup.csv`). Spend ~106.5 credits; then ~90 more on P-006
  → **balance ≈ 2,415.5**.
- **Verification caveat:** the fixes were confirmed by **automated re-analysis,
  NOT a human eye** (canary on C13) — a real render is the final confidence check.
  `when-it-rains/RENDER_REVIEW.md` (P-002, **refreshed to 86/274 by P-012**) is the
  structured instrument for that still-pending human review; `preview.html` (P-011)
  is the silent in-browser pass. **C27 + C33 (the two singer-facing P-006 band
  clips) are CONFIRMED ON-MODEL (P-008)** via Higgsfield `video_analysis` — C27
  "late-30s, fair complexion, very short thinning reddish hair, light beard"; C33
  "mid-30s, freckles, short ginger hair, trimmed ginger beard" (short reddish/ginger
  hair + beard, NOT bald). The reference-anchoring bald-fix held; the C27/C33
  on-model risk from P-006 is **CLOSED** (no regen needed). This is still an
  automated confirmation, not a human eye — the render pass stays the final check.
- **Creative invariants:** the man = fair freckled skin, reddish beard, short
  cropped red-blonde hair with a receding hairline (NOT bald/shaved/buzzed); the
  woman = one brunette, long dark wavy hair, only ever memory/reflection. Look =
  16:9, 35mm grain, 1970s cinematic; performance = warm amber/wood, story = cool
  blue-grey rain. One narrative motion per clip.

---
_Updated by the archivist on close. Seeded from `when-it-rains/HANDOFF.md`,
`FOOTAGE_AUDIT.md`, `README.md`, and `data/` on 2026-06-29. P-001 closed
2026-06-29; P-002 closed 2026-06-29; P-003 closed 2026-06-29; P-004 closed
2026-06-29; P-005 closed 2026-06-29; P-006 closed 2026-06-29; P-007 closed
2026-06-29; P-008 closed 2026-06-29; P-009 closed 2026-06-29; P-011 closed
2026-06-29; P-012 closed 2026-06-29; P-013 closed 2026-06-29 (AUDIT-001
recorded — system ALIGNED to canonical); P-014 closed 2026-06-29 (stills-catalog
backfill — manifest now truthful; AUDIT-001 D5-M3 RESOLVED — stills 52 → 59, 34/36
source_stills resolve); P-015 closed 2026-07-01 (beat-lock analysis + gated
beat-aware EDL variant — `beat_lock.py` + `analysis/beats.json` + `analysis/beat_vs_cut.md`
+ NON-DESTRUCTIVE `data/edl_beatlocked.csv`; live edit byte-untouched, empty diff on
all 6 product surfaces; qa GREEN 8/8 / suite 20/20 / Commit-1 iso in a throwaway
worktree / determinism by md5 / safety clean; reviewer PASS, Codex unavailable — solo;
base `9ba310b`, tip `9370af3`; render pipeline `82ac71e` + `9ba310b` recorded as
shipped; live edit preflight render-ready); P-016 closed 2026-07-01 (director's cut
— late-90s / 2000s bleach-bypass re-edit replacing the 70s cut; 24 new
reference-anchored Higgsfield clips ~198 credits; `build_edit_v2.py` sequenced
`data/edl.csv` = 107 cuts / 274.00 s / no repeat-within-8; preflight PASS 0
warnings; old 70s edit preserved as `data/*.70s.csv`; qa PASS, reviewer PASS —
caveats: a few perf clips "shaved" not "buzzed", AI lip-sync not frame-accurate;
commit `60b297d`; receipt debt cleared this close); P-017 closed 2026-07-01
(Higgsfield-native wan2_7 lip-sync pipeline, CODE ONLY — `slice_vocals.py` +
durable `analysis/line_map.json` + gated `lipsync_driver.py` [DRY-RUN default,
`--go` refuses] + non-destructive `swap_lipsync_clips.py`; qa GREEN suite 42/42/0,
Commit-1 iso 23/0/4, dry-run zero-network both paths, safety clean; reviewer PASS,
Codex unavailable — solo; base `60b297d`, tip `eed8ed8`; HONEST STATUS: code
shelved-ready but wan2_7 mechanism UNPROVEN / SO FAR FAILING [3 attempts failed, a
4th in flight at close] → true lip-sync likely needs filmed footage). The live edit
is now the P-016 107-cut / 274.00 s 2000s director's cut. All of P-016 + P-017
commits + this close are local-only, awaiting an explicit push go. P-018 closed 2026-07-01 (CHORUS LOCK — the
chorus-production era: trained Soul `07822e21`, elements `wir-him` / `wir-her`,
LOCKED `render_chorus_v16.sh` + `PRODUCTION_PLAYBOOK.md` canonized, wan2_7
lip-sync PROVEN via imported media, CI render delivery live; 32 commits
`8a5048c..bc9d4d7` + CI `8a2e88d`, base `90ce268`; proof = user verdicts on
CI-rendered mp4s [accepted process deviation]; NOTE: the branch AUTO-MIRRORS to
origin — the "local-only / awaiting push go" framing above is superseded).
**P-018/P-019 (intro pair) closed 2026-07-02** (INTRO LOCKED — intro_v6
"Amazing"; combined receipt `build-os/receipts/P-018_P-019.md`; id collision
with the chorus-lock P-018 recorded, numbering resumes at P-020; review-fetch
"sandbox eyes" QC path live + playbook laws 0/0b canonized; double-bed canon;
credits ~1700–1800/2415; next: Verse 1 board 23.5–43.0s, kitchen / TWO MUGS)._

_P-020/P-021/P-022 catch-up + P-023 close appended 2026-07-03 by the archivist
(P-023 first70 v2 SHIP — receipt `build-os/receipts/P-023.md`; P-021 receipt
debt recorded; branch now `claude/when-it-rains-handoff-l0u075`; credits
1405.71; next P-024 PRE1)._

_P-024 close appended 2026-07-03 by the archivist (PRE1 SHIP — pre1_v1 19.51s +
first90 89.79s frame-exact on the July Reverb bed, likeness 9/10; new laws:
mix-swap clock verification, frame-exact stitch, wan behavioral pinning,
rotation salvage + explicit kling sound:off; DIRECTORS_NOTES.md committed —
ROADMAP back-half clock verified wrong, re-time staged as PAPER PACKET P-025;
credits 1371.75; receipt `build-os/receipts/P-024.md`)._
