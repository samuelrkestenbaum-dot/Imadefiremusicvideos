# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-012 CLOSED → repo fully coherent; both review instruments current. ONLY
> open item = user render-review (open `when-it-rains/preview.html` in a browser
> and/or run the full Mac audio render). Optional later (post-approval only):
> sub-beat quantization, upscale.**
>
> **P-012 (Refresh `RENDER_REVIEW.md` to the current 86-cut / 274.0s edit,
> doc-only) is CLOSED** — marketing-media (docs-consistency on
> `when-it-rains/RENDER_REVIEW.md`; no generation, no source-CSV / functional
> change), route builder → reviewer → qa → archivist. Commit `59baa8b`
> (RENDER_REVIEW.md rewritten — 86-row per-cut table re-derived from `data/edl.csv`,
> timecodes to 274.0s, cut 86 = 4:34.0; header 86 / 274 / 4:34; watch-points
> refreshed; section times marked CONFIRMED; `preview.html` pointer added; stale
> 76/276/4:36 demoted to explicit history; one file, 213 ins / 164 del), base
> `25a6a7f`. **qa GREEN 8/8 + Commit-1 isolation** (table independently re-derived
> from `edl.csv` — 86/86 rows, 0 timecode mismatches, total 274.0, cut 86 4:34.0;
> zero stale 76/276/4:36 current-claims; C02 11× band-coverage indices verified;
> section starts consistent; Commit-1 isolation; safety clean). **reviewer PASS**
> (every timecode reproducible to the hundredth; watch-points truthful — C27/C33
> faithfully reproduces P-008's video_analysis-confirmed on-model nuance, FINAL
> ~0.25s arithmetically grounded, stale figures demoted not deleted; usability
> preserved; scope clean; **Codex UNAVAILABLE** — single-reviewer). Receipt
> `build-os/receipts/P-012.md`. **Both review instruments are now current at
> 86/274** — `preview.html` (silent browser pass) + `RENDER_REVIEW.md` (audio-render
> checklist); the repo is fully coherent.
> (P-011 — browser preview tool `preview.html` + `build_preview.py` — CLOSED,
> receipt `build-os/receipts/P-011.md`; P-009 — assets.json reconciled to clips.csv
> — CLOSED; P-008 — docs/manifest refresh + C27/C33 on-model verified — CLOSED;
> P-007 — band coverage inserted + PRE2/CH1 re-timed — CLOSED; P-006 — clips
> generated — CLOSED; P-005 — plan — CLOSED; P-004 — section-sync — CLOSED; P-003 —
> SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED; P-001 — Install
> Build OS — CLOSED.)

## Open work (no packet — for the orchestrator to stage next)

1. **User reviews + judges the cut — the ONLY remaining real work.** Both review
   instruments are now current at **86 cuts / 274.0s**. Two paths, both the user's:
   (a) open `when-it-rains/preview.html` in a browser (silent, approximate-timing,
   streams the 86 cuts from the CDN — the P-011 in-browser review aid), and/or
   (b) the full Mac audio render `scripts/fetch_assets.sh` →
   `scripts/assemble_rough_cut.sh` (with `when-it-rains/RENDER_REVIEW.md`, now
   refreshed to 86/274 by P-012, as the timecode-keyed capture checklist). The
   human-eye confirmation of the 11 regenerated clips, the P-004 section-sync
   timing, the P-006/P-007 band coverage, and overall pacing. **C27 / C33 on-model
   is RESOLVED** (verified on-model in P-008) — no longer a render spot-check item.
2. **P-010 (optional / low-priority, declined by user / needs go)** — stills
   backfill: `clips.csv`'s `source_still` values are **8-char prefixes** that don't
   resolve to `stills.csv`'s **full-UUID** keys (a pre-existing id-format quirk
   affecting all clips; **non-functional** — the render reads `mp4_url` from
   `clips.csv` directly). Also **C04's** `source_still` is a `regenA1` **placeholder**
   (known-incomplete from the earlier C04 partial regen). Touches a source CSV +
   a count → needs explicit go.
3. **Sub-beat beat-grid quantization (optional, deferred — POST-APPROVAL)** — snap
   the cuts to the **0.97524s** beat grid (61.5234375 BPM) on top of the
   section-sync. Premature until the cut is approved; needs a rigorous downbeat
   phase reference + the MP3 re-attached (won't survive a new session).
4. **Selective 2K/4K upscale (POST-APPROVAL)** — explicitly LAST, only after the
   cut is emotionally locked.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only). The C27/C33 regen is **moot** (verified
  on-model). P-010 (if taken) also needs a go (touches a source CSV + a count).
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-012 close: `59baa8b` (base `25a6a7f`). Local commits only — not pushed.

---
_P-012 closed 2026-06-29 (refresh RENDER_REVIEW.md to 86/274, doc-only — qa GREEN
8/8, reviewer PASS, Codex unavailable). No packet active — both review instruments
(preview.html + RENDER_REVIEW.md) are current at 86/274 and the repo is fully
coherent; the user's render-review (interactive preview and/or full Mac audio
render) is the only open item. Optional later (post-approval): sub-beat
quantization; selective upscale. P-010 (stills backfill) remains declined / needs
a fresh go._
