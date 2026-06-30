# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-009 CLOSED → repo coherent + render-ready. Only open item = the user's
> render-review. Optional / low-priority: P-010 (stills backfill — pre-existing
> id-format gap, non-functional).**
>
> **P-009 (Reconcile `assets.json` clip entries to `clips.csv`) is CLOSED** —
> marketing-media manifest / docs-consistency (no generation, no CSV functional
> change), route builder → reviewer → qa → archivist. Commit `f59829b`
> (base `cb7610b`): updated the **11 stale clip entries**
> (C01, C04, C06, C07, C13, C15, C16, C19, C22, C23, C24) in `data/assets.json`
> (job_id / source_still / mp4_url) to match the fixed `data/clips.csv`. One file,
> 33 ins / 33 del. **qa GREEN 8/8 + Commit-1 isolation** (assets.json clips ==
> clips.csv 36/36, 0 divergence; exactly the 11 changed, other 25 byte-identical;
> old job_ids/source_stills all gone; stills 52 / counts 36/52/86 / inline edl 86
> / models / references byte-unchanged; safety clean). **reviewer PASS**
> (verbatim-from-source; scope airtight; manifest now points at the CORRECT fixed
> clips; the source_still↔stills.csv non-resolution is a PRE-EXISTING id-format
> quirk affecting all 36 clips before AND after, NOT a P-009 defect; Codex
> second-eyes UNAVAILABLE — single-reviewer). Receipt `build-os/receipts/P-009.md`.
> (P-008 — docs/manifest refresh + C27/C33 on-model verified — CLOSED, receipt
> `build-os/receipts/P-008.md`; P-007 — band coverage inserted + PRE2/CH1 re-timed
> — CLOSED; P-006 — clips generated — CLOSED; P-005 — plan — CLOSED; P-004 —
> section-sync — CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 —
> RENDER_REVIEW.md — CLOSED; P-001 — Install Build OS — CLOSED.)

## Open work (no packet — for the orchestrator to stage next)

1. **User renders + judges the cut** (off-machine, user's Mac) — **the only
   remaining real work.** `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`,
   walking `when-it-rains/RENDER_REVIEW.md` — the human-eye confirmation of the 11
   regenerated clips, the P-004 section-sync timing, the P-006/P-007 band coverage,
   and overall pacing. **C27 / C33 on-model is RESOLVED** (verified on-model in
   P-008) — no longer a render spot-check item.
2. **P-010 (optional / low-priority, needs user go)** — stills backfill: `clips.csv`'s
   `source_still` values are **8-char prefixes** that don't resolve to `stills.csv`'s
   **full-UUID** keys (a pre-existing id-format quirk affecting all clips;
   **non-functional** — the render reads `mp4_url` from `clips.csv` directly). Also
   **C04's** `source_still` is a `regenA1` **placeholder** (known-incomplete from the
   earlier C04 partial regen). Touches a source CSV + a count → needs explicit go.
3. **Sub-beat beat-grid quantization (optional, deferred)** — snap the cuts to the
   **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session).
4. **Selective 2K/4K upscale** — explicitly LAST, only after the cut is locked.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only). The C27/C33 regen is **moot** (verified
  on-model). P-010 (if taken) also needs a go (touches a source CSV + a count).
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-009 close: `f59829b` (base `cb7610b`). Local commits only — not pushed.

---
_P-009 closed 2026-06-29 (assets.json reconciled to clips.csv — qa GREEN,
reviewer PASS). No packet active — the repo is coherent + render-ready; the user's
render-review is the only open item. Optional later: P-010 (stills backfill)._
