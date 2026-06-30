# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-007 CLOSED → the edit (86 cuts, 274.0s) is ready for the user's
> render-review.** Backups: `data/edl_pre_bandcoverage_backup.csv`
> (pre-band-coverage, byte-exact 76-cut section-synced state),
> `data/edl_original_backup.csv` (pre-section-sync, byte-exact original 276s) —
> neither overwritten.
>
> **P-007 (Insert band-coverage C25–C34 + re-balance PRE2/CH1) is CLOSED** —
> marketing-media media-pipeline edit, route builder → reviewer → qa → archivist.
> Commit `1969435` (base `ed046b5`): `scripts/insert_band_coverage.py`
> regenerated `data/edl.csv` → 86 cuts (PRE2 6→12 / 41.00s, CH1 8→12 / 38.75s,
> ~3.3s avg, total 274.0s, all section starts unchanged), +10 rows each into
> `clips.csv` / `stills.csv`. **qa GREEN 13/13; reviewer PASS** (Codex
> second-eyes unavailable, single-reviewer). Fully reversible. Receipt
> `build-os/receipts/P-007.md`. (P-006 — clips generated — CLOSED, receipt
> `build-os/receipts/P-006.md`; P-005 — plan — CLOSED; P-004 — section-sync —
> CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED;
> P-001 — Install Build OS — CLOSED.)

## Also-open (no packet active — for the orchestrator to stage next)

1. **User renders + judges the cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md` — the human-eye confirmation of the 11
   regenerated clips, the P-004 section-sync timing, the new P-006/P-007 band
   coverage (esp. **C27 / C33 on-model**, see residue), and overall pacing.
2. **Sub-beat beat-grid quantization (optional, deferred)** — snap the cuts to the
   **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session).
3. **Selective 2K/4K upscale** — explicitly LAST, only after the cut is locked.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only), including the ~10-credit C27/C33 regen if
  off-model.
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-007 close: `1969435`.

---
_P-007 closed 2026-06-29 (band-coverage inserted + PRE2/CH1 re-timed). No packet
in flight — the cut is staged for the user's render-review; the orchestrator
picks the next thread on the user's go._
