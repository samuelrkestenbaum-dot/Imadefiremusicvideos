# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **PRE2 / CH1 drag — STAGED (P-005) and now GENERATED (P-006); insert pending
  (P-007).** The section-sync stretched **CH1 ×1.55** and **PRE2 ×1.64**, so their
  cuts hold **~5–6.5s and may DRAG**. P-005 spec'd the fix
  (`when-it-rains/BAND_COVERAGE_PLAN.md`: 10 new band-only add-cuts, C25–C30 PRE2 →
  12 cuts @ ~3.4s; C31–C34 CH1 → 12 cuts @ ~3.2s). **P-006 GENERATED all 10** (stills
  + Kling clips, recorded in `build-os/receipts/P-006.md`). One gated packet remains:
  - **P-007 — insert the 10 clips into `data/edl.csv` (+ `clips.csv` / `stills.csv`)
    + re-time PRE2 / CH1 to ~3.3s avg (GATED edit, in flight).** Needs explicit go.
    Ids + mp4 URLs + per-clip `slot_after_row` / `target_dur` are in the P-006
    receipt. The added cuts are the fix — **NOT** stretched holds.
- **P-006 open verification — C27 + C33 (singer-facing) on-model NOT
  auto-verified.** The Higgsfield `video_analysis` on-model check **ERRORED** on
  all 10 — the tool needs an **uploaded/imported video id**, not a generation
  **job id** (importing + a 3–5 min scene analysis per clip was deemed a heavy
  detour and skipped). Reference-anchoring (the proven bald-fix) **IS** confirmed
  applied to all 10 stills, and C27/C33 (the two singer stills, also +3
  man-selfies) were shown to the user — so **risk is low**. **Confirm C27 + C33
  read on-model at the user's render-review** (they are the designated spot-check);
  if either is off-model, **regenerate just those (~10 credits).** This is the one
  open verification item carried out of P-006.
- **P-005 non-blocking generation-time notes (carry into P-007).**
  1. Ensure **C26 (full-band push-in)** reads visually **distinct** from existing
     **C09 (also a push-in)** — avoid a near-duplicate shot.
  2. The plan's relative `data/edl.csv` path is correct **from `when-it-rains/`**;
     whoever runs P-007 **from repo root** must use `when-it-rains/data/edl.csv`.
- **Verify the fast V3 cuts on render (P-004 follow-up).** The section-sync
  compressed **V3 ×0.53**, so its cuts are now **~1.6–2.7s (fast)** — confirm on the
  render they read as energetic, not rushed.
- **Sub-beat beat-grid quantization (still deferred).** Snap the 76 cuts to the
  **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync — but this needs
  a **rigorous downbeat phase reference** and the MP3 re-attached (staged this
  session, won't survive a new one — see risks). P-004 delivered the coarser
  **section-sync** (cuts re-timed to confirmed section spans; cumulative starts exact,
  total 274s), NOT this finer beat quantization.
- **Selective 2K/4K upscale** — explicitly LAST, only after the cut is emotionally
  locked.

## Known risks / debt

- **The section-sync is reversible** — `when-it-rains/data/edl_original_backup.csv`
  is a **byte-exact** backup of the original (pre-P-004) EDL (sha256 `786a51b1…`;
  md5 matches the base file). Restoring it over `data/edl.csv` returns the original
  276s cut byte-for-byte. `scripts/resync_edl.py` is deterministic/idempotent, so the
  synced EDL can also be regenerated exactly from the confirmed times.
- **P-006 assets live only on Higgsfield's CDN + in the P-006 receipt — not in
  git.** The 10 generated stills/clips (C25–C34) enter `data/` only when P-007
  splices them. Until then, the **durable record is `build-os/receipts/P-006.md`**
  (full UUIDs + mp4 URLs). The `scratchpad/p006_assets.json` copy will **NOT
  survive a new session** — rely on the receipt.
- **The song MP3 is NOT in git** — but it has been **re-attached + staged this
  session** (gitignored), and `analyze_song.py` was re-run with the analysis
  verified **reproducible in-session** (`numpy` + `imageio-ffmpeg` installed; the
  in-session audio-analysis capability now exists). However, the raw audio
  (`When_It_Rains__Jun_27_mix.mp3`) lives only in the session's uploads dir and
  will **NOT survive into a new session** — it must be re-attached again before
  any future audio/beat-lock work in a fresh session. The `analysis/` outputs
  (BPM 61.5234375, 0.97524s/beat, `music_end 273.75`, climaxes) are derived and
  stay; the raw audio does not.
- **No render in the cloud env.** The Higgsfield CDN is egress-blocked here and
  there is no system ffmpeg, so the rough cut **cannot be rendered or eyeballed in
  this session** — it MUST be rendered on the user's Mac
  (`scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`). Server-side
  `video_analysis` (free, bypasses the CDN) is the only in-session look at footage
  — **and it only accepts imported video ids, not generation job ids** (this is why
  the P-006 clips could not be auto-checked on-model). The section-synced timing
  (P-004) is therefore **unverified by human eye** until the user renders the
  re-timed cut.
- **Regenerated + newly-generated clips are unverified by human eye.** The 11 P-002-era
  fixes (bald lead / content failures / auburn woman) were confirmed by **automated
  re-analysis** (`video_analysis`, canary on C13), NOT by a human watching playback;
  and the **10 P-006 band clips** were not auto-analyzed at all (only reference-anchoring
  confirmed + C27/C33 shown). A render is the final confidence check. Known-open items
  even after the P-002 fix: C04's head-turn is still absent, and the lead's exact face
  still varies slightly clip-to-clip (anchored, not a trained Soul).
  **`when-it-rains/RENDER_REVIEW.md`** (P-002, closed 2026-06-29) is the structured
  timecode-keyed capture instrument for this still-pending human render review — the gap
  stays open until the user actually renders + reviews (now including C25–C34).
- **Mid-song section starts — now CONFIRMED + applied (resolved).**
  **`when-it-rains/SECTION_TIMES.md`** (P-003) proposed the ambiguous starts; the
  user **CONFIRMED** them ("those look good, keep going") and **P-004 applied them**
  to `data/edl.csv` — **CH1 = 1:29 (89.25s)** (the 1:29-vs-1:51 call settled at 1:29),
  PRE1 = 1:09.75, V2 = 41.25, V4 = 144.5, PRE2 = 173. This prior gap is now CLOSED.
  The remaining open thread is the user's render-judgment of the re-timed cut (above).

## Open boundaries (awaiting explicit go)

- **No push / merge / PR** on `claude/when-it-rains-music-video-fetr0z` (repo has
  no trunk) — local commits only without explicit go.
- **No further Higgsfield generation / upscale** — spends credits = external
  mutation; STOP unless inside a confirmed media packet with go. (P-006's C25–C34
  generation go is **spent / done**; any new generation — including the ~10-credit
  C27/C33 regen if off-model — needs a fresh go.) **P-007 (edl insert + re-time)
  is the gated edit that follows.**

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29; P-003 note
appended 2026-06-29; P-004 note appended 2026-06-29; P-005 note appended
2026-06-29; P-006 note appended 2026-06-29._
