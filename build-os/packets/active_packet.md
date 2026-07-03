# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE (opened 2026-07-03 on explicit user GO)
- **Packet id:** P-024
- **Title:** PRE1 (70.3–89.8s) — the darkening walk

## Scope

- **Lines:** "Don't know if you still feel it / I lose my breath / the trees
  are moving / like you never left."
- **Scene (ROADMAP.md Part 3, rung 3 — signs without her):** he walks faster;
  wind moves the trees like someone passing; he stops — breath fogging — turns
  around ON the line "like you never left": empty street. **Δ: the signs are
  now chasing HIM. He decides to go somewhere (the cafe) — giving CH1 a
  cause.** Because-chain: BECAUSE the V2 puddle double-reflection almost
  caught him, the dread rises here; BECAUSE he decides to go somewhere, CH1
  (the cafe, LOCKED chorus_v16) has a cause.
- **Id note:** ROADMAP.md Part 4 table lists PRE1 as "P-023" — that id was
  consumed by the first70 revision. PRE1 is **P-024**; all later table rows
  shift by one (V3/V4 → PRE2 → CH2 → BRIDGE → FINAL → full assembly).

## Method (ROADMAP Part 4 flow, playbook-bound)

board → user reacts → master(s) w/ candidate batches (3–4 per pick) → user
likeness-gates vs `review/ANCHOR_BOARD.png` → derived takes → sync stack →
measured cut → frame QC via review-fetch (sandbox eyes, law 0b) → CI render →
user verdict → receipt. Laws 0 (DERIVE, DON'T DESCRIBE) + 0b binding; Δ +
because-chain stated on the board BEFORE any generation.

## Budget

- Roadmap estimate **~150–200 credits**; **1405.71** available at open.
- New generation only inside this packet, with the user's GO (given 2026-07-03).

## Known blocker (surface before the sync/cut stage)

- **NO audio slices exist for 70.3–89.8** — `audio_relay/` has intro/v1/v2/
  chorus slices only, and `song.mp3` (Jun-27 mix) is NOT in this container.
  **The user must re-attach the mix before slicing PRE1 vocals** for the wan
  sync stack. Board/master/takes stages can proceed without it.

## Hard rules in force

- **NO bare chest, ever** (user hard rule 2026-07-03) — delete on sight,
  never ship; do NOT reroll wardrobe fixes — salvage best frame via nano edit.
- Likeness law: candidate batches gated by the USER vs
  `review/ANCHOR_BOARD.png`; max 2 nano passes on face frames.
- wan2_7: both inputs imported media, exact roles
  `start_image`/`audio_references`; verify "mouth stops" flags against the
  slice's mid-band FFT energy envelope before rerolling (breath gaps are
  correct sync).
- Frame-QC raw before any 2K upscale; purge same-named `review/` copies
  before re-queuing; keep `review/` under ~30MB.

## Out of scope (explicit, until a fresh go)

- Any merge / deploy / publish / secrets. (CI relay pushes render commits on
  the triggering branch — established mechanism; everything else is gated.)
- The history rewrite to purge Soul TRAINING photos from PUBLIC git history
  (offered, unanswered).
- Replacing locked material: hero clip `491e39d1`, chorus_v16, intro_v6
  (incl. the intro ~19–21s chain+ring — flag before FINAL assembly only).
- Generation outside this packet's PRE1 scope.

## Branch base

- `claude/when-it-rains-handoff-l0u075`, HEAD at open **`2f791a8`** (P-023
  close commit), in sync with origin (0 ahead / 0 behind). No trunk — green
  is judged against the branch tip. `render-chorus.yml` is branch-agnostic.

---
_P-024 opened 2026-07-03 by the orchestrator on explicit user GO. Prior
packet P-023 closed 2026-07-03 (receipt `build-os/receipts/P-023.md`)._
