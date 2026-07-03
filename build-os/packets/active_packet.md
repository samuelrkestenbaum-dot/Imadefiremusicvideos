# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — P-024 CLOSED 2026-07-03 (receipt
  `build-os/receipts/P-024.md`; final frame-QC SHIP, PRE1 likeness 9/10;
  `pre1_v1.mp4` 19.51s + `first90.mp4` 89.79s frame-exact on the July Reverb
  bed). No packet is in flight; the next packet below is STAGED and needs an
  explicit user GO to open.

## Staged next: PAPER PACKET P-025 — re-time ROADMAP to the verified clock + apparition legibility standard + waterfront-photo plant

- **Type:** PAPER packet — docs only, **zero generation, zero credits**.
- **Source:** `when-it-rains/DIRECTORS_NOTES.md` — must-fix **#2** (the
  back-half clock is WRONG, VERIFIED against the beat-locked line map — see
  the addendum table: CH1 is really 89.8–132.7 [42.9s; locked chorus_v16
  covers only the first 12s], V3/V4 132.7–183.4, PRE2 183.4–214.6, CH2
  214.6–238.1, BRIDGE 238.1–257.6, FINAL 257.6–273.8 [16.2s, was planned 5×
  too long]), must-fix **#1** (the ghosts don't read — write the APPARITION
  LEGIBILITY STANDARD: edge contrast, ONE identifying cue, minimum 1.5s hold,
  he-sees/we-sees chart per ladder rung), and the **STRUCTURAL** section (put
  the WATERFRONT PHOTO in the V3/V4 drawer so the BRIDGE-at-the-water has a
  cause and PRE2 interrupts a pilgrimage).
- **Deliverables:** ROADMAP.md Part 3/4 re-timed to the verified clock (incl.
  a CH1 plan for 102–132.7 and a 16s FINAL); the apparition standard written
  (new doc or ROADMAP/PLAYBOOK section); the waterfront-photo plant added to
  the V3/V4 board spec. Mark STORY/TREATMENT superseded where changed.
- **Id note:** the MEDIA packet formerly numbered "P-025" in the old roadmap
  numbering **shifts after this paper packet** (as PRE1's id shifted at
  P-023/P-024). Do not generate against the old clock before this closes.
- **Read first:** `when-it-rains/HANDOFF.md` (P-024 addendum),
  `DIRECTORS_NOTES.md` in full, then ROADMAP.md.

## Hard rules in force (standing)

- **NO bare chest, ever**; salvage wardrobe via nano/local edit, never reroll.
- Likeness law: user gates picks vs `review/ANCHOR_BOARD.png`; max 2 nano
  passes on face frames.
- Laws 0 (DERIVE) + 0b (SANDBOX EYES) + frame-exact stitch law + wan
  behavioral pinning + explicit kling `sound:"off"` (P-024 addendum).
- Song is the **July Reverb mix** — cross-correlate anchors before slicing
  any new mix; `song.mp3` stays gitignored.
- No merge / deploy / publish / secrets / new generation without explicit go.

## Branch base

- `claude/when-it-rains-handoff-l0u075`, HEAD at P-024 close = `057f739` +
  the archivist close commit; in sync with origin at close. No trunk — green
  is judged against the branch tip. `render-chorus.yml` is branch-agnostic.

---
_P-024 closed 2026-07-03 by the archivist (receipt `build-os/receipts/P-024.md`).
P-025 staged, awaiting explicit user GO._
