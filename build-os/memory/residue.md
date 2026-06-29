# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **PRE2 / CH1 drag — now has a STAGED remediation (P-005 spec'd it).** The
  section-sync stretched **CH1 ×1.55** and **PRE2 ×1.64**, so their cuts hold
  **~5–6.5s and may DRAG**. P-005 turned the fix into a concrete plan:
  `when-it-rains/BAND_COVERAGE_PLAN.md` specifies **10 new band-only add-cuts**
  (C25–C30 PRE2 → 12 cuts @ 3.42s; C31–C34 CH1 → 12 cuts @ 3.23s), each fully
  recipe'd. Two gated packets remain to actually land them:
  - **P-006 — generate the 10 staged clips on Higgsfield (GATED = credits / external
    mutation).** Generate C25–C34 per the plan's recipes. STOP without the user's
    explicit go inside a confirmed media packet.
  - **P-007 — insert the 10 clips into `data/edl.csv` + re-time PRE2 / CH1 to ~3.3s
    avg (GATED edit).** Follows P-006. Needs explicit go.
  Fire P-006 only **after** the user's GO to generate (and ideally after the
  render-judgment confirms the drag). The added cuts are the fix — **NOT** stretched
  holds.
- **P-005 non-blocking generation-time notes (carry into P-006 / P-007):**
  1. At generation, ensure **C26 (full-band push-in)** reads visually **distinct**
     from existing **C09 (also a push-in)** — avoid a near-duplicate shot.
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
  `video_analysis` (free, bypasses the CDN) is the only in-session look at footage.
  The section-synced timing (P-004) is therefore **unverified by human eye** until
  the user renders the re-timed cut.
- **Regenerated clips are unverified by human eye.** The 11 fixes (bald lead /
  content failures / auburn woman) were confirmed by **automated re-analysis**
  (`video_analysis`, with a canary on C13), NOT by a human watching a real
  playback. A render is the final confidence check. Two known-open items even
  after the fix: C04's head-turn is still absent, and the lead's exact face still
  varies slightly clip-to-clip (anchored, not a trained Soul). **`when-it-rains/RENDER_REVIEW.md`** (P-002, closed 2026-06-29) now exists as the structured timecode-keyed capture instrument for this still-pending human render review — but the gap itself stays open until the user actually renders + reviews.
- **Mid-song section starts — now CONFIRMED + applied (resolved).**
  **`when-it-rains/SECTION_TIMES.md`** (P-003) proposed the ambiguous starts; the
  user **CONFIRMED** them ("those look good, keep going") and **P-004 applied them**
  to `data/edl.csv` — **CH1 = 1:29 (89.25s)** (the 1:29-vs-1:51 call settled at 1:29),
  PRE1 = 1:09.75, V2 = 41.25, V4 = 144.5, PRE2 = 173. This prior gap is now CLOSED.
  The remaining open thread is the user's render-judgment of the re-timed cut (above).

## Open boundaries (awaiting explicit go)

- **No push / merge / PR** on `claude/when-it-rains-music-video-fetr0z` (repo has
  no trunk) — local commits only without explicit go.
- **No Higgsfield generation / upscale** — spends credits = external mutation;
  STOP unless inside a confirmed media packet with go. **P-006 (generate C25–C34)
  is GATED on this**; **P-007 (edl insert + re-time) is the gated edit that follows.**

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29; P-003 note
appended 2026-06-29; P-004 note appended 2026-06-29; P-005 note appended
2026-06-29._
