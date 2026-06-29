# Render-Review Checklist — "When It Rains" rough cut

**What this is.** A watch-once checklist for the rendered rough cut. It lists all
**76 EDL cuts in playback order** with their running in→out timecode, so you can
flag failures by **timecode + cut index + clip key** while you watch. The output
of this pass feeds the next packets (beat-lock the EDL, the 2s FINAL trim, the
optional band-coverage batch).

**How to use it.**
1. Render the rough cut on your Mac (`scripts/fetch_assets.sh` then
   `scripts/assemble_rough_cut.sh` — see `REVIEW.md` Step 0).
2. Watch it **once, straight through, in playback order.** Don't scrub.
3. For each cut, mark the **PASS / FAIL (reason)** cell: `PASS`, or
   `FAIL — <one-line reason>`. Note anything by its timecode so the fix list
   writes itself.
4. Then run the **Targeted watch-points** pass (below) for the known risk-spots,
   and fill the **Section-time confirmation** block.

**Target runtime.** The music resolves at **~4:34** (this Jun-27 mix; the
assembler caps audio at 274s). Heads-up: the EDL itself sums to **276.0s
(≈4:36)** — that 2-second overhang is the known FINAL truncation (see the
watch-points and `FOOTAGE_AUDIT.md` §6). The timecodes in the table below are the
**EDL's own running times** (cut 1 in = 0:00; each out = in + duration), so the
last cut reads 4:33–4:36 even though playback will stop ~2s sooner.

---

## Per-cut checklist (all 76 cuts, playback order)

Mark each row PASS or FAIL with a one-line reason.

| # | In–Out | Section | Clip | EDL note | PASS / FAIL (reason) |
|---|--------|---------|------|----------|----------------------|
| 1 | 0:00–0:04 | INTRO | C03 | rain on glass (open) | |
| 2 | 0:04–0:08 | INTRO | C01 | band room wakes | |
| 3 | 0:08–0:11 | INTRO | C02 | singer close-up | |
| 4 | 0:11–0:15 | INTRO | C04 | man alone by window | |
| 5 | 0:15–0:18 | INTRO | C03 | rain hold into verse | |
| 6 | 0:18–0:22 | V1 | C02 | sings opening line | |
| 7 | 0:22–0:27 | V1 | C04 | turns as if touched; reflection dissolves | |
| 8 | 0:27–0:30 | V1 | C01 | restrained band | |
| 9 | 0:30–0:34 | V1 | C06 | grey ocean | |
| 10 | 0:34–0:38 | V1 | EX1 | gazes at ocean through glass | |
| 11 | 0:38–0:42 | V1 | C05 | river bend | |
| 12 | 0:42–0:45 | V1 | C02 | singer | |
| 13 | 0:45–0:48 | V1 | C04 | window | |
| 14 | 0:48–0:53 | V2 | C07 | over shoulder; her reflection surfaces | |
| 15 | 0:53–0:56 | V2 | C02 | face-on singing | |
| 16 | 0:56–0:59 | V2 | C03 | rain behind him | |
| 17 | 0:59–1:03 | V2 | C07 | raindrop breaks reflection; empty room | |
| 18 | 1:03–1:06 | V2 | C09 | band fragments | |
| 19 | 1:06–1:09 | V2 | C02 | more direct | |
| 20 | 1:09–1:13 | V2 | C04 | window | |
| 21 | 1:13–1:18 | V2 | C07 | reflection again, gone | |
| 22 | 1:18–1:23 | PRE1 | C08 | curtains breathe; trees move | |
| 23 | 1:23–1:27 | PRE1 | C13 | almost turns toward a sound | |
| 24 | 1:27–1:31 | PRE1 | C09 | drummer enters, build | |
| 25 | 1:31–1:34 | PRE1 | C02 | it's like you never left | |
| 26 | 1:34–1:38 | PRE1 | C08 | trees move | |
| 27 | 1:38–1:43 | PRE1 | C09 | push-in, intensity rising | |
| 28 | 1:43–1:47 | CH1 | C12 | band release | |
| 29 | 1:47–1:50 | CH1 | C10 | puddle reflection trembles | |
| 30 | 1:50–1:53 | CH1 | C19 | thunder flash | |
| 31 | 1:53–1:56 | CH1 | C11 | woman from behind, gone | |
| 32 | 1:56–1:59 | CH1 | C12 | band | |
| 33 | 1:59–2:02 | CH1 | C02 | chorus with force | |
| 34 | 2:02–2:05 | CH1 | C10 | water again | |
| 35 | 2:05–2:08 | CH1 | C12 | band | |
| 36 | 2:08–2:13 | V3 | C13 | turns toward window at thunder | |
| 37 | 2:13–2:16 | V3 | C18 | storm clouds | |
| 38 | 2:16–2:19 | V3 | C09 | band warmer, urgent | |
| 39 | 2:19–2:23 | V3 | C13 | turns, nothing | |
| 40 | 2:23–2:26 | V3 | C11 | distant woman, one shot | |
| 41 | 2:26–2:30 | V3 | C02 | singer less controlled | |
| 42 | 2:30–2:34 | V3 | C12 | drummer harder | |
| 43 | 2:34–2:39 | V3 | C13 | listening, haunted | |
| 44 | 2:39–2:44 | V4 | C14 | opens drawer, hides memory | |
| 45 | 2:44–2:49 | V4 | C15 | her face in misted mirror | |
| 46 | 2:49–2:52 | V4 | C02 | CU; band swallowed by story | |
| 47 | 2:52–2:56 | V4 | C16 | face forms in fog | |
| 48 | 2:56–3:00 | V4 | C15 | he reaches; dissolves to his reflection | |
| 49 | 3:00–3:04 | V4 | C14 | drawer closes | |
| 50 | 3:04–3:09 | V4 | C09 | shadowy band | |
| 51 | 3:09–3:14 | PRE2 | C17 | looks up into storm sky | |
| 52 | 3:14–3:18 | PRE2 | C18 | clouds move | |
| 53 | 3:18–3:22 | PRE2 | C12 | band carries the confession | |
| 54 | 3:22–3:26 | PRE2 | C02 | I still want you | |
| 55 | 3:26–3:30 | PRE2 | C17 | stops fighting it | |
| 56 | 3:30–3:34 | PRE2 | C20 | band rises | |
| 57 | 3:34–3:37 | CH2 | C20 | band | |
| 58 | 3:37–3:39.5 | CH2 | C10 | water | |
| 59 | 3:39.5–3:42 | CH2 | C19 | thunder | |
| 60 | 3:42–3:45 | CH2 | C15 | mirror | |
| 61 | 3:45–3:48 | CH2 | C07 | window reflection | |
| 62 | 3:48–3:51 | CH2 | C21 | clean memory shot, turns away | |
| 63 | 3:51–3:54 | CH2 | C20 | band | |
| 64 | 3:54–3:58 | CH2 | C02 | almost angry at himself | |
| 65 | 3:58–4:03 | BRIDGE | C22 | rainwater spreads across floor | |
| 66 | 4:03–4:06 | BRIDGE | C16 | mirror fogs | |
| 67 | 4:06–4:09 | BRIDGE | C11 | she turns away | |
| 68 | 4:09–4:12 | BRIDGE | C20 | band at peak | |
| 69 | 4:12–4:15 | BRIDGE | C22 | drawer creaks open | |
| 70 | 4:15–4:18 | BRIDGE | C21 | she vanishes | |
| 71 | 4:18–4:21 | BRIDGE | C15 | he reaches for the mirror | |
| 72 | 4:21–4:24 | FINAL | C20 | final chorus, band plays out | |
| 73 | 4:24–4:27 | FINAL | C24 | singer direct, almost still | |
| 74 | 4:27–4:31 | FINAL | C23 | alone by the window | |
| 75 | 4:31–4:33 | FINAL | C03 | rain continues | |
| 76 | 4:33–4:36 | FINAL | C23 | looks to camera, unresolved (end) | |

**Total: 76 cuts · EDL sum 276.0s (≈4:36) · playback caps ≈4:34.**

---

## Section-time confirmation (needed before beat-lock)

The section-boundary energy transitions line up with the EDL at V1 (~0:19),
V3 (~2:10), CH2 (~3:31), BRIDGE (~3:56), FINAL (~4:16) — but the **mid-song
splits are ambiguous from energy alone** and need your ear (per `HANDOFF.md`
Open threads #2 and `REVIEW.md` §9). Confirm or correct the start times below;
on your word the EDL gets regenerated to snap every cut onto the 0.98s beat grid.

| Section start to confirm | EDL-assumed start | Confirmed start (your ear) |
|--------------------------|-------------------|----------------------------|
| **V2** | 0:48 | |
| **PRE1** | 1:18 | |
| **CH1** | 1:43 | |
| **V4** | 2:39 | |
| **PRE2** | 3:09 | |

If a confirmed time differs from the EDL-assumed start, note the offset so the
beat-lock pass can shift the affected cuts.
