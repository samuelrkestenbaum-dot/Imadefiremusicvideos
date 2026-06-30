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

- **Last closed packet:** **P-006 — band-coverage clips generated (C25–C34)** —
  marketing-media generation, executed from the main loop via the Higgsfield MCP
  under the user's **explicit "all at once" go** (the previously-GATED credit
  spend). Generated **10 reference-anchored stills** (`nano_banana_flash`, 16:9,
  1k, all anchored on the C20 on-model frame `5cc8239a`; the 2 singer stills
  C27/C33 also +3 man-selfies) and **animated each** with `kling3_0` (std, sound
  off, 5s, `start_image`). The 6 PRE2 clips (C25–C30) carry
  `declined_preset 24bae836-…` (storm/dark); the 4 CH1 clips (C31–C34) omit it
  (warm). **~90 credits** spent (10 stills ×1.5 + 10 clips ×7.5); **balance ≈
  2,415.5** (ultra plan). Full durable asset map (clip → still_id → job_id →
  mp4_url → section → slot_after_row → target_dur) is in
  `build-os/receipts/P-006.md` (+ non-durable `scratchpad/p006_assets.json`).
  **Verification DEFERRED to the user's render-review:** automated `video_analysis`
  on-model check ERRORED (it needs an imported video id, not a job id), so on-model
  was not auto-confirmed; reference-anchoring (the proven bald-fix) IS confirmed on
  all stills, and C27/C33 (the singer spot-check) were shown to the user. (Prior:
  **P-005 — band-coverage add-cuts plan** `when-it-rains/BAND_COVERAGE_PLAN.md`,
  spec-only, qa GREEN 10/10 + reviewer PASS, receipt `build-os/receipts/P-005.md`,
  commits `cff6043` + `bbd952a`. P-004 — EDL section-sync; P-003 — SECTION_TIMES.md;
  P-002 — RENDER_REVIEW.md; P-001 — Install Build OS — earlier. P-004's confirmed
  times stand: CH1 = 1:29 (89.25s), PRE1 = 1:09.75, V2 = 41.25, V4 = 144.5,
  PRE2 = 173; EDL section-synced, total 274.0s, reversible via
  `data/edl_original_backup.csv`.)
- **Now:** the **10 band-coverage assets are GENERATED + recorded** (C25–C34 on
  Higgsfield's CDN; ids/URLs durable in the P-006 receipt). They are **not yet in
  git** — they enter `data/` only when P-007 splices them. The PRE2 / CH1 drag
  (sections stretched ×1.64 / ×1.55 in P-004, holding ~5–6.5s) now has its footage
  in hand. (Still open from before: the user's render-judgment of the section-synced
  cut + the broader human-eye render review via `RENDER_REVIEW.md`, P-002 — both
  off-machine on the user's Mac; and C27/C33 on-model confirmation at render.)
- **Next:** **P-007 — insert C25–C34 into `data/edl.csv` (+ `clips.csv` /
  `stills.csv`) + re-time PRE2 / CH1 to ~3.3s avg** — **in flight** (GATED edit;
  needs explicit go). Carry the two P-005 notes: keep C26 distinct from C09;
  from repo root use `when-it-rains/data/edl.csv`. (Still deferred, optional:
  sub-beat **beat-grid quantization** to the 0.97524s grid — needs a rigorous
  downbeat phase reference. Section-sync remains reversible via
  `data/edl_original_backup.csv`.)

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section, IDs +
  CDN URLs in `when-it-rains/data/clips.csv` (26 clips), `stills.csv` (42 stills),
  `assets.json`. **PLUS the P-006 band-coverage batch: 10 new stills + 10 new
  clips (C25–C34)**, generated 2026-06-29 and recorded in
  `build-os/receipts/P-006.md` — these are on the CDN but **not yet written into
  `data/`** (that is P-007).
- **Edit kit:** `data/edl.csv` = **76 cuts, now section-synced to the confirmed
  section times, total 274.0s** (resolves on the Jun-27 mix end). The original
  pre-sync EDL (sum 276s, FINAL truncated ~2s) is preserved byte-exact at
  `data/edl_original_backup.csv`; the re-timer is `scripts/resync_edl.py`
  (deterministic / idempotent). Cut durations span ~1.6–8.2s
  (assembler-compatible). Note: the section-sync is coarse — it matches section
  spans, NOT a sub-beat beat grid (that quantization is still deferred).
- **Band-coverage plan (P-005, spec only):** `when-it-rains/BAND_COVERAGE_PLAN.md`
  specifies 10 new band-only cuts (C25–C30 PRE2, C31–C34 CH1) to break the long PRE2
  / CH1 holds — each with a reference-anchored still recipe + Kling clip recipe +
  draft prompt + EDL slot + target duration. **Now GENERATED (P-006)**; **NOT yet
  inserted/re-timed (P-007, gated edit, in flight).**
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
  still-pending human review. (The P-006 band clips are likewise unverified — see
  residue: C27/C33 on-model deferred to render.)
- **Creative invariants:** the man = fair freckled skin, reddish beard, short
  cropped red-blonde hair with a receding hairline (NOT bald/shaved/buzzed); the
  woman = one brunette, long dark wavy hair, only ever memory/reflection. Look =
  16:9, 35mm grain, 1970s cinematic; performance = warm amber/wood, story = cool
  blue-grey rain. One narrative motion per clip.

---
_Updated by the archivist on close. Seeded from `when-it-rains/HANDOFF.md`,
`FOOTAGE_AUDIT.md`, `README.md`, and `data/` on 2026-06-29. P-001 closed
2026-06-29; P-002 closed 2026-06-29; P-003 closed 2026-06-29; P-004 closed
2026-06-29; P-005 closed 2026-06-29; P-006 closed 2026-06-29._
