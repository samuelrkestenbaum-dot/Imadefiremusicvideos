# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **Beat-lock the EDL** — build the beat-lock script + regenerate `data/edl.csv`
  to the **0.97524s** beat grid (61.5234375 BPM) + trim ~2s off the FINAL so the
  276s cut resolves on the 274s mix end. Blocked on the user confirming the
  section times in `when-it-rains/SECTION_TIMES.md` (esp. the 1:29-vs-1:51
  chorus-downbeat call, which also settles PRE1) and on the MP3 being re-attached
  (it is staged this session but won't survive a new one — see risks below).
- **Band-coverage batch (~8 clips)** — lower priority; reduces C02's 11× overuse
  (pacing, not quality). Marketing/media authority; fire only after the lead is
  locked. Generation = credits = STOP without a confirmed media packet + go.
- **Selective 2K/4K upscale** — explicitly LAST, only after the cut is
  emotionally locked.

## Known risks / debt

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
- **Regenerated clips are unverified by human eye.** The 11 fixes (bald lead /
  content failures / auburn woman) were confirmed by **automated re-analysis**
  (`video_analysis`, with a canary on C13), NOT by a human watching a real
  playback. A render is the final confidence check. Two known-open items even
  after the fix: C04's head-turn is still absent, and the lead's exact face still
  varies slightly clip-to-clip (anchored, not a trained Soul). **`when-it-rains/RENDER_REVIEW.md`** (P-002, closed 2026-06-29) now exists as the structured timecode-keyed capture instrument for this still-pending human render review — but the gap itself stays open until the user actually renders + reviews.
- **Ambiguous mid-song section starts — now has a decision instrument, still
  open.** **`when-it-rains/SECTION_TIMES.md`** (P-003, closed 2026-06-29) now
  exists as the confirm/correct worksheet for the ambiguous section starts
  (V2/PRE1/CH1, V4/PRE2): 6 KEEP + 5 SUGGESTED, with the energy≠downbeat caveat
  recorded. The gap stays **open** until the user answers — especially the **CH1
  chorus-downbeat call (1:29 vs 1:51)**, which also settles PRE1. The beat-lock
  packet cannot start until these are confirmed.

## Open boundaries (awaiting explicit go)

- **No push / merge / PR** on `claude/when-it-rains-music-video-fetr0z` (repo has
  no trunk) — local commits only without explicit go.
- **No Higgsfield generation / upscale** — spends credits = external mutation;
  STOP unless inside a confirmed media packet with go.

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29; P-003 note
appended 2026-06-29._
