# PRE1 SCENE SPEC — "the darkening walk" (70.3–89.8) — P-024 BOARD
### STATUS: BOARD — awaiting user reaction. Nothing generates until reacted to.

**Δ (one sentence):** The signs stop waiting for him and start chasing HIM —
wind moves the trees like someone passing, his breath catches, he turns on
"like you never left" to an empty street — and he decides to GO somewhere
(the cafe), giving CH1 its cause.

**Because:** V2 ended with the almost-catch (second reflection in the puddle,
rippled apart). PRE1 is him walking AWAY from that puddle, rattled, and the
world escalating behind him.

---

## Beat grid (beat-locked, from line_map.json)
| Slot | Song time | Line | Shot |
|---|---|---|---|
| A | 70.31–74.22 (3.90) | "don't know if you still feel it" | THE WALK (take 1, part 1) |
| B | 74.22–78.12 (3.90) | "I lose my breath" | take 1, part 2: he slows — BREATH FOG close beat |
| C | 78.12–82.02 (3.90) | "the trees are moving" | TREES INSERT: gust moves dark branches like someone passing |
| D | 82.02–89.82 (7.80) | "like you never left" | THE TURN — lip-sync: he spins to camera, empty street behind, sings the line; last beat he exits frame WITH PURPOSE |

Cut rhythm: A and B are one continuous take (cut away to C, back into the
same take is NOT needed — B ends the take at the stop+breath); C is a
no-face insert; D is the section's single sync shot (pattern: one sync per
section, like V1 kitchen / V2 awning).

## Scene canon
- Same morning as V2, MINUTES LATER, a block further from home: the street
  gains TREES (dark, heavy with rain) — new visual element that motivates C.
- DARKENING: heavier rain than V2, darker sky, wind visible (rain angle,
  moving branches, his jacket flapping at the hem).
- WARDROBE LOCKED (continuity + hard rule): dark rain jacket ZIPPED over grey
  hoodie — chest completely covered, NO skin below the chin, dark jeans.
  Neck bare — NO chain. Hands bare — NO ring. NEVER the word "open".
- Bible: buzzed red-blonde hair, full hairline, reddish stubble; restrained.
  NO text/signage anywhere. No other people's faces (blurred/umbrella'd only).
- Grade: V2's muted 35mm documentary palette, one notch darker.

## Masters (candidate batches count 3-4; user gates every pick vs ANCHOR_BOARD)
- **M1 — WALK master:** medium-wide, him mid-stride toward camera on the
  tree-lined wet sidewalk, faster energy than V2's exit, eyes down/ahead,
  mouth closed. (Drives take 1.)
- **M2 — TURN master:** chest-up, he has just spun to face the camera,
  feet planted, breath-fog faint at his lips, empty tree-lined street
  receding behind him, quiet alarm in the eyes, mouth gently closed about to
  sing. (Drives the wan sync.) Realism recipe from P-023 (RAW candid 35mm
  documentary phrasing) — it produced the two best faces yet.
- **Trees insert still:** DERIVED from M1's environment (nano reframe onto
  the trees, remove him) — dark branches over the sidewalk, rain streaking
  through. No face → no likeness gate, standard QC only.

## Takes
- **T1 (kling, 10s, from M1):** FIRST he walks toward camera at a clip,
  jacket hem flapping, rain heavier than before; THEN he slows over two
  steps and STOPS, chest rising, a visible fog of breath; his eyes lift.
  Locked camera. (Slots A+B; cut at the beat.)
- **T2 (kling, 5s, from trees still):** locked camera; ONE hard gust rolls
  through the branches left-to-right, like something passing; leaves shed
  rainwater; nothing else changes, no one appears.
- **T3 (wan lip-sync, ~8s, from M2):** sings "like you never left" from the
  very first beat, restrained but urgent, minimal head movement; in the
  final two seconds his eyes harden with decision and he steps out of frame
  left — the street behind him stays empty. (Slot D; vocal slice
  pre1_line12 = song 82.0 + 7.9s. Onset-tight per P-023 law; frame-QC then
  2K.)

## Cut (render_pre1.sh)
- 70.3–74.2 T1 walk portion → 74.2–78.1 T1 stop+breath portion (in-points
  measured from frames) → 78.1–82.0 T2 trees → 82.0–89.8 T3 sync 2K at
  in-point = slot_start − slice_start = 0.10 if slice starts 81.9 (cut
  exact when slice exists). Grain VF chain identical to v1/v2 scripts.
- Checkpoint deliverable: pre1_v1.mp4 (19.5s) + restitched first90.mp4
  (intro + V1 + V2 + PRE1) once the bed audio exists.

## BLOCKER — audio (needs user)
song.mp3 is NOT in this container (gitignored; the old session's upload is
gone). Needed before T3 and the cut:
- pre1_bed.mp3 (70.3–89.8 full mix) and pre1_line12.mp3 (82.0+7.9 vocal).
**User: re-attach When_It_Rains__Jun_27_mix.mp3** — masters and T1/T2 can
proceed meanwhile; the sync stack waits for the slices.

## Estimate
Roadmap: ~150-200 credits. Expected spend: 2 master batches (6-8 soul_2
stills) + 1-2 nano derivations + 2 kling takes (10s+5s) + 1 wan ~8s + 1
bytedance 2K + scrubs as needed. P-023's actuals suggest this lands well
under the roadmap ceiling.
