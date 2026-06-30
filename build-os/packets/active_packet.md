# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** in flight
- **Packet id:** P-009
- **Title:** Reconcile `assets.json` existing clip/still entries to
  `clips.csv` / `stills.csv`

> **P-008 CLOSED → P-009 in flight (reconcile `assets.json`'s existing clip/still
> entries to `clips.csv` / `stills.csv`). Then the render-review is the only open
> item.**
>
> **P-008 (Documentation / manifest consistency refresh) is CLOSED** —
> marketing-media docs-consistency (no generation, no CSV/functional change),
> route builder → reviewer → qa → archivist. Commits `71bf753` + `a07c5a0`
> (base `2925961`): `data/assets.json` counts → 36/52/86, runtime 274/"4:34",
> clips/stills arrays +10 (C25–C34), inline `edl` array rebuilt to **86 ==
> data/edl.csv**; `fetch_assets.sh` comment-only; `HANDOFF.md` refreshed.
> **qa GREEN 10/10** (9 counts reconcile; edl-array == edl.csv; comment-only;
> Commit-1 isolation; safety clean). **reviewer PASS** (zero functional change;
> Codex second-eyes unavailable, single-reviewer). **On-model CONFIRMED:** C27 +
> C33 verified ON-MODEL (short reddish/ginger hair + beard, NOT bald) — the P-006
> on-model risk is CLOSED. Receipt `build-os/receipts/P-008.md`. (P-007 — band
> coverage inserted + PRE2/CH1 re-timed — CLOSED, receipt `build-os/receipts/P-007.md`;
> P-006 — clips generated — CLOSED; P-005 — plan — CLOSED; P-004 — section-sync —
> CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED;
> P-001 — Install Build OS — CLOSED.)

## P-009 — in flight (scope)

- **Reconcile `assets.json`'s pre-existing clip/still entries to the fixed
  `clips.csv` / `stills.csv`.** The 11 earlier-regenerated clips
  (**C01, C04, C06, C07, C13, C15, C16, C19, C22, C23, C24**) still carry
  **pre-regen job_ids / urls** in `assets.json`, diverging from the fixed
  `clips.csv` (which the render actually reads). **Non-functional** manifest drift
  — P-009 brings the manifest's existing rows into line. **No generation, no CSV
  functional change** (the CSVs are the source of truth; this updates the manifest
  to match them).

## Also-open (no packet — for the orchestrator to stage next)

1. **User renders + judges the cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md` — the human-eye confirmation of the 11
   regenerated clips, the P-004 section-sync timing, the P-006/P-007 band
   coverage, and overall pacing. **C27 / C33 on-model is now RESOLVED** (verified
   on-model in P-008) — no longer a render spot-check item. **This is the only
   remaining real work once P-009 lands.**
2. **Sub-beat beat-grid quantization (optional, deferred)** — snap the cuts to the
   **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session).
3. **Selective 2K/4K upscale** — explicitly LAST, only after the cut is locked.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only). The C27/C33 regen is **moot** (verified
  on-model).
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-008 close: `a07c5a0`. Real ahead-of-origin = 2 (not pushed).

---
_P-008 closed 2026-06-29 (docs/manifest refresh + C27/C33 on-model verified).
P-009 in flight — reconcile `assets.json`'s pre-existing clip/still entries to
`clips.csv` / `stills.csv`; after it lands, the user's render-review is the only
open item._
