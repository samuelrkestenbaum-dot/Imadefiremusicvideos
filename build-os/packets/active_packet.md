# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-018/P-019 (intro pair — bed regen v5 + opening match v6) are CLOSED. THE
> INTRO IS LOCKED. NO packet is active.** Combined receipt:
> `build-os/receipts/P-018_P-019.md`. (Numbering note: "P-018" also names the
> earlier chorus-lock receipt `P-018.md` — an id collision, recorded; **the
> next packet is P-020**.)
>
> **The pair in one paragraph:** 21 commits `f724323..25b8b80` (base
> `f724323` = the intro_v4 CI render; 12 authored + 9 CI). P-018 fixed the
> intro_v4 bed setup per user feedback (insert was a DIFFERENT bedroom; bed
> became a **DOUBLE bed** for the "her untouched side" beat). Root cause fixed
> as PROCESS: assets had been prompted fresh instead of DERIVED from the scene
> master, and used blind (sandbox can't see the CDN) → built the **CI
> review-fetch path** (`scripts/fetch_review.sh` + `render-chorus.yml`;
> `review_urls.txt` assets land in `when-it-rains/review/`, videos as 2fps
> frame PNGs — sandbox eyes on EVERYTHING before spend/ship). New assets all
> derived from the approved soul_2 bed master `2d080b77`: bed take kling 10s
> `eea03072` (beats measured from frames), her-half insert nano `9924df64` →
> `f64ef24d` → kling 5s `8bd72a9d` (first attempt caught in frame QC — whole
> bed empty — re-derived). `render_intro_v5.sh` → `intro_v5.mp4`: "Looks great
> except [opening shot mismatch]". P-019 matched the opening rain shot to the
> bedroom's own window by derivation (nano `c63df6d2` → kling 8s `371791eb`,
> frame-QC'd: locked camera, same building/road). `render_intro_v6.sh` →
> `intro_v6.mp4` — **USER LOCKED: "Amazing"**. Docs (`25b8b80`):
> `INTRO_SCENE_SPEC.md` LOCKED (final asset IDs, double-bed canon);
> `PRODUCTION_PLAYBOOK.md` **law 0 "DERIVE, DON'T DESCRIBE"** + **law 0b
> "SANDBOX EYES"**, section 6 = intro_v6 is the second reference cut.

## Next packet (staged for the orchestrator — open as P-020)

**P-020 — Verse 1 board (23.5–43.0s): morning-routine kitchen, the TWO MUGS
beat.**

- **Lines / timings:** "soft touch upon my skin" 23.5–31.3 · "my heart had
  crossed the ocean" 31.3–35.2 · "where the rivers bend" 35.2–43.0.
- **Scene:** morning-routine kitchen with the **TWO MUGS handled-action beat**
  (the grief-in-ordinary-life grammar: his routine, her absence).
- **Method (laws 0 + 0b BINDING):** scene spec (INTRO_SCENE_SPEC.md is the
  template now) → kitchen scene MASTER still (soul_2 + character bible; user
  eyeballs likeness BEFORE animation) → every take/insert DERIVED from the
  master → queue everything through `review_urls.txt` → frame QC in
  `when-it-rains/review/` BEFORE cutting → measured cuts from frames →
  `render_v1_*.sh` → CI render → user verdict.
- **Budget:** credits ~1700–1800 of 2415 remain (rough) — new generation only
  inside this packet with go.
- **After V1:** PRE1 → CH1 → V3/V4 → PRE2 → CH2 → BRIDGE → FINAL, then the
  **full 4:34 assembly** (one continuous vocal, cuts on `analysis/beats.json`).

## Out of scope (explicit, until a fresh go)

- Any merge / deploy / publish / secrets. (The branch **auto-mirrors to
  origin** — an environment fact; commits are fine, everything else is gated.)
- The **history rewrite** to purge the Soul training photos from PUBLIC git
  history — **offered to the user, unanswered**; needs an explicit go.
- Replacing locked material: hero clip `491e39d1`, chorus_v16, intro_v6 —
  user-locked.
- New Higgsfield generation outside a staged scene packet (credits).

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch
  tip). HEAD at this close: **`25b8b80`** (intro_v6 lock: spec + playbook laws),
  plus the archivist's own `build-os/` close commit on top. The branch
  auto-mirrors to origin.

---
_P-018/P-019 closed 2026-07-02 (INTRO LOCKED — intro_v6 "Amazing"; double-bed
canon; review-fetch "sandbox eyes" + laws 0/0b canonized; combined receipt
`build-os/receipts/P-018_P-019.md`). NO packet active. Next: P-020 — Verse 1
board (23.5–43.0s, kitchen / TWO MUGS)._
