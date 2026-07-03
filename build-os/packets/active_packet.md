# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-023 (first70 revision — mug grain, lip-sync timing, AI-look syncs, curb
> finale redesign) is CLOSED (2026-07-03). NO packet is active.** Receipt:
> `build-os/receipts/P-023.md`. Delivered `first70.mp4` v2 (70.0s, final
> frame-QC = **SHIP**) + `v1_v2.mp4` (19.5s) + `v2_v2.mp4` (27.3s) on
> `claude/when-it-rains-handoff-l0u075`. All four user notes on v1 resolved;
> curb zoom finale live. Read `when-it-rains/HANDOFF.md` for final asset IDs +
> ops learnings (incl. the NEW HARD RULE: no bare chest ever;
> salvage-don't-reroll wardrobe fixes; and the audio-gap verification method).
>
> (Memory catch-up recorded at this close: P-020 locked V1 "Great", P-021 [V2
> board] closed UNRECEIPTED, P-022 delivered first70 v1 — see the P-023 receipt
> Notes.)

## Next packet (staged for the orchestrator — open as P-024)

**P-024 — PRE1 (70.3–89.8s): the darkening walk.**

- **Lines:** "Don't know if you still feel it / I lose my breath / the trees
  are moving / like you never left."
- **Scene (ROADMAP.md, rung 3 — signs without her):** he walks faster; wind
  moves the trees like someone passing; he stops — breath fogging — turns
  around ON the line "like you never left": empty street. **Δ: the signs are
  now chasing HIM. He decides to go somewhere (the cafe) — giving CH1 a
  cause.**
- **Method:** board FIRST per the roadmap story rules (Δ + because-chain stated
  before any generation); playbook laws 0/0b binding; scene spec → master still
  (user gates likeness vs `review/ANCHOR_BOARD.png`) → derived takes → frame QC
  via review-fetch → measured cuts → CI render → user verdict.
- **Budget:** roadmap estimate ~150–200 credits; 1405.71 remaining at P-023
  close. New generation only inside this packet with go.
- **Id note:** the ROADMAP.md packet table lists PRE1 as "P-023", but P-023 was
  consumed by the first70 revision — PRE1 is **P-024**; later sections shift by
  one (V3/V4 → PRE2 → CH2 → BRIDGE → FINAL → full assembly).

## Out of scope (explicit, until a fresh go)

- Any merge / deploy / publish / secrets. (CI relay pushes render commits on
  the triggering branch — established mechanism; everything else is gated.)
- The **history rewrite** to purge the Soul TRAINING photos from PUBLIC git
  history — offered to the user, still unanswered; needs an explicit go. (The
  bare-chest purge was a separate, user-ORDERED rewrite, already done.)
- Replacing locked material: hero clip `491e39d1`, chorus_v16, intro_v6
  (incl. the intro's ~19–21s chain+ring — flag before FINAL assembly, do not
  fix without reopening the lock).
- New Higgsfield generation outside a staged scene packet (credits).
- Anything showing bare chest — NEW HARD RULE: delete immediately, never ship,
  never reroll wardrobe fixes (salvage via nano edit instead).

## Branch base

- `claude/when-it-rains-handoff-l0u075` (supersedes the fetr0z-era branches,
  same history; no trunk — judged against the branch tip). HEAD at this close:
  **`9992e95`** (P-023 QC purge + HANDOFF refresh), plus the archivist's own
  `build-os/` close commit on top. `render-chorus.yml` is branch-agnostic
  (follows `${{ github.ref_name }}`).

---
_P-023 closed 2026-07-03 (first70 v2 SHIP — enhanced mugs, onset-tight syncs,
realism stills, curb zoom finale; receipt `build-os/receipts/P-023.md`). NO
packet active. Next: P-024 — PRE1 (70.3–89.8, the darkening walk)._
