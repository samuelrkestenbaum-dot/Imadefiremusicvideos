# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** **NONE ACTIVE.** P-026 (first90 QUALITY PASS — resolution + face
  consistency) **CLOSED 2026-07-03** — 1080p `first90.mp4` (89.79s) +
  `pre1_v1.mp4` re-delivered, frame reads SHIP, receipt
  `build-os/receipts/P-026.md`. Next packet staged below — open it via the
  orchestrator before any work.

## Staged next — P-027 — PAPER PACKET (docs only, zero generation)

**ROADMAP re-time to the verified section clock + APPARITION LEGIBILITY
STANDARD + waterfront-photo plant** (per `when-it-rains/DIRECTORS_NOTES.md`
must-fix #1/#2 + the STRUCTURAL section; the verified clock table is its
addendum).

- **Why it must come first:** the ROADMAP back-half section clock is
  **VERIFIED WRONG** (CH1 is really 89.8–132.7 = 42.9s — the locked
  chorus_v16 covers only the first ~12s; FINAL is only 257.6–273.8 = 16.2s;
  V3/V4/PRE2/CH2 all shifted). **Do NOT generate against the old clock.**
- **Scope:** (1) re-time ROADMAP.md to the verified clock — absorbing the
  CH1-extension question (a plan for 102–132.7, 30.7s of chorus beyond the
  locked cut) and FINAL's mug-choice ending landing in **16s, not 86**;
  (2) write the APPARITION LEGIBILITY STANDARD; (3) add the waterfront-photo
  plant to V3/V4. **Zero Higgsfield generation, zero credits.**
- **Id note:** renumbered **P-026 → P-027** when the QUALITY PASS
  (user-directed) took the P-026 id. (Itself renumbered from the original
  "P-025" staging at the P-025 close.)
- **Read first:** `when-it-rains/HANDOFF.md` (QUALITY PASS addendum FIRST, then
  P-025 / P-024), `DIRECTORS_NOTES.md`, `ROADMAP.md`, `PRODUCTION_PLAYBOOK.md`.

## Hard rules in force (standing)

- **NO bare chest, ever**; salvage wardrobe via nano/local edit, never reroll.
- Likeness law: user gates picks vs `review/ANCHOR_BOARD.png`; max 2 nano
  passes on face frames. Element-refit (P-025) is the fix for AI-look faces;
  refit QC must check brown eyes explicitly (drift) + chain bias; **lock the
  pose explicitly — refit reimagines composition ~half the time** (P-026).
- **Render at 1080p, never downscale high-res takes to 720p** (P-026);
  **Topaz prob-4, not bytedance, for real detail on sub-1080p takes** (P-026).
- Laws 0 (DERIVE) + 0b (SANDBOX EYES) + frame-exact stitch law + wan
  behavioral pinning + explicit kling `sound:"off"` + rotation salvage.
- Song is the **July Reverb mix** — cross-correlate anchors before slicing
  any new mix; `song.mp3` stays gitignored.
- Delivery law: **>50MB chat sends fail silently — send phone encode (37MB
  crf24 1080p delivers fine), check file_uuid** (P-026).
- No merge / deploy / publish / secrets without explicit go. CI-relay pushes
  on the working branch are the accepted delivery mechanism (P-020..P-026
  precedent; branch auto-mirrors).

## Branch base

- `claude/when-it-rains-handoff-l0u075`, tip at P-026 close = **`fb26aad`**
  (+ the archivist close commit on top); clean, 0 ahead / 0 behind origin.
  No trunk — green is judged against the branch tip. `render-chorus.yml` is
  branch-agnostic.

---
_P-026 closed + cleared 2026-07-03 by the archivist (receipt
`build-os/receipts/P-026.md`); P-027 staged (paper packet, renumbered from the
old P-026 staging)._
