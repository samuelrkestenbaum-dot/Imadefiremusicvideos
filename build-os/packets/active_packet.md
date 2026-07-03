# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** **ACTIVE — P-025 — PRE1 REALISM REPAIR** (user-directed,
  opened 2026-07-03). Takes precedence over the staged paper packet, which
  is **RENUMBERED → P-026** (see Id note below).

## P-025 — PRE1 REALISM REPAIR (media packet, marketing-media authority)

- **Trigger (user feedback on the delivered `first90.mp4`, P-024):** the PRE1
  renderings of him "look extremely like AI, not realistic like early in the
  song." Same scenes/images wanted — the face repaired to the canonical
  likeness. **Delivered-cut repair rule: the CUT SHAPE STAYS** (same
  choreography, same timings, same scenes — only the face/realism changes).
- **Two face zones to repair:**
  1. **Walk-stop-breath take (70.3–78.1)** — master: walk W2 `4aaefb8b` +
     chain scrub → `361af0a5`; take: kling `584f5e2b` (10s).
  2. **Turn sync close-up (82–89.8)** — master: T3 `d1688201` → local
     rotate90CW + chest-up crop (`turn_master_crop.png`, imported
     `b59d18d8`); take: wan retry `97a9771e` → 2K `c6888a50`.
- **Plan (in order):**
  1. **Nano element-refit** of the two masters using element **wir-him**
     `1b581c11-e515-4d88-bb2c-b2b0af3b722d` embedded per
     `PRODUCTION_PLAYBOOK.md` elements section (`<<<uuid>>>` placeholder).
     Candidate batches; frame-QC via sandbox eyes; **user gates picks vs
     `review/ANCHOR_BOARD.png`** (likeness law: max 2 nano passes on face
     frames).
  2. **Re-animate:** walk = kling, SAME choreography as `584f5e2b`
     (`sound:"off"` explicit); turn = wan with the **pinned behavioral
     prompt** (sings DIRECTLY INTO CAMERA / never turns away / exit window /
     no hand near lens) + audio slice **`3b540307`** (wan roles
     `start_image`/`audio_references`, both imported media).
  3. **Frame-QC** every take before spend/ship (law 0b SANDBOX EYES);
     then **2K** upscale of accepted takes.
  4. **Swap URLs in `render_pre1.sh`**, re-render **pre1 + first90** via the
     CI relay (`render_request.txt` line-1 + nonce; frame-exact stitch law —
     tpad+trim to exact frame counts, `render_p024.sh` pattern 576/456/655/468).
  5. **Deliver the phone encode** (crf 23; chat sends >~50MB fail silently —
     verify file_uuid; full-quality master stays in the repo).
  6. **Receipt** via archivist (`build-os/receipts/P-025.md`) + memory update.
- **Budget:** est **~40–60 credits** of **1371.75** available.
- **Read first:** `when-it-rains/HANDOFF.md` (P-024 addendum),
  `PRODUCTION_PLAYBOOK.md` (elements + laws), `review/ANCHOR_BOARD.png`.

## Id note (renumber recorded)

- The **PAPER packet** formerly staged as P-025 (re-time ROADMAP to the
  verified clock + APPARITION LEGIBILITY STANDARD + waterfront-photo plant,
  from `DIRECTORS_NOTES.md`) **shifts to P-026** — unchanged in content,
  still REQUIRED before any back-half generation (the ROADMAP back-half
  clock is verified wrong; PRE1 is unaffected, so P-025 may proceed).

## Hard rules in force (standing)

- **NO bare chest, ever**; salvage wardrobe via nano/local edit, never reroll.
- Likeness law: user gates picks vs `review/ANCHOR_BOARD.png`; max 2 nano
  passes on face frames.
- Laws 0 (DERIVE) + 0b (SANDBOX EYES) + frame-exact stitch law + wan
  behavioral pinning + explicit kling `sound:"off"` + rotation salvage
  (soul_2 chest-up/facing-camera renders rotated 90° — rotate+crop locally,
  never reroll) (P-024 addendum).
- Song is the **July Reverb mix** — cross-correlate anchors before slicing
  any new mix; `song.mp3` stays gitignored.
- Delivery law: >~50MB chat sends fail silently — send phone encode, check
  file_uuid.
- No merge / deploy / publish / secrets without explicit go. CI-relay pushes
  on the working branch are the accepted delivery mechanism (P-020..P-024
  precedent; branch auto-mirrors). ≤2-commit contract acknowledged
  inapplicable to the CI-relay media workflow (same precedent).

## Branch base

- `claude/when-it-rains-handoff-l0u075`, tip at open = `414b235` (P-024
  close `45d4fcb` + HANDOFF delivery-size law `414b235`); clean, in sync
  with origin. No trunk — green is judged against the branch tip.
  `render-chorus.yml` is branch-agnostic.

---
_P-025 opened 2026-07-03 by the orchestrator (user-directed realism repair;
paper packet renumbered → P-026). P-024 closed 2026-07-03 (receipt
`build-os/receipts/P-024.md`)._
