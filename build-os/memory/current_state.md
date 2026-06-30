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

- **Last closed packet:** **P-012 — RENDER_REVIEW.md refreshed to 86/274** —
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
- **Now:** **P-012 is CLOSED** — `when-it-rains/RENDER_REVIEW.md` is refreshed to
  the current **86-cut / 274.0s** edit (was STALE at 76/276/4:36). **Both review
  instruments are now current:** `preview.html` (P-011, silent in-browser pass) +
  `RENDER_REVIEW.md` (P-012, audio-render timecode checklist), both at **86 cuts /
  274.0s**. **The repo is fully coherent** — docs/manifests match the real
  **86-cut / 274.0s** pipeline (**36 clips / 52 stills**; C27/C33 on-model CLOSED;
  reversibility chain intact: `edl_pre_bandcoverage_backup.csv` →
  `edl_original_backup.csv`, neither overwritten). **The ONLY open work is the
  user's render-review** — the interactive preview AND/OR a full Mac audio render.
  (Optional later, POST-APPROVAL only: sub-beat beat-grid quantization; selective
  2K/4K upscale. **P-010** — stills backfill of the pre-existing 8-char-prefix ↔
  full-UUID source_still gap — is non-functional, **declined by the user**, needs a
  fresh go.)
- **Next:** the **user reviews + judges** the cut — either open
  `when-it-rains/preview.html` in a browser (silent, approximate-timing, streams
  from the CDN) and/or run the full Mac audio render (`scripts/fetch_assets.sh` →
  `scripts/assemble_rough_cut.sh`) with `RENDER_REVIEW.md` (now refreshed to
  86/274) as the timecode-keyed capture checklist, for overall pacing judgment
  (C27/C33 on-model is resolved, no longer a spot-check item). Optional later,
  post-approval: **sub-beat beat-grid quantization** to the 0.97524s grid (needs a
  rigorous downbeat phase reference) and **selective 2K/4K upscale** (explicitly
  LAST, after the cut is locked). **P-010** (stills backfill — pre-existing
  id-format gap, non-functional, declined) needs a fresh go if revisited.

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section, **PLUS
  the P-006 band-coverage batch: 10 new stills + 10 new clips (C25–C34)**, now
  **written into `data/`** by P-007. So `data/clips.csv` = 36 clip rows and
  `data/stills.csv` = 52 still rows (IDs + CDN URLs; full P-006 map +
  prompt/recipe in `build-os/receipts/P-006.md`). **P-008** reconciled the
  documentation / manifest layer to match: `data/assets.json` counts block =
  **36 / 52 / 86**, runtime **274 / "4:34"**, clips & stills arrays carry C25–C34,
  and its inline `edl` array == `data/edl.csv` row-for-row. **P-009** then
  reconciled `assets.json`'s **pre-existing** clip entries for the 11
  earlier-regenerated clips (job_id / source_still / mp4_url) to `clips.csv` —
  so the manifest now **fully matches** the functional CSVs (the non-functional
  drift is RESOLVED; the render reads the CSVs, not `assets.json`). Residual: the
  `source_still`↔`stills.csv` id-format quirk (8-char prefixes vs full UUIDs,
  pre-existing, non-functional) is now optional **P-010** (declined by user).
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
  the section-sync is coarse — it matches section spans, NOT a sub-beat beat grid
  (that quantization is still deferred).
- **Band-coverage plan (P-005, spec):** `when-it-rains/BAND_COVERAGE_PLAN.md`
  specified the 10 new band-only cuts (C25–C30 PRE2, C31–C34 CH1). **GENERATED
  (P-006)** + **INSERTED / re-timed (P-007)** — fully landed.
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
2026-06-29; P-012 closed 2026-06-29._
