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

- **Last closed packet:** **P-008 — docs/manifest refresh + on-model verified** —
  marketing-media (docs-consistency sub-scope on `when-it-rains/**`; **no
  generation, no CSV / functional change**), route builder → reviewer → qa →
  archivist. Commits **`71bf753`** + **`a07c5a0`** (base **`2925961`**):
  reconciled the documentation / manifest layer to the real pipeline state.
  `71bf753` set `data/assets.json` counts → **36 / 52 / 86**, runtime →
  **274 / "4:34"**, clips array **+10 (C25–C34)**, stills array **+10**, and
  **rebuilt the inline `edl` array to 86 rows == `data/edl.csv`** (row-for-row);
  `fetch_assets.sh` comment-only (26→36 / 42→52, zero logic change). `a07c5a0`
  refreshed `HANDOFF.md` to the 86-cut/274s/band-coverage state (old numbers only
  as historical "(was…)"). **qa GREEN — 10/10**: all 9 counts reconcile
  (CSV == counts-block == array-lengths = 36/52/86); runtime 274/"4:34" (edl sums
  274.0); C25–C34 + 10 new stills match the registries; inline edl array matches
  `edl.csv` row-for-row; `fetch_assets.sh` comment-only; HANDOFF stale numbers
  only as "(was…)"; Commit-1 isolation; safety clean. **reviewer PASS** — zero
  functional change confirmed (render reads the CSVs, not `assets.json`); manifest
  accurate; HANDOFF truthful/resumable; **Codex second-eyes UNAVAILABLE**,
  single-reviewer. Receipt `build-os/receipts/P-008.md`.
  **On-model: CONFIRMED.** C27 (singer profile) + C33 (chorus CU) both verified
  **ON-MODEL** via Higgsfield `video_analysis` (C27 "late-30s, fair complexion,
  very short thinning reddish hair, light beard"; C33 "mid-30s, freckles, short
  ginger hair, trimmed ginger beard") — short reddish/ginger hair + beard, NOT
  bald. The reference-anchoring bald-fix **held**; this **CLOSES the open on-model
  item from P-006** (no C27/C33 regen needed).
  (Prior: **P-007 — band-coverage inserted + PRE2/CH1 re-timed** — commit
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
- **Now:** the **repo is COHERENT** — docs/manifests now match the real
  **86-cut / 274.0s** pipeline (**36 clips / 52 stills**), and the **C27/C33
  on-model risk is CLOSED** (verified on-model). The edit + manifest are
  **render-ready**. Reversibility chain intact:
  `edl_pre_bandcoverage_backup.csv` (pre-band) → `edl_original_backup.csv`
  (pre-section-sync), neither overwritten. **P-009 in flight** — reconcile
  `assets.json`'s **pre-existing** regenerated-clip rows (the 11 earlier-regen
  clips still carry pre-regen job_ids/urls, diverging from the fixed `clips.csv`;
  non-functional manifest drift). The **only remaining real work is the user's
  render-review**.
- **Next:** finish **P-009** (manifest reconcile of the pre-existing clip/still
  entries to `clips.csv` / `stills.csv`), then the **user renders + judges** the
  cut — `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
  `when-it-rains/RENDER_REVIEW.md` (overall pacing judgment; C27/C33 on-model is
  now resolved, no longer a spot-check item). Optional later: **sub-beat
  beat-grid quantization** to the 0.97524s grid (needs a rigorous downbeat phase
  reference), and **selective 2K/4K upscale** (explicitly LAST, after the cut is
  locked).

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section, **PLUS
  the P-006 band-coverage batch: 10 new stills + 10 new clips (C25–C34)**, now
  **written into `data/`** by P-007. So `data/clips.csv` = 36 clip rows and
  `data/stills.csv` = 52 still rows (IDs + CDN URLs; full P-006 map +
  prompt/recipe in `build-os/receipts/P-006.md`). **P-008** reconciled the
  documentation / manifest layer to match: `data/assets.json` counts block =
  **36 / 52 / 86**, runtime **274 / "4:34"**, clips & stills arrays carry C25–C34,
  and its inline `edl` array == `data/edl.csv` row-for-row. (NOTE: `assets.json`'s
  **pre-existing** clip/still entries for the 11 earlier-regenerated clips still
  carry pre-regen job_ids/urls — a non-functional manifest drift **P-009**
  reconciles; the render reads the CSVs, not `assets.json`.)
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
  `when-it-rains/RENDER_REVIEW.md` (P-002) is the structured instrument for that
  still-pending human review. **C27 + C33 (the two singer-facing P-006 band clips)
  are now CONFIRMED ON-MODEL (P-008)** via Higgsfield `video_analysis` — C27
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
2026-06-29; P-008 closed 2026-06-29._
