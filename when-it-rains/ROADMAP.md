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
> **CLOCK CORRECTED (verified against analysis/line_map.json).** The times in
> the beats below were re-timed after the director review caught that the
> original ROADMAP guessed them. The authoritative section clock:
> INTRO 0–19.6 · V1 19.6–43.0 · V2 43.0–70.3 · PRE1 70.3–89.8 ·
> **CH1 89.8–132.7 (42.9s)** · **V3 132.7–148.3 · V4 148.3–183.4 (V3/V4 = 50.7s)** ·
> **PRE2 183.4–214.6 (31.2s)** · **CH2 214.6–238.1 (23.4s)** ·
> **BRIDGE 238.1–257.6 (19.5s)** · **FINAL 257.6–273.8 (16.2s)**.
> (Packet IDs in this doc are historical and have since drifted — go by section
> name, not P-number.) Grade every "her" beat below against APPARITION_STANDARD.md.

- **CH1 (89.8–132.7, 42.9s) — the cafe — chorus_v16 covers only 89.8–~102.**
  The reflection in the glass case. He turns: no one. **Δ: rung 4 — the first
  true sighting.** **RE-TIME CONSEQUENCE: the locked chorus is only the first
  ~12s; CH1 needs a PLAN for 102–132.7 (~30s more of chorus).** Cheapest: the
  hero-performance clip returns as a motif (2–3 recuts, wider/wetter) carrying
  the repeated hook, intercut with 1–2 fresh cafe-reflection beats. This also
  fixes the reviewer note that CH1 "starves its own chorus."
- **V3/V4 (132.7–183.4, 50.7s) — home again, searching.** BECAUSE of the
  sighting he goes home and does what he's avoided: opens the closet (her side:
  empty hangers + ONE dress), the drawer (her things), the hallway mirror he's
  kept turned away — and turns it BACK. Nothing in it but him (rung 5,
  audience-only per the sees-chart — he confronts, does not catch).
  **NEW PLANT (director note): the drawer also holds a PHOTO of the waterfront
  — the place she loved. He looks at it a beat too long. This one insert is the
  cheapest fix in the plan: it explains WHY the BRIDGE happens at the water,
  and it aims PRE2 (the following becomes a pilgrimage toward that place).**
  **Δ: he stops avoiding and starts confronting; we see EVIDENCE she was real
  (her things), and the waterfront is planted for the ending.** 50.7s is long —
  budget it as V3 (132.7–148.3, the closet/drawer) + V4 (148.3–183.4, the
  mirror + the "I'm trying to forget you" hold, which the reviewer suggests
  using for him shutting it all again — and failing).
- **PRE2 (183.4–214.6, 31.2s) — following.** A figure with her hair ahead in
  the rain, moving toward the waterfront (the photo's payoff begins); he
  follows; she turns at the crossing — a stranger's face (bible: her true face
  still never shown; clearly NOT her). Sky churns. **Δ: the chase peaks and
  FAILS.** (rung 6; the wrong-face reveal must read — hair cue present then
  broken.)
- **CH2 (214.6–238.1, 23.4s) — everywhere — chorus grammar reprise.** The
  chorus method multiplied: her oblique in bus glass, shop glass, standing
  water — cut on the grid, faster than CH1. **Give CH2 two hero-sync slots and
  put the closet DRESS on its reflections** (director note — 23s of empty
  surfaces at the loudest music will flatline). **Δ: rung 7 — full haunting.**
- **BRIDGE (238.1–257.6, 19.5s) — the waterfront flood.** Rain peaks. He
  arrives at the water (the waterfront from the drawer photo — payoff). He
  stops. Lets the rain hit. The reflections in the water are ONLY him.
  **Δ: he stops chasing — and the world stops showing her. The ghost was the
  chase.** (rung 8.)
- **FINAL CH (257.6–273.8, 16.2s) — return + resolution.** "And I still
  wonder." **NOTE: 16s, not the ~86s the old ROADMAP assumed — this must land
  FAST.** Home, drier light. He takes the second mug OUT of the cupboard and
  sets it on the counter — a choice, not a habit. At the window (bookending
  line 1) he looks at the glass on purpose — just glass, just rain easing.
  Hold. **Δ: acceptance without closure — when it rains, he'll still wonder,
  and he can live there.** (rung 9. Payoffs: mugs from V1; window/shape from
  INTRO; waterfront from V3/V4; hero clip carries the last hooks.)

### Story rules (checkable, every future board)
1. Every section states its Δ in ONE sentence before anything generates.
2. Every section is CAUSED by the previous one (the board must say "because").
3. Her escalation only moves UP the ladder until the BRIDGE, then stops.
4. Her face: never literal (bible). The PRE2 stranger is explicitly not-her.
5. Objects carry memory: mugs (V1→FINAL), pillow (INTRO), mirror/dress
   (V3/V4), water rings (V2→BRIDGE), **waterfront photo (V3/V4→PRE2→BRIDGE)**.
   Every plant pays off exactly once.
6. **Every "her" sighting is graded against `APPARITION_STANDARD.md` before it
   ships** (five requirements + the he-sees/we-sees chart). The sightings are
   the engine; if they don't read on a phone, the film is just a man in the
   rain. This is the #1 must-fix from the director review.

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

### Checkpoints for the user (phone-sized) — times corrected
- DONE: first 90s delivered (through PRE1), 1080p, faces canonical (awning
  pending). CH1 chorus (89.8–~102) + intro locked.
- After V3/V4: stitched first **~3:03** (through 183.4s).
- After CH2: stitched first **~3:58** (through 238.1s).
- After FINAL: the full film (**4:34 / 273.8s**).

> **Build-order note:** CH1 still needs its 102–132.7 extension (~30s) built
> before the film is continuous past the locked chorus — sequence that with or
> before V3/V4. See the CH1 beat above.

---

## PART 5 — WHAT I NEED FROM YOU BEFORE ANYTHING RUNS
1. **Which clips read most off-likeness?** My suspects: the V2 street master
   face (gaunt) and curb hold, possibly the V1 mug-take mid-frames. Naming
   them focuses the repair.
2. **React to the ladder + per-section deltas** (Part 3) — especially the two
   cheap V1/V2 ladder inserts, the V3/V4 closet/mirror scene, the PRE2
   stranger reveal, and the FINAL mug-choice ending.
3. **Confirm the checkpoint cadence** (or ask for every section like now).
