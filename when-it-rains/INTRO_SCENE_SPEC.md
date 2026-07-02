# INTRO SCENE — LOCKED as intro_v6 (user: "Amazing", 2026-07-02)

Per PRODUCTION_PLAYBOOK.md. Final shape after three director rounds: the ghost
is RATIONED (intro = ambiguous shape only; the cafe stays the first unambiguous
her; chorus = everywhere); mugs relocated to V1 as a handled action.

## The room (fixed geometry) — FINAL: DOUBLE bed (user call)
- His bedroom, grey rainy morning. A QUEEN/DOUBLE bed with charcoal-grey
  bedding: HIS half slept-in, HER half made, tucked, untouched — the pillow
  no one slept on. Dark-framed two-pane window above the bed onto a grey
  street (concrete building, white road markings). ALL bedroom assets derive
  from the approved BED MASTER (soul_2 job 2d080b77) — never fresh prompts.
- (History: a single-bed + face-down-frame variant was tried in v4 and killed —
  the fresh-prompt insert didn't match the room and the single bed broke the
  "her side" story. The face-down photo beat remains AVAILABLE as a plant for
  the final chorus if wanted, but it must be derived from a scene master.)
- Wardrobe: plain dark t-shirt (slept in). Bare hands, NO ring.
- Body-state law: his body exists ONLY in (a) the BED take and (b) the WINDOW
  take. Inserts contain no part of him.

## LOCKED asset IDs (intro_v6 = render_intro_v6.sh)
- BED MASTER still (user-approved likeness): soul_2 `2d080b77`
- Opening rain-on-glass = the bedroom's OWN window: nano-derived still
  `c63df6d2` -> kling 8s `371791eb`
- BED take (10s, still 0-6 / head-turn 6.5-7.5 / rise 8.5-10, frame-measured):
  kling `eea03072`
- HER-HALF insert (tight close, pillow no one slept on): nano chain
  `9924df64` -> `f64ef24d` -> kling 5s `8bd72a9d`
- V1 window take `2280a662`; SYNC line (wan2_7 + 2K aigc) `24c8dda3`;
  maybe-her shape still `f4405992`; audio `audio_relay/intro_open24.mp3`

## Cuts (downbeats: 0.1 / 4.0 / 7.9 / 11.8 / 15.7; V1 line 1 at ~19.6)
1. **0:00–0:06 — RAIN ON GLASS (long hold).** The film's first breath: rain
   running down the dark window pane, grey street beyond, no people. Patience
   is the contract.
2. **0:06–0:12 — BED TAKE, beat 1.** Him lying awake on his back, eyes open,
   staring at the ceiling; his head slowly turns toward HER empty half.
   (Face clearly visible; restrained.)
3. **0:12–0:15 — INSERT (his eyeline, no him).** Tight close on HER half:
   the plumped, undisturbed pillow and smooth tucked duvet — the pillow no
   one slept on. Look → see → react; the rise is the reaction.
4. **0:15–0:18 — BED TAKE, beat 2 (same take).** He sits up / rises, heavy,
   toward the window light.
5. **V1 opens (~0:18–0:22) — THE WINDOW + the AMBIGUOUS shape.** He stands at
   the rain-streaked window; exactly on "when it rains I think I feel you," a
   faint SHAPE in the glass beside his reflection that COULD be her — held
   ~1.5s at low opacity (empty-plate composite, GHOST_OPACITY ~0.30) — gone
   when he refocuses. Deliberately unreadable: the audience asks "was it?"
   The cafe later answers.

## Relocated to V1 (morning routine)
The TWO MUGS beat is an ACTION: he takes two mugs down out of habit, stops,
puts one back. Handled objects over still lifes. (Board with V1's spec.)

## Assets to generate
- ATM_rainglass: rain on the dark window pane (no people; nano still + kling)
- BED master (soul_2): him lying awake, face visible (single bed)
- BED take (kling 10s): staring -> head turns -> (later) rises — FIRST/THEN choreography
- INSERT_nightstand (nano still + kling, no him): face-down frame on the
  nightstand, glass of water, rain-shadow light (replaces the dead bedside insert)
- WINDOW master (soul_2): him at the window, grey light, from three-quarter behind
- WINDOW empty plate + shape layer for the ambiguous-reflection composite
