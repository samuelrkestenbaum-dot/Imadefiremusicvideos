# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **PRE2 / CH1 drag — RESOLVED (P-007).** The section-sync had stretched
  **CH1 ×1.55** and **PRE2 ×1.64** so their cuts held **~5–6.5s and dragged**.
  P-005 spec'd the fix, P-006 generated the 10 band-only add-cuts, and **P-007
  inserted them + re-timed**: PRE2 **6→12 cuts** (41.00s, ~3.4s avg, lead 4.12s),
  CH1 **8→12 cuts** (38.75s, ~3.1–3.2s). `data/edl.csv` is now **86 cuts /
  274.0s**, all section starts unchanged, no two new cuts back-to-back. The drag
  thread is **CLOSED** — the remaining check is the human render-eye on the new
  pacing (below).
- **C27 + C33 (singer-facing) on-model — RESOLVED (P-008).** Earlier the
  Higgsfield `video_analysis` check had errored on the P-006 clips, so C27/C33
  on-model was carried open. **P-008 verified both ON-MODEL** via `video_analysis`:
  **C27** "late-30s, fair complexion, very short thinning reddish hair, light
  beard"; **C33** "mid-30s, freckles, short ginger hair, trimmed ginger beard" —
  short reddish/ginger hair + beard, **NOT bald**. The reference-anchoring bald-fix
  **held**; **no C27/C33 regen needed**. This **CLOSES the open on-model item from
  P-006**. (Still an automated confirmation, not a human eye — the render pass
  remains the final human-eye check, but the on-model RISK is closed.)
- **`assets.json` pre-existing regenerated-clip rows drift — NEW, handled by P-009.**
  `assets.json`'s **existing** clip entries for the 11 earlier-regenerated clips
  (**C01, C04, C06, C07, C13, C15, C16, C19, C22, C23, C24**) still carry
  **pre-regen job_ids / urls**, diverging from the fixed `clips.csv`. This is
  **non-functional** — the render reads `clips.csv` (the source of truth), not
  `assets.json` — but it is a manifest drift **P-009 reconciles** (bring the
  manifest's existing rows into line with the fixed CSVs; no generation, no CSV
  functional change). P-008 already reconciled the counts block, the runtime, the
  C25–C34 array rows, and the inline `edl` array; P-009 finishes the existing-row
  reconcile.
- **Sub-beat beat-grid quantization (still deferred / optional).** Snap the 86
  cuts to the **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync —
  but this needs a **rigorous downbeat phase reference** and the MP3 re-attached
  (staged this session, won't survive a new one — see risks). P-004 delivered the
  coarser **section-sync** and P-007 the band-coverage insert; neither is this
  finer beat quantization.
- **Verify the fast V3 cuts on render (P-004 follow-up).** The section-sync
  compressed **V3 ×0.53**, so its cuts are **~1.6–2.7s (fast)** — confirm on the
  render they read as energetic, not rushed.
- **Selective 2K/4K upscale** — explicitly LAST, only after the cut is emotionally
  locked.

## Known risks / debt

- **The edit is reversible (two-layer chain) — neither backup overwritten.**
  `when-it-rains/data/edl_pre_bandcoverage_backup.csv` is a **byte-identical**
  backup of the pre-P-007 (76-cut, section-synced 274.0s) EDL; restoring it over
  `data/edl.csv` returns the pre-band-coverage cut byte-for-byte.
  `when-it-rains/data/edl_original_backup.csv` is still the **byte-exact**
  pre-section-sync (pre-P-004) original 276s EDL (sha256 `786a51b1…`). Both
  `scripts/resync_edl.py` and `scripts/insert_band_coverage.py` are
  deterministic / idempotent, so each layer can be regenerated exactly from
  inputs.
- **P-006/P-007 band assets are now in git.** The 10 generated stills/clips
  (C25–C34) are written into `data/clips.csv` (+10) / `data/stills.csv` (+10) by
  P-007; the **durable map of UUIDs + mp4 URLs** remains `build-os/receipts/P-006.md`.
  The `scratchpad/p006_assets.json` copy will **NOT survive a new session** — rely
  on the receipt + the now-committed `data/` rows.
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
  the P-006 clips could not be auto-checked on-model). The 86-cut, PRE2/CH1-retimed
  cut (P-007) is therefore **unverified by human eye** until the user renders it.
- **The rough cut still needs a human render pass — STILL OPEN.** The full 86-cut
  274.0s edit (the 11 P-002-era fixes + the P-004 section-sync + the P-006/P-007
  band coverage) has **not been watched by a human**. The 11 fixes were confirmed
  by **automated re-analysis** (`video_analysis`, canary on C13), and the 10 band
  clips were not auto-analyzed at all (only reference-anchoring confirmed +
  C27/C33 shown). A render is the final confidence check. Known-open even after
  the P-002 fix: C04's head-turn is still absent, and the lead's exact face still
  varies slightly clip-to-clip (anchored, not a trained Soul).
  **`when-it-rains/RENDER_REVIEW.md`** (P-002) is the structured timecode-keyed
  capture instrument for this still-pending review — the gap stays open until the
  user actually renders + reviews (now including C25–C34 and the new PRE2/CH1
  pacing).
- **Mid-song section starts — CONFIRMED + applied (resolved).**
  **`when-it-rains/SECTION_TIMES.md`** (P-003) proposed the ambiguous starts; the
  user **CONFIRMED** them ("those look good, keep going") and **P-004 applied them**
  to `data/edl.csv` — **CH1 = 1:29 (89.25s)** (the 1:29-vs-1:51 call settled at 1:29),
  PRE1 = 1:09.75, V2 = 41.25, V4 = 144.5, PRE2 = 173. P-007 preserved all 12
  section starts. This gap is CLOSED; the remaining open thread is the user's
  render-judgment of the cut (above).

## Open boundaries (awaiting explicit go)

- **No push / merge / PR** on `claude/when-it-rains-music-video-fetr0z` (repo has
  no trunk) — local commits only without explicit go.
- **No further Higgsfield generation / upscale** — spends credits = external
  mutation; STOP unless inside a confirmed media packet with go. (P-006's C25–C34
  generation go is **spent / done**; the **C27/C33 regen is now MOOT** — P-008
  verified both on-model, so no regen is needed; any other new generation needs a
  **fresh go**.) The P-007 edit (the gated insert + re-time) is **done**; **P-008**
  (docs/manifest refresh) is **done**; **P-009** (manifest existing-row reconcile)
  is a docs-only edit — no generation.

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29; P-003 note
appended 2026-06-29; P-004 note appended 2026-06-29; P-005 note appended
2026-06-29; P-006 note appended 2026-06-29; P-007 note appended 2026-06-29
(PRE2/CH1 drag RESOLVED); P-008 note appended 2026-06-29 (C27/C33 on-model
RESOLVED — verified on-model; P-009 manifest-drift item opened)._
