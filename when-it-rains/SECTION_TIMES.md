# Section-Time Proposal — "When It Rains"

**What this is.** A data-driven proposal to settle the **ambiguous mid-song
section start times** *before* the beat-lock packet runs. It does **not** change
the edit — it proposes a RECOMMENDED start for each of the 11 sections, marked
**KEEP** (the energy data agrees with the current EDL) or **SUGGESTED** (the data
hints at a different start and needs your ear). You read it, then **confirm or
correct** each row. Your confirmed times feed the beat-lock packet, which then
regenerates `data/edl.csv` to snap every cut onto the beat grid (and folds in the
~2s FINAL trim). This is the worksheet `HANDOFF.md` Open thread #2 and
`RENDER_REVIEW.md`'s "Section-time confirmation" block both point to.

**How to use it.** For every section in the table below, look at the **RECOMMENDED
start**. If it's right, write `KEEP` (or the same time) in the **Your call**
column. If your ear says otherwise, write the corrected `mm:ss` there. The
**KEEP** rows are low-risk (the data already agrees with the EDL); the
**SUGGESTED** rows are the ones to actually listen to.

**Runtime context.** The music resolves at **4:33.75** (`music_end = 273.75s` in
`analysis/song.json`; file duration is `284.4s`). The current EDL sums to
**276.0s (≈4:36)** — so the last shot currently overhangs the music by **~2.25s**
(276.0 − 273.75). That overhang is the known **FINAL truncation** (`RENDER_REVIEW.md`
watch-point C, `FOOTAGE_AUDIT.md` §6); the beat-lock packet trims it upstream. This
proposal is about *where each section starts*, not the trim — but the two are
confirmed together, so the runtime is stated here for context.

---

## Caveat — read before trusting any number below

- **The detected "transitions" are RMS-energy shifts, NOT musical downbeats.**
  `analyze_song.py` picks the 12 biggest changes in a smoothed energy envelope,
  spaced ≥12s apart (see lines 39–45). A loud entry, a drum fill, a sudden drop,
  or a swell all register as an "energy transition." So these numbers are
  **evidence, not truth** — they tell you *where the song's loudness changes*, not
  *where a bar starts*.
- **The 61.5234375 BPM grid is a reference, not a snap target here.**
  beat = 60 ÷ 61.5234375 = **0.97524s** (≈0.9753s). That grid is useful for
  sanity-checking spacing, but a true beat-snap needs a **downbeat phase
  reference** (which beat is beat 1 of the bar) — and the energy detector does not
  give that. **Exact beat-snapping is deferred to the beat-lock packet.** Treat
  every "≈" below as approximate.
- **Therefore:** KEEP rows mean "the EDL start and a detected energy shift agree,
  so it's probably already close." SUGGESTED rows mean "the data leans toward a
  different start — listen and decide." Neither is a beat-accurate timecode yet.

---

## The 11-section proposal

Current EDL starts are from `analysis/analyze_song.py` (lines 62–63). Transitions
are from `analysis/song.json`. All times in **mm:ss (seconds)**.

| Section | Current EDL start | Nearest detected energy transition(s) | RECOMMENDED start | Flag | Your call (confirm / correct) | Reasoning |
|---------|-------------------|----------------------------------------|-------------------|------|-------------------------------|-----------|
| **INTRO** | 0:00 (0.0) | — (first transition 0:19.25 is the V1 entry, not an INTRO move) | **0:00** | KEEP | | Song start is fixed at 0. The 0:19.25 shift is context only — it marks where V1 comes in. |
| **V1** | 0:18 (18.0) | 0:19.25 (19.25) | **0:18–0:19** | KEEP | | Anchored: EDL 18.0 vs transition 19.25 agree within ~1.25s — the band/verse entry. Keep ≈ as-is; beat-lock fine-tunes. |
| **V2** | 0:48 (48.0) | 0:41.25 (41.25) | **≈0:41 (41)** | SUGGESTED | | Energy shift sits ~6.75s *earlier* than the EDL start. Leans toward V2 beginning nearer 0:41. **Needs your ear** — is the verse-2 line at ~0:41 or ~0:48? |
| **PRE1** | 1:18 (78.0) | 1:09.75 (69.75) | **≈1:10 (70)** | SUGGESTED | | Energy shift ~8.25s *earlier* than the EDL start. Pre-chorus build may start nearer 1:10. **Needs your ear.** Moving it earlier lengthens PRE1 and shortens V2's tail. |
| **CH1** | 1:43 (103.0) | **1:29.25 (89.25)** and **1:51.00 (111.0)** — two candidates | **≈1:29 (89.25)**, pending your ear | SUGGESTED | | **Two transitions bracket CH1 — see the note below.** 89.25 reads as the chorus *lift* (band release at the downbeat); 111.0 is energy *within* an already-running chorus. Recommend 89.25 as the chorus downbeat, but this is the call most needing your ear: 89.25 pulls CH1 ~14s earlier and eats most of PRE1. |
| **V3** | 2:08 (128.0) | 2:10.50 (130.5) | **2:08–2:10** | KEEP | | Anchored: EDL 128.0 vs transition 130.5 agree within ~2.5s — the verse-3 re-entry after CH1. Keep ≈ as-is. |
| **V4** | 2:39 (159.0) | 2:24.50 (144.5) | **≈2:24–2:25 (144.5)** | SUGGESTED | | Energy shift ~14.5s *earlier* than the EDL start. The detector sees the section change nearer 2:24. **Needs your ear** — this is a large move; confirm whether V4's story beat begins that early. |
| **PRE2** | 3:09 (189.0) | 2:53.00 (173.0) | **≈2:53 (173)** | SUGGESTED | | Energy shift ~16s *earlier* than the EDL start (the largest gap). Pre-chorus-2 build may start nearer 2:53. **Needs your ear** — big move; this is the most uncertain ambiguous row. |
| **CH2** | 3:34 (214.0) | 3:30.75 (210.75) | **3:31–3:34** | KEEP | | Anchored: EDL 214.0 vs transition 210.75 agree within ~3.25s — the chorus-2 release. Keep ≈ as-is. |
| **BRIDGE** | 3:58 (238.0) | 3:56.25 (236.25) | **3:56–3:58** | KEEP | | Anchored: EDL 238.0 vs transition 236.25 agree within ~1.75s — the bridge breakdown. Keep ≈ as-is. |
| **FINAL** | 4:21 (261.0) | 4:16.50 (256.5) | **4:16–4:21** | KEEP | | Anchored: EDL 261.0 vs transition 256.5 agree within ~4.5s — the final-chorus / outro lift. Keep ≈ as-is. (Separately, the FINAL section is where the ~2.25s trim lands — beat-lock packet.) |

**Summary:** 6 sections **KEEP** (INTRO, V1, V3, CH2, BRIDGE, FINAL — INTRO is
fixed, the other 5 are data-anchored) · 5 sections **SUGGESTED** (V2, PRE1, CH1,
V4, PRE2 — the ambiguous mid-song block). The 5 SUGGESTED rows are exactly the
block `RENDER_REVIEW.md` and `HANDOFF.md` flag as "ambiguous from energy alone."

---

## Honest handling of the transition-count mismatch

There are **12 detected transitions** but only **10 post-INTRO sections**, so the
map is **not 1:1** — at least **2 transitions are mid-section energy events, not
section boundaries.** Forcing a 1:1 map would invent boundaries that aren't there.
Here is how each transition is treated:

| Transition | mm:ss | Treated as | Why |
|------------|-------|-----------|-----|
| 19.25 | 0:19.25 | **Boundary → V1** | Verse-1 / band entry; agrees with EDL 18.0. |
| 41.25 | 0:41.25 | **Boundary → V2** | The energy shift the V2 SUGGESTED start moves toward. |
| 69.75 | 1:09.75 | **Boundary → PRE1** | The energy shift the PRE1 SUGGESTED start moves toward. |
| **89.25** | **1:29.25** | **Boundary → CH1** (recommended) | Reads as the chorus lift / band release — the chorus downbeat. |
| **111.0** | **1:51.00** | **Mid-section** (energy *within* CH1) | A second swell after the chorus has already begun, not a new section. |
| 130.5 | 2:10.50 | **Boundary → V3** | Verse-3 re-entry; agrees with EDL 128.0. |
| 144.5 | 2:24.50 | **Boundary → V4** | The energy shift the V4 SUGGESTED start moves toward. |
| 173.0 | 2:53.00 | **Boundary → PRE2** | The energy shift the PRE2 SUGGESTED start moves toward. |
| 210.75 | 3:30.75 | **Boundary → CH2** | Chorus-2 release; agrees with EDL 214.0. |
| 236.25 | 3:56.25 | **Boundary → BRIDGE** | Bridge breakdown; agrees with EDL 238.0. |
| 256.5 | 4:16.50 | **Boundary → FINAL** | Final-chorus / outro lift; agrees with EDL 261.0. |
| **272.5** | **4:32.50** | **Mid-section** (energy event inside FINAL / right at the outro) | Sits ~11.5s into FINAL and only ~1.25s before `music_end` (273.75) — it's the final resolve/decay, not a new section. |

So: **10 transitions are read as section boundaries** (one per post-INTRO
section), and **2 are read as mid-section energy events** — **111.0** (a swell
inside CH1) and **272.5** (the outro resolve inside FINAL). That accounts for all
12 without forcing a false boundary.

### The CH1 call: 89.25 vs 111.0

CH1 is the one section with **two** plausible boundary transitions bracketing it
(EDL start 1:43 / 103.0 sits between them):

- **89.25 (1:29.25)** — recommended as the **chorus downbeat.** In this kind of
  build-and-release structure, the single biggest energy jump is usually the
  chorus *entry* (the band "opens up"). 89.25 is that jump. Choosing it moves CH1
  **~14s earlier** than the EDL (103 → 89.25), which **absorbs most of the current
  PRE1 section** — i.e. what the EDL labels late-PRE1 would become early-CH1.
- **111.0 (1:51.00)** — treated as a **second swell inside an already-running
  chorus** (a post-hook lift), not the chorus entry. Choosing it instead would
  push CH1 **~8s later** (103 → 111) and shrink CH1.

**Recommendation: 89.25**, but flagged as the call **most needing your ear**,
because it's coupled to PRE1: if PRE1 also moves earlier (to ~70, its SUGGESTED
start) and CH1 moves to ~89.25, the pre-chorus stays a real section; if PRE1 stays
at 1:18 but CH1 jumps to 89.25, PRE1 collapses to almost nothing. **Listen to
1:29 vs 1:51 and tell me which one is the chorus downbeat** — that single answer
resolves both PRE1 and CH1.

---

## Verified source numbers (so you can check this proposal)

| Quantity | Value | Source |
|----------|-------|--------|
| File duration | 284.4s (4:44.4) | `analysis/song.json` `duration` |
| Music end | 273.75s (4:33.75) | `analysis/song.json` `music_end` |
| Tempo | 61.5234375 BPM | `analysis/song.json` `tempo_bpm` |
| Beat length | 60 ÷ 61.5234375 = **0.97524s** | computed (reference grid only) |
| Detected transitions (s) | 19.25, 41.25, 69.75, 89.25, 111.0, 130.5, 144.5, 173.0, 210.75, 236.25, 256.5, 272.5 | `analysis/song.json` `transitions` |
| Current EDL section starts (s) | INTRO 0, V1 18, V2 48, PRE1 78, CH1 103, V3 128, V4 159, PRE2 189, CH2 214, BRIDGE 238, FINAL 261 | `analysis/analyze_song.py` lines 62–63 |
| EDL total | 276.0s (≈4:36); overhang vs music = ~2.25s | `data/edl.csv` (76 cuts), `RENDER_REVIEW.md` |

---

## What happens after you confirm

| Your output here | Feeds into |
|------------------|------------|
| Confirmed / corrected starts for the 5 SUGGESTED rows (V2, PRE1, CH1, V4, PRE2) — especially the **89.25-vs-111.0 chorus-downbeat answer** | **Beat-lock packet** — regenerate `data/edl.csv` to snap every cut onto the 0.97524s grid, using your confirmed starts + a downbeat phase reference. |
| The KEEP rows you accept as-is | Beat-lock treats them as fixed anchors and only fine-tunes within ~1 beat. |
| (Confirmed alongside) the ~2.25s FINAL overhang | Beat-lock trims ~2s upstream so the last shot lands on the music resolve (`FOOTAGE_AUDIT.md` §6, `RENDER_REVIEW.md` watch-point C). |

Cross-references: `HANDOFF.md` Open thread #2 · `RENDER_REVIEW.md`
"Section-time confirmation" · `EDIT_MAP.md` · `FOOTAGE_AUDIT.md` §6.
