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
  ffmpeg. "Proof" for this project = the user eyeballing a real render. There is
  also `when-it-rains/preview.html` (P-011) — a self-contained, browser-playable
  in-browser review aid that streams the 86 clip mp4s from the CDN
  (browser-reachable even though this cloud session's egress is blocked); silent +
  approximate-timing, but it lets the user review the rough cut in a browser
  without the Mac fetch+ffmpeg render.

## Where we are

- **Last closed packet:** **P-015 — beat-lock analysis + gated beat-aware EDL
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
- **Now:** **P-015 is CLOSED → the beat-analysis capability + a gated
  beat-aware EDL variant exist; the live edit is byte-untouched.** `beat_lock.py`
  (+ 20-check suite) decodes `song.mp3` via bundled `imageio_ffmpeg` and produced
  the durable map `analysis/beats.json`, the diagnostic `analysis/beat_vs_cut.md`,
  and the **non-destructive** variant `data/edl_beatlocked.csv` (86 rows, section
  starts preserved, 274.0 s, 84/86 cuts snapped; ±50 ms alignment 8.1 % → 84.9 %
  **if promoted**). The **NON-DESTRUCTIVE INVARIANT HELD** — the live `data/edl.csv`
  + all 5 other product surfaces are byte-identical (empty diff). The render
  pipeline is now also on record: **`82ac71e`** (`scripts/render_master.sh`,
  one-shot validate→fetch→assemble→verify) + **`9ba310b`** (`scripts/preflight_edl.py`,
  offline render-readiness validator, gating render_master) — the **86-cut / 274.0 s
  live edit is validated render-ready** (preflight 0-critical). P-014 + P-013 +
  AUDIT-001 all still stand (stills catalog truthful — 59 stills, 34/36 resolve;
  docs coherent at 86/274; system ALIGNED to canonical). **Both review instruments
  are current** at 86/274: `preview.html` (P-011) + `RENDER_REVIEW.md` (P-012).
  **The ONLY open real work is the user's render-review + judgment** — and, if the
  user likes it, the **user-gated** decision to promote `edl_beatlocked.csv` into
  the live edit. **BLOCKED in-session:** the real footage master cannot render here
  — the Higgsfield CDN (`d8j0ntlcm91z4.cloudfront.net`) is egress-blocked (403, org
  policy); the user must allowlist the host OR run `scripts/render_master.sh` on a
  connected Mac. (Optional later, POST-APPROVAL only: promote the beat-locked
  variant; selective 2K/4K upscale.)
- **Next:** the **user reviews + judges** the cut — either open
  `when-it-rains/preview.html` in a browser (silent, approximate-timing, streams
  from the CDN) and/or run the full Mac render (`scripts/render_master.sh`, or
  `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`) with `RENDER_REVIEW.md`
  as the timecode-keyed capture checklist, for overall pacing judgment. If the
  pacing wants tightening to the beat, the **user-gated** promotion of
  `data/edl_beatlocked.csv` into the live `data/edl.csv` is staged and ready (84/86
  cuts snapped, section starts preserved). Optional later, post-approval:
  **selective 2K/4K upscale** (explicitly LAST, after the cut is locked). NOT YET
  PUSHED: P-015 commits `c65748e` / `9370af3` + this close commit are local-only —
  awaiting an explicit push go.

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
shipped; live edit preflight render-ready; P-015 commits + close are local-only,
awaiting push go)._
