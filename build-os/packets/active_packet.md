# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** in flight (next)
- **Packet id:** P-007
- **Title:** Insert C25–C34 into `data/edl.csv` (+ `clips.csv` / `stills.csv`) +
  re-time PRE2 / CH1 to ~3.3s avg

> **P-006 CLOSED (10 clips generated) → P-007 insert+re-time `edl.csv` in
> flight. Assets in `build-os/receipts/P-006.md` + `scratchpad/p006_assets.json`.**
>
> **P-006 (Generate 10 band-coverage clips C25–C34 on Higgsfield) is CLOSED** —
> marketing-media generation executed from the main loop via the Higgsfield MCP
> under the user's **explicit "all at once" go**. 10 reference-anchored stills
> (`nano_banana_flash`, anchor `5cc8239a`; C27/C33 also +3 selfies) + 10 Kling
> clips (`kling3_0`/std/off/5s); PRE2 clips carry `declined_preset 24bae836-…`,
> CH1 clips warm. **~90 credits; balance ≈ 2,415.5.** On-model verification
> DEFERRED to the user's render-review (auto `video_analysis` errored on job-ids;
> reference-anchoring confirmed; C27/C33 are the spot-check). Receipt:
> `build-os/receipts/P-006.md` (full asset map, closed 2026-06-29). (P-005 — plan
> — CLOSED, receipt `build-os/receipts/P-005.md`; P-004 — EDL section-sync —
> CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED;
> P-001 — Install Build OS — CLOSED.)

## P-007 — insert + re-time (GATED edit, in flight)

- **What:** splice the 10 generated clips (C25–C30 into PRE2, C31–C34 into CH1)
  into `data/edl.csv` and re-time PRE2 / CH1 to ~3.3s avg per cut; add their
  rows to `clips.csv` / `stills.csv` (ids + mp4 URLs from
  `build-os/receipts/P-006.md`). The asset map lists `slot_after_row` +
  `target_dur` per clip (PRE2 @ 3.4s, CH1 @ 3.2s).
- **Authority:** edit authority on `when-it-rains/**` product files — **needs the
  user's explicit go** before the builder touches `data/`.
- **Carry the two P-005 non-blocking notes:** (a) keep **C26** (full-band push-in)
  visually distinct from existing **C09** (also a push-in); (b) the plan's relative
  `data/edl.csv` path is correct **from `when-it-rains/`** — from repo root use
  `when-it-rains/data/edl.csv`.

## Also-open (not the active packet)

1. **User renders + judges the section-synced cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md` — still-open human-eye confirmation of the 11
   regenerated clips, the P-004 section-sync timing, AND the new P-006 band clips
   (esp. C27 / C33 on-model, see residue).
2. **Sub-beat beat-grid quantization (optional, deferred)** — snap the cuts to the
   **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session). Section-sync (P-004) was the coarser confirmed-times pass.

## Out of scope (explicit)

- Any **further** Higgsfield generation / upscale beyond the C25–C34 already
  generated (credits = external mutation → media packet + explicit go only).
  Upscale is explicitly LAST, after the cut is locked.
- Doing the P-007 edit without the user's explicit go.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  Base for P-007: `0193678` (P-005 close) + the P-006 close commit.

## Plan (≤2 commits) — P-007

1. **Commit 1 (green in isolation):** insert C25–C34 rows + re-time PRE2 / CH1 in
   `data/edl.csv` (+ `clips.csv` / `stills.csv`); EDL still totals to the confirmed
   span, reversible via the backups.
2. **Commit 2 (optional, same packet):** _to be defined when the packet is cut._

---
_P-006 closed 2026-06-29 (clips generated). P-007 staged here as next/in-flight —
confirm the user's go before the builder edits `data/`._
