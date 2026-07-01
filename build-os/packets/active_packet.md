# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-018 (CHORUS LOCK — the chorus-production era) is CLOSED. NO packet is
> active.** The live deliverable is the **LOCKED chorus**
> (`when-it-rains/scripts/render_chorus_v16.sh` → `when-it-rains/chorus_v16.mp4`)
> + **`when-it-rains/PRODUCTION_PLAYBOOK.md`** — the copy-paste bible for every
> remaining section. Receipt: `build-os/receipts/P-018.md`.
>
> **P-018 in one paragraph:** 32 commits `8a5048c..bc9d4d7` (base `90ce268`,
> + CI render commit `8a2e88d` = `chorus_v16.mp4`). Trained Soul of the artist
> `07822e21-af62-44cc-a8b8-0b27dfe6de8a` (8 real photos; removed from the tree
> after training — still in git history, see residue). Reference elements
> `wir-him` `1b581c11-…` (from de-ringed cafe still `32058bcb`) + `wir-her`
> `38ebfd81-…` (from her anchor `65382e29`) — multi-likeness single-frame
> generation PROVEN via `<<<uuid>>>` placeholders (nano_banana_2 / kling3_0).
> The locked chorus shape: hero hook (ORIGINAL wan2_7 lip-sync `491e39d1`) →
> her puddle reflection (`b22edfc6`) → hero → cafe one-take notice (`c1ffc156`
> @1.0s) → composited POV reflection reveal (insert `6b3be8f1` @55% over empty
> plate `ec557078`, setpts-fixed) → same-take turn (@6.9s). Method CANONIZED in
> `PRODUCTION_PLAYBOOK.md` (spec-first staging, body-state law, measured cuts,
> POV insert grammar, environment-mirrored reflections, surgical nano edits,
> true ffmpeg composites, wan2_7 lip-sync via IMPORTED media — P-017's mechanism
> question CLOSED: PROVEN — vocal relay via git → raw.githubusercontent →
> media_import_url, CI delivery via `.github/workflows/render-chorus.yml`).
> Character bible hard rules: HIM buzz cut FULL hairline reddish stubble fit
> lean BARE HANDS no ring; HER = his ex, oblique/reflections only; NO text in
> any frame. Proof = user eyeball verdicts on CI-rendered mp4s (v12..v16);
> ≤2-commit contract + formal qa/reviewer superseded by user direction
> (accepted, recorded deviation). User verdicts on record: original hero clip
> is THE hero (never replace); v14-style environment-mirrored reflection
> preferred; composited v15/v16 ghost is the standard; likeness ALWAYS beats
> scene-cohesion.

## Open work (no packet — for the orchestrator to stage next)

1. **Board the remaining `STORY.md` scenes with the playbook** (one scene =
   one packet, chorus shape as the reference): **apartment intro → V1 morning →
   street/bus PRE1 → V3 hall glimpse → V4 mirror/drawer → PRE2 train/sky →
   bridge waterfront flood → final.** Per scene: scene spec (CAFE_SCENE_SPEC.md
   template) → master still (soul_2 + bible, user eyeballs likeness BEFORE
   animation) → ONE continuous take per setup → measured cuts via
   `video_analysis` → inserts/composites per the playbook → CI render → user
   verdict. Credits: ~1900–2000 of 2415 remain (rough) — budget accordingly.
2. **The full 4:34 assembly** (after the scenes land): one continuous vocal,
   cuts on `analysis/beats.json`, hero holds on the hooks — supersedes the old
   107-cut `data/edl.csv` section by section.
3. **Later hygiene (optional packet):** prune the chorus v2–v15 iteration
   scripts and the older CI mp4s (v12–v15); refresh any review docs still keyed
   to the pre-playbook 107-cut edit.

## Out of scope (explicit, until a fresh go)

- Any merge / deploy / publish / secrets. (The branch **auto-mirrors to
  origin** — an environment fact; commits are fine, everything else is gated.)
- A **history rewrite** to purge the Soul training photos from git history
  (needed only if the repo goes public — user decision).
- Replacing the ORIGINAL hero clip `491e39d1` — user-locked, never replace.
- New Higgsfield generation outside a staged scene packet (credits).

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch
  tip). HEAD at P-018 close: **`8a2e88d`** (CI `chorus_v16.mp4` render, on top
  of the lock commit `bc9d4d7`), plus the archivist's own `build-os/` close
  commit on top. The branch auto-mirrors to origin.

---
_P-018 closed 2026-07-01 (CHORUS LOCK — trained Soul + elements + the locked
`render_chorus_v16.sh` + `PRODUCTION_PLAYBOOK.md` canonized; wan2_7 lip-sync
PROVEN via imported media; CI render delivery live; proof = user verdicts on
CI-rendered mp4s, accepted process deviation). NO packet active. Next: board
the remaining STORY.md scenes with the playbook, then the full 4:34 assembly._
