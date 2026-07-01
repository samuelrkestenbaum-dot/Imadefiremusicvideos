# CAFE SCENE — locked physical staging (V2 "beyond my shoulder" beat)

**Why this doc:** every prior miss (wrong table, wrong eyeline, third-person
reflection, two-reflection composite, hands on counter vs at sides) came from
generating shots without ONE locked physical layout. This spec is the law for
every shot in the scene. Nothing gets generated that contradicts it.

## The room (fixed geometry)
- He stands AT the counter, first in line, waiting to order.
- The glass pastry case sits ON the counter to his RIGHT, at waist height,
  its glass front angled ~45 degrees to his eyeline.
- BEHIND him: the cafe floor — a few tables, the door, the big rain-streaked
  window. This is the space the case glass reflects.
- HER (virtual position): standing back by the tables/door BEHIND him — which
  is exactly what an angled glass front would reflect to his eye.

## The reflection physics (why the insert works now)
Standing at an angle to the glass, he does NOT see his own reflection — he sees
the room BEHIND him mirrored in the glass. So the insert contains **HER
reflection ONLY** — no reflection of him, no part of his body in frame. One
reflection, physically correct, simple to read.

## Body-state law (kills the hands mismatch)
His body appears ONLY in the one-take. The insert contains NO part of him.
Therefore his posture/hands cannot mismatch between shots — the take is
internally consistent by definition, and it is the only source of his body.

## The sequence (3 shots, 2 sources)
1. **MEDIUM — the one-take, first beat (in 1.0s, ~2.0s):**
   He waits in line; his gaze drifts down-right to the case glass; he stills.
   (Existing take c1ffc156 — gaze verified down at the case, 0:00-0:07.)
2. **INSERT — his angle on the glass (ONE new shot):**
   The case glass from his position, angled ~45 degrees, waist height,
   pastries dimly visible through the glass; IN the glass, ONE translucent
   reflection: HER, standing back by the tables/door, looking toward him.
   No text. No him. Same case/counter/warm light as the master (9b3953d6).
3. **MEDIUM — the same take, second beat (re-enter at ~6.9s, ~2.2s):**
   He turns around toward where she would be standing — strangers, no one;
   his face falls. (Same take = same counter/background, by construction.)

Cut logic: look (1) -> what he sees (2) -> reaction (3). Eyeline down-right in
(1) matches the angle of (2); her reflected position in (2) is behind him,
which is where he turns in (3). Every look motivates the next cut.

## Prompt law for the insert (verbatim constraints)
- angled view of the glass case front, from the standing eyeline of the man
  at the counter, waist-height case, looking down and to the right
- ONE reflection in the glass: the woman (element wir-her), translucent,
  ghost-like, standing a few feet back in the cafe behind the viewer
- NO reflection of the viewer, NO person in frame, NO hands
- same case, counter, warm tungsten light, rainy window in the reflected
  background (matching master 9b3953d6)
- absolutely NO text/signage/letters; film grain, 2.35:1
