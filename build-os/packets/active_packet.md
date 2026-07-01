# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-017 CLOSED → the Higgsfield-native wan2_7 lip-sync pipeline exists as CODE
> ONLY and is SHELVED pending mechanism validation. NO packet is active.** The
> live / authoritative edit is now the **P-016 107-cut / 274.00 s late-90s / 2000s
> director's cut** (`data/edl.csv`). The open real work is the user's push go +
> render-review; the lip-sync mechanism is UNPROVEN (see below).**
>
> **P-017 (Higgsfield-native lip-sync pipeline, CODE ONLY) is CLOSED** — build,
> route orchestrator → builder → qa → reviewer → archivist. Commits `8dd6c41`
> (Commit-1: `scripts/slice_vocals.py` + durable committed `analysis/line_map.json`
> [43 lines, 27 in-scope, 3 still job_ids embedded] + `scripts/test_slice_vocals.py`;
> 4 files / 1215 ins; green in isolation 23/0/4) + `eed8ed8` (Commit-2 tip:
> `scripts/lipsync_driver.py` [gated wan2_7 call-plan — DRY-RUN default = zero
> network; `--go` refuses by `SystemExit`; path-b mint+Mac-PUT+confirm or path-c
> web-app upload] + `scripts/swap_lipsync_clips.py` [NON-DESTRUCTIVE backup+repoint]
> + driver/swap checks; 3 files / 438 ins), base `60b297d`; diff 6 files / +1653.
> **qa GREEN:** suite 42/42/0 (full-slice branch executed); zero-network dry-run
> both paths, `--go` refused; non-destructive swap, preflight PASS before+after;
> Commit-1 green in isolation 23/0/4; safety grep clean (no secrets, song.mp3 +
> audio_segments/ gitignored, data/ empty). **reviewer PASS** — gated-generation
> safety airtight, no hardcoded md5, reversible swap, honest about the assumed
> wan2_7 audio_references shape; **Codex UNAVAILABLE — reviewer ran SOLO**. Receipt
> `build-os/receipts/P-017.md`. **HONEST STATUS:** the CODE is correct + shelved-ready
> but the wan2_7 mechanism is UNPROVEN / SO FAR FAILING — 3 render attempts failed,
> a 4th (image `686b2b8a`, audio `720e0e5a`) in flight at close; if it also fails,
> true lip-sync likely needs FILMED footage.
>
> **P-016 (director's cut — late-90s / 2000s aesthetic) receipt debt CLEARED this
> close.** Commit `60b297d` (also P-017's base) replaced the 70s rough cut: 24 new
> reference-anchored Higgsfield clips (buzz-cut / fit / soaked 2000s frontman +
> consistent memory woman + atmosphere; bleach-bypass; ~198 credits),
> `scripts/build_edit_v2.py` sequenced `data/edl.csv` = 107 cuts / 274.00 s / no
> clip repeating within 8 cuts; preflight PASS 0 warnings; old 70s edit preserved
> as `data/{edl,clips,stills}.70s.csv`; `TREATMENT.md` re-skinned; frontman
> likeness corrected across 3 anchor iterations (canonical still `00d037d0`). qa
> PASS, reviewer PASS — caveats: a few perf clips "shaved" not "buzzed" (possible
> re-roll), AI lip-sync not frame-accurate. Receipt `build-os/receipts/P-016.md`.
>
> (P-015 — beat-lock analysis + gated beat-aware EDL variant — CLOSED, receipt
> `build-os/receipts/P-015.md`; render pipeline `82ac71e` + `9ba310b` recorded as
> shipped. P-014 — stills-catalog backfill, D5-M3 RESOLVED — CLOSED, receipt
> `build-os/receipts/P-014.md`; AUDIT-001 — system ALIGNED to canonical — receipt
> `build-os/receipts/AUDIT-001.md`; P-013 — README + EDIT_MAP doc-coherence —
> CLOSED; P-012 — RENDER_REVIEW.md refreshed — CLOSED; P-011 — browser preview tool
> `preview.html` — CLOSED; P-009 — assets.json reconciled — CLOSED; P-008 —
> docs/manifest refresh + C27/C33 on-model verified — CLOSED; P-007 — band coverage
> inserted + PRE2/CH1 re-timed — CLOSED; P-006 — clips generated — CLOSED; P-005 —
> plan — CLOSED; P-004 — section-sync — CLOSED; P-003 — SECTION_TIMES.md — CLOSED;
> P-002 — RENDER_REVIEW.md — CLOSED; P-001 — Install Build OS — CLOSED.)

## Open work (no packet — for the orchestrator to stage next)

1. **PUSH GO — the whole session is local-only.** Commits `3b4bc4d` + `0320218` +
   `60b297d` (P-016) + `8dd6c41` + `eed8ed8` (P-017) + the archivist close commit
   await the user's explicit push. No push / merge / deploy without go.
2. **wan2_7 lip-sync mechanism — VALIDATE OR PIVOT (P-017).** The lip-sync CODE is
   shelved-ready but the wan2_7 mechanism is UNPROVEN and SO FAR FAILING (3 render
   attempts failed; a 4th with proper media_ids [image `686b2b8a`, audio
   `720e0e5a`] was in flight at close). If it fails, the pivot is FILMED
   performance footage of the artist (graded + intercut). Any live wan2_7 run
   needs a human `--go` + the live MCP (credits).
3. **User reviews + judges the cut — the ONLY remaining real / creative work.** The
   authoritative live edit is now the **P-016 107-cut / 274.00 s** 2000s director's
   cut (`data/edl.csv`). Two paths, both the user's: (a) `when-it-rains/preview.html`
   in a browser (silent, approximate-timing — NOTE: predates P-016, still reflects
   the older 86-cut edit; the authoritative edit is the 107-cut `data/edl.csv`),
   and/or (b) the full Mac render (`scripts/render_master.sh`, the one-shot
   validate→fetch→assemble→verify wrapper gated on `scripts/preflight_edl.py`, or
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`) with
   `when-it-rains/RENDER_REVIEW.md` as the timecode-keyed capture checklist (NOTE:
   RENDER_REVIEW.md also predates P-016 — refresh to 107/274.00 is deferred).
   **BLOCKED in-session:** the real footage master cannot render here — the
   Higgsfield CDN (`d8j0ntlcm91z4.cloudfront.net`) is egress-blocked (403, org
   policy); unblock = the user allowlisting the host OR rendering on a connected
   machine (a policy boundary, not routable). C27 / C33 on-model is RESOLVED (P-008).
4. **Promote the beat-locked variant — USER-GATED (P-015 delivered it).** If the
   pacing wants tightening to the beat, `data/edl_beatlocked.csv` is a ready,
   non-destructive alternative (86 rows, section starts preserved, 274.0 s, 84/86
   cuts snapped to the 0.9752381 s grid; ±50 ms alignment 8.1 % → 84.9 %). Swapping
   it into the live `data/edl.csv` is the user's call after human review — do not
   promote without an explicit go. Caveat: it snaps to BEATS, not downbeats
   (downbeat times in `beats.json` are advisory only).
5. **Selective 2K/4K upscale (POST-APPROVAL)** — explicitly LAST, only after the cut
   is emotionally locked; needs footage + credits.

## Resolved (was open last session)

- **Sub-beat beat-grid quantization (former deferred item) — a gated variant now
  EXISTS (P-015).** The prior "still deferred, needs a rigorous downbeat phase
  reference" framing is advanced: P-015 built the beat-lock capability
  (`scripts/beat_lock.py` + 20-check suite) and produced the non-destructive variant
  `data/edl_beatlocked.csv`. Only its **promotion** into the live edit remains open
  (user-gated, item 2 above). It snaps to BEATS not downbeats (downbeat phase
  confidence LOW ≈ 720 ms) — an honest, recorded limitation, not a defect.
- **Stills-catalog backfill (D5-M3 / former P-010) — RESOLVED (P-014).** Stills
  52 → 59, C04 `source_still` resolved `regenA1` → `2d0ba697` (CONFIRMED via the
  clip's `start_image`), 4 off-model stills pruned; 34 / 36 clip `source_still`s
  resolve. Only EX1 / EX2 `'prior'` remain (a prior project — accepted / benign).

## Low / cosmetic (from AUDIT-001)

- **D1-01** — the ClaudeOrchestrator source `global-claude-md.md` says "(global) /
  user scope" even for project installs (wording-only). **GATED** — fixing it edits
  the source repo, outside this project's `build-os/`-only authority.
- **D3-M1** — receipts say "not pushed" but `origin` mirrors HEAD (wording imprecision,
  not an ungated mutation). Cosmetic; phrase future receipts precisely.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only). The C27/C33 regen is **moot** (verified
  on-model). P-014's stills backfill is **done** (retrieval was READ-ONLY — no
  credits); any **new** generation needs a fresh go.
- **Promoting `data/edl_beatlocked.csv`** into the live edit without an explicit go.
- No push / merge / deploy. **NOT YET PUSHED (whole session):** `3b4bc4d` +
  `0320218` + `60b297d` (P-016) + `8dd6c41` + `eed8ed8` (P-017) + the archivist's
  `build-os/` close commit — all local-only, awaiting the user's push go. (Earlier
  P-015 / render-pipeline commits `c65748e` / `9370af3` / `82ac71e` / `9ba310b`
  are also still unpushed.)
- **Live wan2_7 lip-sync generation** (credits) without a human `--go` + the live MCP.
- **Any re-roll of the "shaved-not-buzzed" perf clips** (P-016) without a fresh
  media-packet go (credits).

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-017 close: `eed8ed8` (chain `60b297d` ← `8dd6c41` ← `eed8ed8`; P-017's
  base `60b297d` = the P-016 director's cut), plus the archivist's own `build-os/`
  close commit on top. Local commits only — not pushed.

---
_P-017 closed 2026-07-01 (Higgsfield-native wan2_7 lip-sync pipeline, CODE ONLY —
`scripts/slice_vocals.py` + durable `analysis/line_map.json` [43 lines, 27 in-scope,
3 still job_ids] + gated `scripts/lipsync_driver.py` [DRY-RUN default, `--go`
refuses by SystemExit] + non-destructive `scripts/swap_lipsync_clips.py`; qa GREEN
suite 42/42/0, Commit-1 iso 23/0/4, dry-run zero-network both paths, safety clean;
reviewer PASS, Codex unavailable — solo; base `60b297d`, tip `eed8ed8`, diff 6 files
/ +1653; HONEST STATUS: code shelved-ready but the wan2_7 MECHANISM is UNPROVEN / SO
FAR FAILING — 3 render attempts failed, a 4th in flight at close → true lip-sync
likely needs FILMED footage). **P-016 receipt debt CLEARED this close** (director's
cut — late-90s / 2000s bleach-bypass re-edit replacing the 70s cut; 24 new
reference-anchored Higgsfield clips ~198 credits; `build_edit_v2.py` sequenced
`data/edl.csv` = 107 cuts / 274.00 s / no repeat-within-8; preflight PASS 0
warnings; old 70s edit preserved as `data/*.70s.csv`; commit `60b297d`; qa PASS,
reviewer PASS — caveats: a few perf clips "shaved" not "buzzed", AI lip-sync not
frame-accurate). NO packet active — the live / authoritative edit is now the P-016
107-cut / 274.00 s 2000s director's cut. Open work: the user's push go; validate or
pivot the wan2_7 lip-sync mechanism (→ filmed footage if it fails); the user's
render-review (in-session render still blocked on the 403 egress-blocked Higgsfield
CDN). All session commits (`3b4bc4d` / `0320218` / `60b297d` / `8dd6c41` /
`eed8ed8`) + this close are local-only, awaiting an explicit push go._
