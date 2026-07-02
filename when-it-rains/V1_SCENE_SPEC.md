# V1 SCENE — THE KITCHEN (23.5–43.0s, boarded; user: "Go if you like it")

Per PRODUCTION_PLAYBOOK.md (laws 0/0b apply: derive from the master, frame-QC
every asset). Story job: the morning continues; the absence lives in OBJECTS.
The ghost stays RATIONED — no her in V1; the cafe (chorus) is the first true
sighting.

## The room (fixed geometry — defined by the KITCHEN MASTER)
- Small apartment kitchen, same flat as the bedroom, minutes later. Grey rainy
  morning: cool daylight from a rain-streaked window over the counter + soft
  warm under-cabinet tungsten (playbook "normal life" grammar).
- Upper cupboard with plain ceramic mugs; kettle on the counter, steaming.
- A small open shelf in the background: a little framed photo among books —
  always soft, never readable (bible: her face never literal). PLANT for the
  final chorus payoff.
- Wardrobe: the same plain dark slept-in tee (continuity from the bedroom).
  Bare hands, NO ring.
- Body-state law: his body exists ONLY in (a) the MUG take and (b) the WINDOW
  SYNC shot. Inserts contain no part of him.

## Cuts (V1 lines from analysis/line_map.json)
1. **23.5–31.3 — "soft touch upon my skin" — THE TWO MUGS (one take).**
   He opens the cupboard, takes down TWO mugs out of habit — stops — a beat;
   his thumb brushes the rim of the second mug (the lyric lands ON the touch)
   — he puts one back and closes the door on it. Whole beat in one 10s kling
   take, cut points measured from 2fps frames.
2. **31.3–35.2 — "my heart had crossed the ocean" — SYNC LINE.** Closeup at
   the kitchen window: he sings the line quietly, looking out at the rain.
   Same stack as the intro line: derived sync still → wan2_7 (imported still
   + imported vocal slice) → 2K aigc upscale finish.
3. **35.2–43.0 — "where the rivers bend" + tail.**
   a. 35.2–38.2: INSERT (derived from master): rain trails BENDING down the
      window glass — the lyric drawn, not said.
   b. 38.2–43.0: back into the take (or take 2, same setup): he pours coffee
      into ONE mug and stands with it; in the final half-beat his eyes drift
      to the shelf photo. NO push-in — a glance, then out.

## Audio
- Music bed: local ffmpeg slice song.mp3 23.5–43.0 → audio_relay/v1_bed.mp3.
- Sync vocal: slice 30.5–35.5 → audio_relay/v1_line3.mp3 (line starts at 0.81
  in-slice; in the cut the sync seg's in_point MUST equal timeline_pos−30.5).
- Rule: ONE continuous music track under all cuts.

## Assets to generate (in order, each frame-QC'd before the next spend)
1. KITCHEN MASTER (soul_2 + bible) — USER LIKENESS GATE before any animation.
2. MUG take (kling 10s from master, FIRST/THEN choreography above).
3. WINDOW SYNC still (derived from master: he turns to the window, face
   visible toward camera through/at the glass) → wan2_7 → 2K.
4. INSERT rain-rivers (derived window close-up → kling 5s locked-off).
5. POUR beat: covered by the tail of the MUG take if it reads; otherwise a
   second take from the same master (body-state law holds: same setup pose).
