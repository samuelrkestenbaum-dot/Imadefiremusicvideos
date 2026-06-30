# Render-Review Checklist — "When It Rains" rough cut

**What this is.** A watch-once checklist for the rendered rough cut. It lists all
**86 EDL cuts in playback order** with their running in→out timecode, so you can
flag failures by **timecode + cut index + clip key** while you watch. This is the
instrument for the **full audio render on the Mac** — the one place you judge
pacing against the actual music. (For a fast, silent visual/order/on-model pass
in the browser, open `preview.html` first; it has no audio, so it can't replace
this render-against-the-music pass.) The output of this pass feeds the next
packets (beat-lock the EDL, optional regen refinements).

**How to use it.**
1. Render the rough cut on your Mac (`scripts/fetch_assets.sh` then
   `scripts/assemble_rough_cut.sh` — see `REVIEW.md` Step 0).
2. Watch it **once, straight through, in playback order.** Don't scrub.
3. For each cut, mark the **PASS / FAIL (reason)** cell: `PASS`, or
   `FAIL — <one-line reason>`. Note anything by its timecode so the fix list
   writes itself.
4. Then run the **Targeted watch-points** pass (below) for the known risk-spots,
   and skim the **Section-time confirmation** block (now all confirmed & applied).

**Target runtime.** The EDL now sums to **exactly 274.0s (4:34)** and the Jun-27
mix resolves at **~273.75s** — so the cut and the music end land together with
only a **~0.25s** tail (the old 2-second FINAL overhang is gone, see watch-point C).
The timecodes in the table below are the **EDL's own running times** (cut 1 in =
0:00; each out = in + duration; sub-seconds carried), so the last cut reads
**4:31.4–4:34.0**. (The earlier review described a shorter 76-cut edit that
summed long with a ~2s overhang — now superseded by this 86-cut/274.0s edit.)

---

## Per-cut checklist (all 86 cuts, playback order)

Mark each row PASS or FAIL with a one-line reason. (Timecodes regenerated
directly from `data/edl.csv` — cut 86 out = 4:34.0 = 274.0s.)

| # | In–Out | Section | Clip | EDL note | PASS / FAIL (reason) |
|---|--------|---------|------|----------|----------------------|
| 1 | 0:00–0:04 | INTRO | C03 | rain on glass (open) | |
| 2 | 0:04–0:08 | INTRO | C01 | band room wakes | |
| 3 | 0:08–0:11 | INTRO | C02 | singer close-up | |
| 4 | 0:11–0:15 | INTRO | C04 | man alone by window | |
| 5 | 0:15–0:18 | INTRO | C03 | rain hold into verse | |
| 6 | 0:18–0:21.1 | V1 | C02 | sings opening line | |
| 7 | 0:21.1–0:24.98 | V1 | C04 | turns as if touched; reflection dissolves | |
| 8 | 0:24.98–0:27.31 | V1 | C01 | restrained band | |
| 9 | 0:27.31–0:30.41 | V1 | C06 | grey ocean | |
| 10 | 0:30.41–0:33.51 | V1 | EX1 | gazes at ocean through glass | |
| 11 | 0:33.51–0:36.61 | V1 | C05 | river bend | |
| 12 | 0:36.61–0:38.94 | V1 | C02 | singer | |
| 13 | 0:38.94–0:41.25 | V1 | C04 | window | |
| 14 | 0:41.25–0:46 | V2 | C07 | over shoulder; her reflection surfaces | |
| 15 | 0:46–0:48.85 | V2 | C02 | face-on singing | |
| 16 | 0:48.85–0:51.7 | V2 | C03 | rain behind him | |
| 17 | 0:51.7–0:55.5 | V2 | C07 | raindrop breaks reflection; empty room | |
| 18 | 0:55.5–0:58.35 | V2 | C09 | band fragments | |
| 19 | 0:58.35–1:01.2 | V2 | C02 | more direct | |
| 20 | 1:01.2–1:05 | V2 | C04 | window | |
| 21 | 1:05–1:09.75 | V2 | C07 | reflection again | |
| 22 | 1:09.75–1:13.65 | PRE1 | C08 | curtains breathe; trees move | |
| 23 | 1:13.65–1:16.77 | PRE1 | C13 | almost turns toward a sound | |
| 24 | 1:16.77–1:19.89 | PRE1 | C09 | drummer enters | |
| 25 | 1:19.89–1:22.23 | PRE1 | C02 | it's like you never left | |
| 26 | 1:22.23–1:25.35 | PRE1 | C08 | trees move | |
| 27 | 1:25.35–1:29.25 | PRE1 | C09 | push-in | |
| 28 | 1:29.25–1:33.4 | CH1 | C12 | band release | |
| 29 | 1:33.4–1:36.51 | CH1 | C10 | puddle reflection trembles | |
| 30 | 1:36.51–1:39.71 | CH1 | C31 | drummer strikes the backbeat hard, cymbal shimmers | |
| 31 | 1:39.71–1:42.82 | CH1 | C19 | thunder flash | |
| 32 | 1:42.82–1:45.93 | CH1 | C11 | woman from behind, gone | |
| 33 | 1:45.93–1:49.13 | CH1 | C32 | hands strum and move along the fretboard, chorus rhythm | |
| 34 | 1:49.13–1:52.24 | CH1 | C12 | band | |
| 35 | 1:52.24–1:55.35 | CH1 | C02 | chorus with force | |
| 36 | 1:55.35–1:58.55 | CH1 | C33 | singer sings the chorus with force into the mic, slight push-in | |
| 37 | 1:58.55–2:01.66 | CH1 | C10 | water again | |
| 38 | 2:01.66–2:04.77 | CH1 | C12 | band | |
| 39 | 2:04.77–2:08 | CH1 | C34 | hands lift into the chorus on the keys under warm lamp | |
| 40 | 2:08–2:10.66 | V3 | C13 | turns toward window at thunder | |
| 41 | 2:10.66–2:12.26 | V3 | C18 | storm clouds | |
| 42 | 2:12.26–2:13.86 | V3 | C09 | band warmer, urgent | |
| 43 | 2:13.86–2:15.99 | V3 | C13 | turns, nothing | |
| 44 | 2:15.99–2:17.59 | V3 | C11 | distant woman, one shot | |
| 45 | 2:17.59–2:19.72 | V3 | C02 | singer less controlled | |
| 46 | 2:19.72–2:21.85 | V3 | C12 | drummer harder | |
| 47 | 2:21.85–2:24.5 | V3 | C13 | listening, haunted | |
| 48 | 2:24.5–2:29.25 | V4 | C14 | opens drawer, hides memory | |
| 49 | 2:29.25–2:34 | V4 | C15 | her face in misted mirror | |
| 50 | 2:34–2:36.85 | V4 | C02 | CU; band swallowed by story | |
| 51 | 2:36.85–2:40.65 | V4 | C16 | face forms in fog | |
| 52 | 2:40.65–2:44.45 | V4 | C15 | he reaches; dissolves to his reflection | |
| 53 | 2:44.45–2:48.25 | V4 | C14 | drawer closes | |
| 54 | 2:48.25–2:53 | V4 | C09 | shadowy band | |
| 55 | 2:53–2:57.12 | PRE2 | C17 | looks up into storm sky | |
| 56 | 2:57.12–3:00.52 | PRE2 | C25 | drummer hands accelerate a tom fill, sticks blur, lightning flickers | |
| 57 | 3:00.52–3:03.82 | PRE2 | C18 | clouds move | |
| 58 | 3:03.82–3:07.22 | PRE2 | C26 | slow dolly push-in toward the band leaning into the build | |
| 59 | 3:07.22–3:10.52 | PRE2 | C12 | band carries the confession | |
| 60 | 3:10.52–3:13.92 | PRE2 | C27 | singer lifts chin and leans into a rising vocal in profile | |
| 61 | 3:13.92–3:17.22 | PRE2 | C02 | I still want you | |
| 62 | 3:17.22–3:20.62 | PRE2 | C28 | bassist sways forward, hand driving low strings, rim light shifts | |
| 63 | 3:20.62–3:23.92 | PRE2 | C17 | stops fighting it | |
| 64 | 3:23.92–3:27.32 | PRE2 | C29 | hands drive hard chords, lightning flash crosses the keys | |
| 65 | 3:27.32–3:30.62 | PRE2 | C20 | band rises | |
| 66 | 3:30.62–3:34 | PRE2 | C30 | whole band rises together at the peak, arms and instruments lifting | |
| 67 | 3:34–3:37 | CH2 | C20 | band | |
| 68 | 3:37–3:39.5 | CH2 | C10 | water | |
| 69 | 3:39.5–3:42 | CH2 | C19 | thunder | |
| 70 | 3:42–3:45 | CH2 | C15 | mirror | |
| 71 | 3:45–3:48 | CH2 | C07 | window reflection | |
| 72 | 3:48–3:51 | CH2 | C21 | clean memory shot, turns away | |
| 73 | 3:51–3:54 | CH2 | C20 | band | |
| 74 | 3:54–3:58 | CH2 | C02 | almost angry at himself | |
| 75 | 3:58–4:03 | BRIDGE | C22 | rainwater spreads across floor | |
| 76 | 4:03–4:06 | BRIDGE | C16 | mirror fogs | |
| 77 | 4:06–4:09 | BRIDGE | C11 | she turns away | |
| 78 | 4:09–4:12 | BRIDGE | C20 | band at peak | |
| 79 | 4:12–4:15 | BRIDGE | C22 | drawer creaks open | |
| 80 | 4:15–4:18 | BRIDGE | C21 | she vanishes | |
| 81 | 4:18–4:21 | BRIDGE | C15 | he reaches for the mirror | |
| 82 | 4:21–4:23.6 | FINAL | C20 | final chorus, band plays out | |
| 83 | 4:23.6–4:26.2 | FINAL | C24 | singer direct, almost still | |
| 84 | 4:26.2–4:29.67 | FINAL | C23 | alone by the window | |
| 85 | 4:29.67–4:31.4 | FINAL | C03 | rain continues | |
| 86 | 4:31.4–4:34 | FINAL | C23 | looks to camera, unresolved (end) | |

**Total: 86 cuts · EDL sum 274.0s (4:34.0) · music end ~273.75s → ~0.25s tail, lands clean.**

---

## Section-time confirmation — CONFIRMED & applied

The mid-song section splits that used to be ambiguous from energy alone are now
**resolved**: the section starts below were **confirmed by the user (P-003)** and
**applied to `data/edl.csv` (P-004)** — every cut is section-synced to these
times. No further input needed here; this block is now a record, not a question.
(Was: an open "confirm with your ear" request.)

| Section | Start (confirmed, applied) | Status |
|---------|----------------------------|--------|
| INTRO | 0:00 | CONFIRMED & applied (P-003 / P-004) |
| V1 | 0:18 | CONFIRMED & applied |
| **V2** | **0:41.25** | CONFIRMED & applied (was EDL-assumed 0:48) |
| **PRE1** | **1:09.75** | CONFIRMED & applied (was EDL-assumed 1:18) |
| **CH1** | **1:29.25** | CONFIRMED & applied (was EDL-assumed 1:43) |
| V3 | 2:08 | CONFIRMED & applied |
| **V4** | **2:24.5** | CONFIRMED & applied (was EDL-assumed 2:39) |
| **PRE2** | **2:53** | CONFIRMED & applied (was EDL-assumed 3:09) |
| CH2 | 3:34 | CONFIRMED & applied |
| BRIDGE | 3:58 | CONFIRMED & applied |
| FINAL | 4:21 | CONFIRMED & applied |

---

## Targeted watch-points (known risk-spots — scrutinize these)

These are the specific things to confirm with a human eye. The clip-content items
were verified by automated analysis (Higgsfield `video_analysis`, not a render),
so this audio render is the **final confidence check**. Sources named per item.

### A. Regenerated clips — light confirm (already on-model-verified)

The 11 earlier-regenerated clips (**C01, C04, C06, C07, C13, C15, C16, C19, C22,
C23, C24**) were regenerated reference-anchored and **re-analyzed on-model**
(`FOOTAGE_AUDIT.md` §8; `data/clips.csv` points at the new jobs, originals in
`data/clips_original_backup.csv`). Treat these as a **light confirm**, not a live
risk — just glance that the fix still reads at the timecode(s) below.

| Clip | What the fix was (confirm it still reads) | Appears at (in–out) |
|------|-------------------------------------------|---------------------|
| **C07** | woman's reflection appears behind his shoulder, raindrop breaks it, empty room (was: woman absent + man shaved) | 0:41.25–0:46 · 0:51.7–0:55.5 · 1:05–1:09.75 · 3:45–3:48 |
| **C23** | turn-to-camera lands, hair present — the film's final shot (was: shaved top + no turn) | 4:26.2–4:29.67 · 4:31.4–4:34 |
| **C06** | empty grey ocean, no people (was: a bald man + a second figure) | 0:27.31–0:30.41 |
| **C22** | empty room with the atmosphere beats (was: an unwanted man) | 3:58–4:03 · 4:12–4:15 |
| **C04** | hair present + reflection kept (known partial: head-turn "as if touched" still static — acceptable read) | 0:11–0:15 · 0:21.1–0:24.98 · 0:38.94–0:41.25 · 1:01.2–1:05 |
| **C13** | lead's hair present, not bald/shaved | 1:13.65–1:16.77 · 2:08–2:10.66 · 2:13.86–2:15.99 · 2:21.85–2:24.5 |
| **C15** | hair present + condensation dissolve (not a digital ripple); woman mirror-face good | 2:29.25–2:34 · 2:40.65–2:44.45 · 3:42–3:45 · 4:18–4:21 |
| **C19** | hair present in the lightning flash (brief, low exposure) | 1:39.71–1:42.82 · 3:39.5–3:42 |
| **C01** | cropped ginger hair, not a buzz cut (band-wide, low visibility) | 0:04–0:08 · 0:24.98–0:27.31 |
| **C16** | woman dark brunette, not auburn/reddish-brown | 2:36.85–2:40.65 · 4:03–4:06 |
| **C24** | warm performance palette + hair on-model | 4:23.6–4:26.2 |

> If any clip drifts off-model again, that's a regen refinement for a later batch
> (`FOOTAGE_AUDIT.md` §5/§8) — but none is expected; these are confirmed fixes.

### B. NEW band coverage C25–C34 — the thing to watch on THIS render

The big change since the last review: **10 new band-performance cuts (C25–C34)**
were generated (P-006) and inserted (P-007), woven into the two sections that used
to **drag**. This is the primary thing to judge on this render — does the new
coverage flow, and does it kill the old slow-pacing?

- **CH1 (now 12 cuts, avg ~3.23s)** — new cuts: **C31** (cut 30, 1:36.51–1:39.71,
  drummer hard CU), **C32** (cut 33, 1:45.93–1:49.13, guitar hands), **C33**
  (cut 36, 1:55.35–1:58.55, second front-singer CU), **C34** (cut 39,
  2:04.77–2:08, keys). The old CH1 5–6.5s holds are **fixed**.
- **PRE2 (now 12 cuts, avg ~3.42s)** — new cuts: **C25** (cut 56, 2:57.12–3:00.52),
  **C26** (cut 58, 3:03.82–3:07.22), **C27** (cut 60, 3:10.52–3:13.92), **C28**
  (cut 62, 3:17.22–3:20.62), **C29** (cut 64, 3:23.92–3:27.32), **C30** (cut 66,
  3:30.62–3:34). The old PRE2 drag (the 5–6.5s C17/C12/C02/C20 holds) is **fixed**.

**Watch for:** does each new band setup read as the same band/room, cut cleanly,
and keep the rising-build energy without feeling like filler?

### C. Two new singer shots — light spot-check (already on-model)

**C27** (cut 60, PRE2, 3:10.52–3:13.92 — singer profile, chin lifting into the
build) and **C33** (cut 36, CH1, 1:55.35–1:58.55 — second front-singer straight
to lens) are the two new shots that show the lead's face. Both were
**`video_analysis`-confirmed ON-MODEL (P-008)** — so this is a **light spot-check**
(does the face match), **not** a likeness risk.

### D. C02 repetition — now broken up by the new coverage

The single singer close-up **C02 still appears 11×** (cuts 3, 6, 12, 15, 19, 25,
35, 45, 50, 61, 74) but the new band coverage now **separates its old back-to-back
runs** in CH1 and PRE2 — C33 and the four new CH1 band cuts sit between C02's
chorus hits, and C25–C30 break up the PRE2 stretch. The old "C02 reads as
repetitive / overused" concern should be **largely resolved** by the new setups;
confirm the repeats now feel like a motif, not a recycle.

`0:08 · 0:18 · 0:36.61 · 0:46 · 0:58.35 · 1:19.89 · 1:52.24 · 2:17.59 · 2:34 · 3:13.92 · 3:54`

### E. The FINAL ending — does it resolve cleanly? (corrected)

**Corrected:** the old "EDL runs ~2s longer than the mix → mix caps at 274s → ~2s
hard truncation" is **gone**. The EDL is now **274.0s** and the Jun-27 mix ends at
**~273.75s**, so the final **C23 hold (cut 86, 4:31.4–4:34.0)** runs essentially
to the music end with only a **~0.25s** tail — the "looks to camera, unresolved"
beat lands clean, not clipped. **Watch the very end: does the last shot resolve on
the music?** (No upstream trim is needed anymore.)

### F. Likeness face-match seams — identity continuity at adjacent cuts

The lead's face comes from two still families (warm band / cool story); the risk
is at the cuts where they meet. Source: `REVIEW.md` §5. Scrutinize whether it
reads as **the same man** across each seam (timecodes derived from the current
table):

- **INTRO/V1:** `0:04 C01 → 0:08 C02 → 0:11 C04` (band-face → singer-face → story-face).
- **FINAL:** `4:23.6 C24 → 4:26.2 C23` — the **last impression of him**; the worst
  place for a mismatch. (Since C02 repeats 11×, also confirm C02's likeness is
  your best singer take — any error there repeats all 11 times.)

---

## What happens next (where this checklist routes)

| Checklist output | Feeds into |
|------------------|------------|
| **New-coverage pacing verdict** (watch-point B; C25–C34 in CH1/PRE2) | Beat-lock fine-tuning if any new cut feels off-grid — the section spans are fixed (P-004), so only intra-section durations would shift. |
| **Ending-resolution verdict** (watch-point E) | Confirmation only — the 2s truncation is already resolved (274.0s EDL vs ~273.75s mix). No trim packet pending. |
| **Any remaining off-model reads** (watch-points A, C, F) | Optional **regen refinement** (e.g. C04's static head-turn, or a trained Soul for a perfect face-lock) — `FOOTAGE_AUDIT.md` §5/§8. |
| **C02-repetition flags** (watch-point D) | Already addressed by the C25–C34 batch; only revisit if a specific C02 hit still reads recycled. |

Cross-references: `FOOTAGE_AUDIT.md` (§5 likeness, §8 regeneration-done),
`BAND_COVERAGE_PLAN.md` (C25–C34 spec), and `REVIEW.md` (§1 C02 overuse, §5
likeness seams). For a quick silent visual pass before the Mac render, open
`preview.html`.
