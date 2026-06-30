# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-014 CLOSED → stills catalog truthful; AUDIT-001 D5-M3 RESOLVED. System
> aligned to canonical; only open CREATIVE step = user render-review.
> Deferred-by-design: beat-lock, upscale.**
>
> **P-014 (Stills-catalog backfill — make the manifest truthful; close AUDIT-001 /
> D5-M3) is CLOSED** — marketing-media (data / catalog edit on `when-it-rains/data/`
> + the inline manifest; the user explicitly authorized — "yes do it"), route
> builder → reviewer → qa → archivist. Commits `6005114` (`stills.csv` **+11 regen
> stills / −4 off-model**, net **+7 → 59 rows**; `clips.csv` **C04 `source_still`
> `regenA1` → `2d0ba697`**, a single 1-line change, other 35 clip rows
> byte-identical; `assets.json` stills **52 → 59** + C04 + `counts.stills` 59) +
> `2223893` (`HANDOFF.md` stills **52 → 59**), base `00af4e3`. The audit (D5-M3)
> found 10 reference-anchored regen stills generated on Higgsfield but never
> cataloged, C04's `source_still` a `regenA1` placeholder, and 4 superseded off-model
> stills lingering. P-014 retrieved the 11 stills' UUIDs / URLs **READ-ONLY from
> Higgsfield (no credits)**; **C04 → `2d0ba697` CONFIRMED** via the clip's
> `start_image` (job `297449bf` `medias.start_image` == `2d0ba697`; still ts 012553
> precedes clip ts 012654); added the 11, pruned the 4 (`22e02845` / `b0f3fd47` /
> `26443c5f` / `ff3797c3`), fixed counts. **Result: 34 / 36 clip `source_still`s now
> resolve (all C01–C34); only EX1 / EX2 `'prior'` intentionally unresolved (a prior
> project — benign / accepted).** **qa GREEN 9/9 + Commit-1 isolation** (stills.csv 59
> rows × 3 cols clean; 11 present / 4 absent; clips.csv C04-only 1-line change, 35
> others byte-identical; assets.json valid, stills 59 / counts.stills 59 / C04
> `2d0ba697` / parity all 36 / edl 86; 34/36 resolve; HANDOFF 59; safety clean).
> **reviewer PASS** (surgically exact — net +7, zero in-place mutations; C04
> corroborated; parity preserved; closes D5-M3 truthfully; no overreach; **Codex
> UNAVAILABLE** — single-reviewer; non-defect caveat — CloudFront URLs not live-hit,
> egress 403 expected, source-derived). Receipt `build-os/receipts/P-014.md`. **The
> stills catalog is now truthful — fully consistent with the live assets (59 stills;
> 34/36 source_stills resolve); AUDIT-001 D5-M3 RESOLVED.**
>
> **System audit AUDIT-001 stands: ALIGNED to canonical** — 6 read-only auditors
> (D1–D6), **zero structural / functional / process defects**; its auto-fixable
> doc-coherence subset was closed by P-013 and the D5-M3 stills-catalog subset by
> P-014. Receipt `build-os/receipts/AUDIT-001.md`.
>
> (P-013 — README + EDIT_MAP doc-coherence fix — CLOSED, receipt
> `build-os/receipts/P-013.md`; P-012 — RENDER_REVIEW.md refreshed to 86/274 —
> CLOSED; P-011 — browser preview tool `preview.html` — CLOSED; P-009 — assets.json
> reconciled to clips.csv — CLOSED; P-008 — docs/manifest refresh + C27/C33 on-model
> verified — CLOSED; P-007 — band coverage inserted + PRE2/CH1 re-timed — CLOSED;
> P-006 — clips generated — CLOSED; P-005 — plan — CLOSED; P-004 — section-sync —
> CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED;
> P-001 — Install Build OS — CLOSED.)

## Open work (no packet — for the orchestrator to stage next)

1. **User reviews + judges the cut — the ONLY remaining real / creative work.** Both
   review instruments are current at **86 cuts / 274.0s**. Two paths, both the
   user's: (a) open `when-it-rains/preview.html` in a browser (silent,
   approximate-timing, streams the 86 cuts from the CDN — the P-011 in-browser review
   aid), and/or (b) the full Mac audio render `scripts/fetch_assets.sh` →
   `scripts/assemble_rough_cut.sh` (with `when-it-rains/RENDER_REVIEW.md`, current at
   86/274, as the timecode-keyed capture checklist). The human-eye confirmation of the
   11 regenerated clips, the P-004 section-sync timing, the P-006/P-007 band coverage,
   and overall pacing. **C27 / C33 on-model is RESOLVED** (verified on-model in P-008).
2. **Sub-beat beat-grid quantization (optional, deferred — POST-APPROVAL)** — snap the
   cuts to the **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync.
   Premature until the cut is approved; needs a rigorous downbeat phase reference + the
   MP3 re-attached (won't survive a new session).
3. **Selective 2K/4K upscale (POST-APPROVAL)** — explicitly LAST, only after the cut
   is emotionally locked.

## Resolved (was open last session)

- **Stills-catalog backfill (D5-M3 / former P-010) — RESOLVED (P-014).** The prior
  "declined / non-functional" framing is **retired**: P-014 cataloged the 10
  reference-anchored regen stills, resolved C04's `source_still` (`regenA1` →
  `2d0ba697`, CONFIRMED via the clip's `start_image`), and pruned the 4 superseded
  off-model stills — stills **52 → 59**, **34 / 36** clip `source_still`s resolve.
  UUIDs retrieved READ-ONLY from Higgsfield (no credits). The only remaining stills
  non-resolvers are EX1 / EX2's `'prior'` pointers (a prior project — accepted /
  benign, **not** an open gap).

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
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-014 close: `2223893` (chain `00af4e3` ← `6005114` ← `2223893`). Local
  commits only — not pushed.

---
_P-014 closed 2026-06-29 (stills-catalog backfill — the manifest is now truthful:
10 regen stills cataloged, C04 `source_still` resolved `regenA1` → `2d0ba697`
[CONFIRMED via the clip's `start_image`], 4 off-model stills pruned, stills 52 → 59,
34/36 source_stills resolve; UUIDs retrieved READ-ONLY from Higgsfield — no credits;
qa GREEN 9/9 + Commit-1 isolation, reviewer PASS, Codex unavailable; AUDIT-001 D5-M3
RESOLVED). No packet active — the system is ALIGNED to canonical and the catalog is
truthful; the user's render-review (interactive preview and/or full Mac audio render)
is the only open creative step. Deferred post-approval: sub-beat quantization;
selective upscale._
