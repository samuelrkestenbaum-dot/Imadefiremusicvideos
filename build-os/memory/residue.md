# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **Beat-lock the EDL** — regenerate `data/edl.csv` to the beat grid + trim ~2s
  off the FINAL so the 276s cut resolves on the 274s mix end. Blocked on the user
  confirming the ambiguous mid-song section times (V2/PRE1/CH1, V4/PRE2) and on
  the MP3 being re-attached (see risks below).
- **Band-coverage batch (~8 clips)** — lower priority; reduces C02's 11× overuse
  (pacing, not quality). Marketing/media authority; fire only after the lead is
  locked. Generation = credits = STOP without a confirmed media packet + go.
- **Selective 2K/4K upscale** — explicitly LAST, only after the cut is
  emotionally locked.

## Known risks / debt

- **The song MP3 is NOT in git.** `When_It_Rains__Jun_27_mix.mp3` is gitignored
  and lives only in the session's uploads dir — it will NOT survive into a new
  session. It **must be re-attached** before any audio/beat-lock work. The
  `analysis/` outputs (BPM, climaxes, ~4:33.8 music end) are derived and stay,
  but the raw audio does not.
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

## Open boundaries (awaiting explicit go)

- **No push / merge / PR** on `claude/when-it-rains-music-video-fetr0z` (repo has
  no trunk) — local commits only without explicit go.
- **No Higgsfield generation / upscale** — spends credits = external mutation;
  STOP unless inside a confirmed media packet with go.

---
_Append-only working notes. Seeded from `when-it-rains/HANDOFF.md` +
`FOOTAGE_AUDIT.md` on 2026-06-29. P-002 note appended 2026-06-29._
