# WHEN IT RAINS — THE ROADMAP
### Likeness lock + story logic + full-film production plan
*(written 2026-07-02 after user notes on v2_v1: "clips moved away from looking
exactly like me" and "the story seems to not be moving forward in an explicit
logical pattern." Nothing generates until this is reacted to.)*

---

## PART 1 — HONEST DIAGNOSIS

### 1a. Why the likeness drifted
The one TRUE likeness anchor is the ORIGINAL hero clip (`491e39d1`, user:
"looks most like me") plus the user-approved masters (bed `2d080b77`, the
gated kitchen and street masters). Drift crept in through four mechanisms:

1. **Soul seed variance.** Every soul_2 still is a fresh sample of the face.
   Some samples land close to the anchor; some come out gaunter, older,
   more-shaved, longer-faced. We accepted the FIRST sample every time instead
   of sampling several and picking the closest.
2. **Nano edit-chain depth.** Surgical edits re-encode the whole image. The V1
   kitchen master went through SIX passes; the V2 stills through two or three
   each. Each pass is small; stacked, the face softens and shifts.
3. **Animation + upscale transforms.** kling movement and the 2K upscale each
   re-interpret the face; a slightly-off still becomes more-off in motion.
4. **QC gap.** My frame QC checked the bible (hairline, chain, ring, text)
   but likeness was judged "reads as him" from memory — never side-by-side
   against the anchor. Subjective drift passes a memory check.

### 1b. Why the story feels static
Intro = alone at home. V1 = alone in the kitchen. V2 = alone on the street.
Three sections, one identical emotional beat: absence + rain + restraint.
Beautiful wallpaper — but nothing CHANGES. A film moves when each scene
changes what the hero SEES, KNOWS, or DOES, and the next scene happens
BECAUSE of it. That causal chain is what's missing, and it's what Part 3
builds explicitly.

---

## PART 2 — THE LIKENESS LOCK (system, mandatory from now on)

1. **THE ANCHOR BOARD.** A fixed reference strip committed at
   `review/ANCHOR_BOARD.png`: face crops from (a) the original hero clip
   frame, (b) bed master `2d080b77`, (c) the user's training photos' closest
   approved still. EVERY new face asset gets a side-by-side crop pasted next
   to the board and inspected in the review loop. "Reads as him from memory"
   is dead; comparison is the law.
2. **CANDIDATE BATCHES.** Every new master/sync still generates with
   `count: 3-4`. I pick the closest to the anchor board; the user gates my
   pick. Stills are cheap; re-shooting scenes is not.
3. **FACE-CHAIN CAP.** Max 2 nano passes on any frame containing his face.
   Scrubs get batched into one pass (proven pattern). If a frame needs a 3rd
   pass, we regenerate from Soul instead.
4. **CHAIN CHECK STAYS STANDING** (the Soul learned the necklace from a
   training photo; every still gets the zoom check).
5. **SYNC-STACK QC**: raw wan output face-crop compared against its OWN input
   still AND the anchor board before the 2K spend.
6. **DELIVERED-CUT REPAIR RULE.** Locked cut TIMINGS are never at risk: the
   render scripts stay; a repaired asset just swaps a URL and re-renders.
   Fixing likeness never un-locks a cut's shape.

---

## PART 3 — THE STORY BIBLE (the explicit logical pattern)

### The one-sentence engine
A man wakes up alone, keeps almost-seeing the woman he lost in every
reflective surface, chases the sightings harder and harder until the rain
peaks — and when it clears he chooses to stop chasing and keep the wondering.

### The escalation ladder of HER (the spine — each rung is a story event)
| Rung | Her visibility | Where |
|---|---|---|
| 0 | Pure absence (objects only: her pillow, second mug) | INTRO, V1 |
| 1 | Ambiguous shape, gone in a blink | INTRO window (locked) |
| 2 | He LOOKS for her but sees nothing | V2 shoulder-look (delivered) |
| 3 | Signs without her (world echoing: trees, breath) | PRE1 |
| 4 | FIRST TRUE SIGHTING — reflection in the cafe glass | CH1 (locked chorus) |
| 5 | He starts searching deliberately — and finds her things instead | V3/V4 |
| 6 | Almost-her strangers; following; wrong faces | PRE2 |
| 7 | She is EVERYWHERE — every surface at once | CH2 |
| 8 | The flood: he stops chasing; the sightings stop WITH him | BRIDGE |
| 9 | Chosen memory: he looks at the glass ON PURPOSE — and it's just glass, and that's survivable | FINAL |

### Per-section beats — with the EXPLICIT DELTA each one must land
Format: **section (song time) — scene — what happens — WHAT CHANGES.**

- **INTRO (0–23.5) — bedroom — LOCKED (intro_v6).** Wakes beside her untouched
  half; sings the first line at the window; a shape that could be her flashes
  in the glass. **Δ: the audience learns the premise; HE half-sees something
  for the first time.**
- **V1 (23.5–43) — kitchen — DELIVERED (v1_v1), one repair to board.** The
  two-mugs habit; puts one back. **Δ as cut: absence lives in his hands, not
  just the room. ROADMAP ADDITION (cheap, one insert swap): as he closes the
  cupboard door, its GLASS/gloss catches a half-second smear of a figure —
  rung 0.5. He doesn't see it; WE do. Now V1 pushes the ladder instead of
  repeating the intro.**
- **V2 (43–70.3) — street — DELIVERED (v2_v1), one repair to board.** He
  looks back over his shoulder — the first time he LOOKS on purpose — and
  the world refuses to stop with him. **Δ as cut: the searching begins.
  ROADMAP ADDITION (one insert swap): in the puddle button at the end, for
  ~12 frames a second reflection stands beside his — gone when a drop hits.
  He almost catches it. Cause → effect: THIS is why PRE1's dread rises.**
- **PRE1 (70.3–89.8) — the walk darkens — TO BUILD (P-023).** "Don't know if
  you still feel it / I lose my breath / the trees are moving / like you never
  left." He walks faster; wind moves the trees like someone passing; he stops
  — breath fogging — turns around ON the line "like you never left": empty
  street. **Δ: the signs are now chasing HIM. He decides to go somewhere
  (the cafe) — giving CH1 a cause.**
- **CH1 (89.8–~102) — the cafe — LOCKED (chorus_v16).** The reflection in the
  glass case. He turns: no one. **Δ: rung 4 — the first true sighting. After
  this he can't pretend it's nothing.**
- **V3/V4 (~102–133) — home again, searching — TO BUILD (P-024).** BECAUSE of
  the sighting he goes home and does what he's avoided: opens the closet
  (her side: empty hangers + ONE dress), the drawer (her things), the hallway
  mirror he's kept turned away — and turns it BACK. Nothing in it but him.
  **Δ: he stops avoiding and starts confronting; we finally see EVIDENCE of
  her reality (her things) — she was real, not a metaphor.**
- **PRE2 (~133–152) — following — TO BUILD (P-025).** A figure with her hair
  ahead in the rain; he follows; she turns at the crossing — a stranger's
  face (bible: her true face still never shown; the stranger is clearly NOT
  her). Sky churns. **Δ: the chase peaks and FAILS. The sightings cannot be
  caught.**
- **CH2 (~152–164) — everywhere — TO BUILD (P-026), chorus grammar reprise.**
  The chorus method again but multiplied: her oblique in bus glass, shop
  glass, standing water — cut on the grid, faster than CH1. **Δ: rung 7 —
  full haunting. It cannot continue; something must break.**
- **BRIDGE (~164–187) — the waterfront flood — TO BUILD (P-027).** Rain peaks.
  He stands at the water (banked exterior through-glass camera idea lands
  here or FINAL). He stops. Lets the rain hit. The reflections in the water
  are ONLY him. **Δ: he stops chasing — and the world stops showing her.
  The ghost was the chase.**
- **FINAL CH (~187–273) — return + resolution — TO BUILD (P-028).** "And I
  still wonder." Home, drier light. He takes the second mug OUT of the
  cupboard and sets it on the counter — not out of habit this time, but as a
  choice: the remembering is allowed now. At the window (bookending line 1)
  he looks at the glass on purpose — just glass, just rain easing. Hold.
  **Δ: acceptance without closure — the title argument: when it rains, he'll
  still wonder, and he can live there.** (Payoffs: mugs plant from V1;
  window/shape plant from INTRO; the hero performance clip carries the last
  chorus hooks.)

### Story rules (checkable, every future board)
1. Every section states its Δ in ONE sentence before anything generates.
2. Every section is CAUSED by the previous one (the board must say "because").
3. Her escalation only moves UP the ladder until the BRIDGE, then stops.
4. Her face: never literal (bible). The PRE2 stranger is explicitly not-her.
5. Objects carry memory: mugs (V1→FINAL), pillow (INTRO), mirror/dress
   (V3/V4), water rings (V2→BRIDGE). Every plant pays off exactly once.

---

## PART 4 — PRODUCTION PLAN

### Packet order (each = board → user reacts → master(s) w/ candidate batches
### → likeness-gate → takes → sync stack → cut → QC → deliver → lock → receipt)
| Packet | Section | Scene | Est. credits |
|---|---|---|---|
| P-022 | Likeness repair V1+V2 + ladder inserts | anchor board, 2-3 stills re-picked, 2 insert swaps, re-renders | ~120-180 |
| P-023 | PRE1 | the darkening walk | ~150-200 |
| P-024 | V3/V4 | closet/drawer/mirror | ~200-250 |
| P-025 | PRE2 | the following / stranger | ~150-200 |
| P-026 | CH2 | everywhere (chorus reprise) | ~150-200 |
| P-027 | BRIDGE | the waterfront flood | ~200-250 |
| P-028 | FINAL | return, mug choice, window bookend | ~200-250 |
| P-029 | FULL ASSEMBLY | 0:00–4:34 single file + polish pass | CI only |

Credits remaining: roughly 1300–1500 of 2415. The plan above fits with
~10-15% reserve. If a section runs hot, the reserve protects BRIDGE/FINAL
(the emotional payload).

### Checkpoints for the user (phone-sized)
- After P-022: repaired v1/v2 + a stitched first 70 seconds.
- After P-024: stitched first ~2:13 (through V3/V4).
- After P-026: stitched first ~2:45.
- After P-028: the full film.

---

## PART 5 — WHAT I NEED FROM YOU BEFORE ANYTHING RUNS
1. **Which clips read most off-likeness?** My suspects: the V2 street master
   face (gaunt) and curb hold, possibly the V1 mug-take mid-frames. Naming
   them focuses the repair.
2. **React to the ladder + per-section deltas** (Part 3) — especially the two
   cheap V1/V2 ladder inserts, the V3/V4 closet/mirror scene, the PRE2
   stranger reveal, and the FINAL mug-choice ending.
3. **Confirm the checkpoint cadence** (or ask for every section like now).
