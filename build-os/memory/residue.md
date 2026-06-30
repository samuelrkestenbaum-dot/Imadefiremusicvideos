# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **`when-it-rains/RENDER_REVIEW.md` stale — RESOLVED (P-012).** It had still
  described the **pre-band-coverage 76-cut / 276.0s / 4:36** edit (predating the
  P-004 section-sync → 274s and the P-006/P-007 band coverage → 86 cuts). **P-012
  rewrote it to the current 86-cut / 274.0s edit**: the 86-row per-cut table
  re-derived from `data/edl.csv` (timecodes to 274.0s, cut 86 = 4:34.0), header →
  86 / 274 / 4:34, watch-points refreshed (band coverage C25–C34 added, C27/C33
  on-model confirmed, section times marked CONFIRMED), `preview.html` pointer
  added, and the stale 76/276/4:36 figures **demoted to explicit history** (not
  silently deleted). One file, 213 ins / 164 del, base `25a6a7f`; qa GREEN 8/8
  (table independently re-derived from `edl.csv` — 86/86 rows, 0 mismatches),
  reviewer PASS (every timecode reproducible to the hundredth; Codex unavailable).
  **Both review instruments are now current at 86/274** — `preview.html` (silent
  browser pass) + `RENDER_REVIEW.md` (audio-render checklist). The stale-doc thread
  is **CLOSED**; the remaining check is the user's human render-eye (below).
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
- **`assets.json` pre-existing regenerated-clip rows drift — RESOLVED (P-009).**
  `assets.json`'s existing clip entries for the 11 earlier-regenerated clips
  (**C01, C04, C06, C07, C13, C15, C16, C19, C22, C23, C24**) had carried
  **pre-regen job_ids / urls**, diverging from the fixed `clips.csv`. **P-009
  reconciled them** (job_id / source_still / mp4_url updated verbatim from
  `clips.csv`; 33 ins / 33 del, exactly the 11 changed, other 25 byte-identical;
  qa GREEN 8/8, reviewer PASS). Combined with P-008 (counts / runtime / C25–C34
  array rows / inline `edl` array), the manifest now **fully matches** the
  functional CSVs. The drift thread is **CLOSED** (non-functional all along — the
  render reads `clips.csv`, not `assets.json`).
- **`source_still` ↔ `stills.csv` id-format gap — OPTIONAL / LOW-PRIORITY (P-010),
  DECLINED by user.**
  `clips.csv`'s `source_still` values are **8-char prefixes** that do **not**
  resolve to `stills.csv`'s **full-UUID** keys — a **pre-existing id-format quirk
  affecting all 36 clips both BEFORE and AFTER P-009** (NOT a P-009 defect, per the
  reviewer). It is **non-functional**: the render reads each clip's `mp4_url` from
  `clips.csv` directly, not via the still join. Additionally, **C04's**
  `source_still` is a `regenA1` **placeholder** (known-incomplete from the earlier
  C04 partial regen — hair/reflection fixed, head-turn still absent). A backfill
  (**P-010**) would resolve the prefixes to full UUIDs and replace the C04
  placeholder — but it **touches a source CSV + a count**, so it needs an **explicit
  go**. Low priority; non-blocking for the render-review; user has declined it for
  now.
- **Sub-beat beat-grid quantization (still deferred / optional — POST-APPROVAL).**
  Snap the 86 cuts to the **0.97524s** beat grid (61.5234375 BPM) on top of the
  section-sync — but this needs a **rigorous downbeat phase reference** and the MP3
  re-attached (staged this session, won't survive a new one — see risks).
  **Premature until the cut is approved.** P-004 delivered the coarser
  **section-sync** and P-007 the band-coverage insert; neither is this finer beat
  quantization.
- **Verify the fast V3 cuts on render (P-004 follow-up).** The section-sync
  compressed **V3 ×0.53**, so its cuts are **~1.6–2.7s (fast)** — confirm on the
  render they read as energetic, not rushed.
- **Selective 2K/4K upscale — POST-APPROVAL.** Explicitly LAST, only after the cut
  is emotionally locked.

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
  (`scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`). `preview.html`
  (P-011) offers an **in-browser** review path — the browser CAN reach the CDN even
  though this cloud session's egress cannot, so the user can stream + review the 86
  cuts in a browser (silent, approximate-timing) without the Mac render. Server-side
  `video_analysis` (free, bypasses the CDN) is the only in-session look at footage —
  **and it only accepts imported video ids, not generation job ids** (this is why
  the P-006 clips could not be auto-checked on-model). The 86-cut, PRE2/CH1-retimed
  cut (P-007) is therefore **unverified by human eye** until the user reviews it
  (via preview.html or the full render).
- **The rough cut still needs a human review pass — STILL OPEN.** The full 86-cut
  274.0s edit (the 11 P-002-era fixes + the P-004 section-sync + the P-006/P-007
  band coverage) has **not been watched by a human**. The 11 fixes were confirmed
  by **automated re-analysis** (`video_analysis`, canary on C13), and the 10 band
  clips were not auto-analyzed at all (only reference-anchoring confirmed +
  C27/C33 shown). A render (or the P-011 `preview.html`) is the confidence check.
  Known-open even after the P-002 fix: C04's head-turn is still absent, and the
  lead's exact face still varies slightly clip-to-clip (anchored, not a trained
  Soul). **Both review instruments are now current at 86/274:**
  `when-it-rains/RENDER_REVIEW.md` (P-002 instrument, **refreshed to 86/274 by
  P-012** — no longer stale) is the structured timecode-keyed capture checklist for
  the audio render, and `when-it-rains/preview.html` (P-011) is the silent
  in-browser pass. The review gap stays open until the user actually reviews
  (preview.html and/or the full Mac render, now including C25–C34 and the new
  PRE2/CH1 pacing).
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
  is **done**; **P-011** (browser preview tool) is **done**; **P-012** (RENDER_REVIEW.md
  refresh) is **done**. The only generation-touching follow-up left is **P-010**
  (optional stills backfill — touches a source CSV + a count; **declined by user**),
  which needs a **fresh go**.
- **Post-approval polish is premature** — sub-beat beat-grid quantization and
  selective 2K/4K upscale are explicitly later, after the user approves the cut.

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29; P-003 note
appended 2026-06-29; P-004 note appended 2026-06-29; P-005 note appended
2026-06-29; P-006 note appended 2026-06-29; P-007 note appended 2026-06-29
(PRE2/CH1 drag RESOLVED); P-008 note appended 2026-06-29 (C27/C33 on-model
RESOLVED — verified on-model; P-009 manifest-drift item opened); P-009 note
appended 2026-06-29 (assets.json drift RESOLVED; remaining source_still↔stills.csv
id-format gap re-characterized as optional P-010); P-011 note appended 2026-06-29
(browser preview tool `preview.html` delivered; NEW finding — RENDER_REVIEW.md is
STALE at 76-cut/276s, preview.html supersedes it for the live review, optional
refresh to 86/274 needs go); P-012 note appended 2026-06-29 (RENDER_REVIEW.md stale
RESOLVED — refreshed to 86/274; both review instruments now current; remaining open
items all user/optional — render-review, post-approval polish, declined P-010)._
