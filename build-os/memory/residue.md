# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **README + EDIT_MAP doc-drift — RESOLVED (P-013, from AUDIT-001).** The system
  audit flagged two stale docs: **D4** (EDIT_MAP described the pre-band-coverage
  state) and **D5-M1 / D5-M2** (README runtime 4:36/276 + wrong CSV schema lines).
  **P-013 fixed both:** README runtime → 86/274/4:34, `clips.csv` schema column
  order corrected to the real `mp4_url`/`section` header, `stills.csv` schema fixed
  (phantom `beat`/`on_model` removed), overhang 2s→0.25s; EDIT_MAP → 274/4:34 with
  an authority banner (`data/edl.csv` authoritative), the 11 confirmed section
  starts, the C25–C34 registry, and EX2 marked unused. Commits `8981252` (README)
  + `0c88c54` (EDIT_MAP), base `1f5211f`; qa GREEN 9/9 + Commit-1 isolation,
  reviewer PASS (Codex unavailable). Both project docs are now coherent with the
  86/274 edit. The doc-drift thread is **CLOSED**.
- **System audit AUDIT-001 — system ALIGNED to canonical.** 6 read-only auditors
  (D1–D6) vs a pinned canonical target found **zero structural / functional /
  process defects** — all findings are non-functional doc / catalog drift. Receipt
  `build-os/receipts/AUDIT-001.md`. The auto-fixable doc-coherence subset was closed
  by P-013, and the D5-M3 stills-catalog subset by P-014 (above); the rest is
  gated (D1-01) or deferred-by-design (below).
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
- **Stills-catalog backfill (D5-M3 / former P-010) — RESOLVED (P-014).** This was
  previously characterized as **declined / non-functional**; it is now **actually
  fixed**. AUDIT-001 (D5-M3) had quantified it as **13 / 36 clips' `source_still`
  not resolving to `stills.csv`**, driven by **10 reference-anchored regen stills
  generated on Higgsfield but never cataloged** (+ EX1 / EX2 "prior" + C04's
  `regenA1` placeholder), with **4 superseded off-model stills** (`22e02845` /
  `b0f3fd47` / `26443c5f` / `ff3797c3`) lingering unflagged. **P-014 closed it
  truthfully** (user authorized — "yes do it"): the **10 regen stills are now
  cataloged** in `stills.csv` + `assets.json`, **C04's `source_still` is resolved**
  from `regenA1` to its real still **`2d0ba697`** (CONFIRMED via the clip's
  `start_image`, job `297449bf` `medias.start_image` == `2d0ba697`; still ts 012553
  precedes clip ts 012654), and the **4 off-model stills are pruned** — net **+7 →
  59 stills**, counts fixed (`assets.json` stills 52 → 59, `HANDOFF.md` 52 → 59).
  UUIDs / URLs were retrieved **READ-ONLY from Higgsfield (no credits)**. Commits
  `6005114` + `2223893`, base `00af4e3`; **qa GREEN 9/9 + Commit-1 isolation**
  (stills.csv 59 rows, 11 present / 4 absent, clips.csv C04-only, assets.json valid
  59 / parity 36 / edl 86, 34/36 resolve, HANDOFF 59, safety clean); **reviewer
  PASS** (surgically exact, net +7, zero in-place mutations, C04 corroborated; Codex
  unavailable; non-defect caveat — CloudFront URLs not live-hit, egress 403 expected,
  source-derived). **Result: 34 / 36 clip `source_still`s resolve (all C01–C34).**
  The catalog thread is **CLOSED**.
- **EX1 / EX2 `'prior'` pointers — ACCEPTED (not an open gap).** The only two
  remaining stills non-resolvers are EX1 / EX2's `'prior'` `source_still`s, which
  point at a **prior project** — intentional / benign by design, **not** a defect or
  open backfill item.
- **D1-01 (engine source wording) — LOW, OPEN / GATED (AUDIT-001).** The
  ClaudeOrchestrator source `global-claude-md.md` says "(global) / user scope" even
  for project-scope installs — wording-only, no functional impact. The fix would
  edit the **source repo**, outside this project's `build-os/`-only authority →
  **GATED** (needs a go in the source repo).
- **D3-M1 (receipt wording) — LOW, OPEN (AUDIT-001).** Receipts say "not pushed"
  but `origin` mirrors HEAD — a **wording imprecision**, NOT an ungated mutation
  (the archivist never pushed; the mirror is an environment fact). Cosmetic; recorded
  so future receipts can phrase it precisely.
- **Sub-beat beat-grid quantization — a gated variant now EXISTS (P-015); its
  PROMOTION is deferred / user-gated.** P-015 built the beat-lock capability
  (`scripts/beat_lock.py` + 20-check suite) and produced the **non-destructive**
  variant `data/edl_beatlocked.csv` — the 86 cuts snapped to the **0.9752381 s**
  grid (61.5234375 BPM), section starts preserved, total 274.0 s, **84/86 snapped**,
  ±50 ms alignment **8.1 % → 84.9 %** (mean `|offset|` 256.0 → 52.7 ms, median 250.5
  → 3.0 ms). It is NOT applied to the live `data/edl.csv` (empty diff verified).
  **Promoting it into the live edit is a user-gated decision after human review** —
  premature until the cut is approved. **Caveat:** it snaps to **BEATS, not
  downbeats** (4/4 downbeat-phase confidence LOW ≈ 720 ms section-start error —
  downbeat times in `beats.json` are advisory only); one residual ~836 ms offset is
  the final cut end pinned by the 274.0 total + preserve-section-start constraints
  (intentional/conservative). Regenerating requires `song.mp3` re-attached in
  `when-it-rains/` (see risks); `analysis/beats.json` is the durable map that
  survives without it.
- **Verify the fast V3 cuts on render (P-004 follow-up).** The section-sync
  compressed **V3 ×0.53**, so its cuts are **~1.6–2.7s (fast)** — confirm on the
  render they read as energetic, not rushed.
- **Selective 2K/4K upscale — POST-APPROVAL.** Explicitly LAST, only after the cut
  is emotionally locked.
- **Render pipeline shipped + now recorded (P-015 close) — NOT its own packet.**
  Two commits landed this session but were unreceipted until the P-015 close:
  **`82ac71e`** (`scripts/render_master.sh` — one-shot validate→fetch→assemble→verify
  wrapper) and **`9ba310b`** (`scripts/preflight_edl.py` — offline render-readiness
  validator, + `render_master.sh` gated on it; `9ba310b` is also P-015's base). The
  **86-cut / 274.0 s live edit is validated render-ready** (`preflight_edl.py` 0
  critical). These are recorded in `current_state.md`; the render itself is still
  the user's (blocked in-session — see the CDN risk below).
- **In-session song-synced ANIMATIC delivered to the user (NOT committed).** A
  placeholder-visuals / real-timings animatic was produced this session as the
  pacing proof — it is a **scratchpad artifact, not in git**; it will not survive a
  new session and is not part of the deliverable.

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
  stay; the raw audio does not. **P-015 made the beat map durable:**
  `when-it-rains/analysis/beats.json` (the phase-locked grid) is committed and
  survives the mp3 disappearing — but re-**running** `beat_lock.py` / its 20-check
  suite from a bare checkout still needs `song.mp3` re-attached in `when-it-rains/`
  (`FileNotFoundError` otherwise — by design; `beats.json` is the durable output,
  not a defect).
- **No render in the cloud env — a POLICY BOUNDARY, not routable.** The Higgsfield
  CDN (`d8j0ntlcm91z4.cloudfront.net`) is **egress-blocked here (403, org policy)**
  and there is no system ffmpeg, so the real footage master **cannot be rendered or
  eyeballed in this session** — it MUST be rendered on the user's Mac
  (`scripts/render_master.sh`, the one-shot validate→fetch→assemble→verify wrapper,
  or `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`). Unblocking
  in-session would require the **user to allowlist the CDN host** for the session;
  otherwise render on a connected machine. `preview.html`
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
  no trunk) — local commits only without explicit go. **NOT YET PUSHED:** P-015
  commits **`c65748e`** + **`9370af3`**, the render-pipeline commits **`82ac71e`** +
  **`9ba310b`**, and the archivist's own `build-os/` close commit are all
  **local-only**, awaiting the user's explicit push go.
- **Promoting the beat-locked variant is USER-GATED.** `data/edl_beatlocked.csv`
  (P-015) is a ready, non-destructive alternative to the live `data/edl.csv`;
  swapping it into the live edit is the user's call after human review — do not
  promote it without an explicit go.
- **No further Higgsfield generation / upscale** — spends credits = external
  mutation; STOP unless inside a confirmed media packet with go. (P-006's C25–C34
  generation go is **spent / done**; the **C27/C33 regen is now MOOT** — P-008
  verified both on-model, so no regen is needed; any other new generation needs a
  **fresh go**.) The P-007 edit (the gated insert + re-time) is **done**; **P-008**
  (docs/manifest refresh) is **done**; **P-009** (manifest existing-row reconcile)
  is **done**; **P-011** (browser preview tool) is **done**; **P-012** (RENDER_REVIEW.md
  refresh) is **done**; **P-014** (stills-catalog backfill — UUIDs retrieved
  READ-ONLY, **no credits**) is **done** (D5-M3 RESOLVED). No
  generation-touching follow-up remains open; any **new** Higgsfield generation
  needs a **fresh go**.
- **Post-approval polish is premature** — the sub-beat beat-grid variant now
  EXISTS (P-015, `data/edl_beatlocked.csv`) but its **promotion** and any selective
  2K/4K upscale are explicitly later, after the user approves the cut.

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
items all user/optional — render-review, post-approval polish, declined P-010);
P-013 note + AUDIT-001 appended 2026-06-29 (README + EDIT_MAP doc-drift D4/D5
RESOLVED; system audit ALIGNED to canonical — zero structural/functional/process
defects; P-010 framing CORRECTED — 13/36 source_still unresolved = 10 uncataloged
regen stills + 4 stale off-model rows + EX1/EX2/C04, all non-functional, declined;
D1-01 + D3-M1 recorded as LOW open items); P-014 note appended 2026-06-29
(stills-catalog gap D5-M3 / former P-010 RESOLVED — 10 regen stills cataloged, C04
`source_still` resolved regenA1 → 2d0ba697 [CONFIRMED via clip start_image], 4
off-model stills pruned, stills 52 → 59, 34/36 source_stills resolve; UUIDs retrieved
READ-ONLY from Higgsfield, no credits; the "declined P-010" framing is RETIRED. Only
remaining stills non-resolvers = EX1/EX2 'prior' [a prior project — accepted/benign,
not an open gap]); P-015 note appended 2026-07-01 (beat-lock analysis + a gated,
NON-DESTRUCTIVE beat-aware EDL variant `data/edl_beatlocked.csv` [86 rows, section
starts preserved, 274.0 s, 84/86 snapped to the 0.9752381 s grid, ±50 ms alignment
8.1 % → 84.9 %] — live `data/edl.csv` byte-untouched [empty diff on all 6 product
surfaces]; durable map `analysis/beats.json`; snaps to BEATS not downbeats [downbeat
confidence LOW]; qa GREEN 8/8 / suite 20/20 / Commit-1 iso in throwaway worktree /
determinism by md5 / safety clean; reviewer PASS, Codex unavailable — solo; render
pipeline `82ac71e` + `9ba310b` recorded as shipped; live edit preflight render-ready;
CDN egress-block characterized as a 403 org-policy boundary; promotion of the variant
is user-gated; P-015 + render-pipeline commits + close are local-only, awaiting push
go)._
