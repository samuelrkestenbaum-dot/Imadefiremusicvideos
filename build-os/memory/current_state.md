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

- **Last closed packet:** **P-004 — EDL section-sync to confirmed times**
  (`when-it-rains/data/edl.csv` rewrite) (qa GREEN 10/10 + Commit-1 isolation,
  reviewer PASS; receipt `build-os/receipts/P-004.md`; commits `0ac19d2` script +
  `72dff55` artifacts, base `bbcc36f`, not pushed). The user **CONFIRMED** the
  P-003 section times ("those look good, keep going") — **CH1 downbeat = 1:29
  (89.25s)**, PRE1 (settling) = 1:09.75, V2 = 41.25, V4 = 144.5, PRE2 = 173; the 5
  anchored sections unchanged. The new deterministic/idempotent
  `scripts/resync_edl.py` re-timed the 76 cuts so each section's cuts sum to its
  confirmed span; **cumulative section starts now land exactly on the confirmed
  times, total = 274.0s**. The original EDL is backed up byte-exact at
  `data/edl_original_backup.csv` (fully reversible). (P-003 — SECTION_TIMES.md —
  closed before it; P-002 — RENDER_REVIEW.md; P-001 — Install Build OS + seed
  memory — earlier.)
- **Now:** no active build packet — **the section times are CONFIRMED** (CH1 = 1:29
  etc.; the 1:29-vs-1:51 question is settled) and the EDL is **section-synced** to
  them. **Awaiting the user's render-judgment** of the re-timed cut on their Mac
  (`scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`). (Also still open:
  the broader human-eye render review via `RENDER_REVIEW.md`, P-002.)
- **Next:** on the user's render-judgment → **if CH1 / PRE2 drag on playback** (they
  were stretched ×1.55 / ×1.64, so their cuts now hold ~5–6.5s), an **added-cuts
  packet** (band-coverage batch, `RENDER_REVIEW.md` §7) — add cuts rather than hold
  stretched. **Optionally**, sub-beat **beat-grid quantization** (snap to the
  0.97524s grid) — but that needs a rigorous downbeat phase reference and stays
  deferred. Section-sync is reversible via `data/edl_original_backup.csv`.

## Stable facts (slow-changing)

- **Assets generated on Higgsfield:** **42 stills + 26 animated clips** (Kling
  v3.0, silent 5s, start-frame, one motion each) covering every section. IDs +
  CDN URLs live in `when-it-rains/data/clips.csv` (26 clips), `stills.csv` (42
  stills), `assets.json`.
- **Edit kit:** `data/edl.csv` = **76 cuts, now section-synced to the confirmed
  section times, total 274.0s** (resolves on the Jun-27 mix end). The original
  pre-sync EDL (sum 276s, FINAL truncated ~2s) is preserved byte-exact at
  `data/edl_original_backup.csv`; the re-timer is `scripts/resync_edl.py`
  (deterministic / idempotent). Cut durations span ~1.6–8.2s
  (assembler-compatible). Note: the section-sync is coarse — it matches section
  spans, NOT a sub-beat beat grid (that quantization is still deferred).
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
2026-06-29; P-002 closed 2026-06-29; P-003 closed 2026-06-29; P-004 closed
2026-06-29._
