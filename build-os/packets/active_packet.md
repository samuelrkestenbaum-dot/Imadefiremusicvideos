# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-011 CLOSED → `preview.html` delivered. Open item = user render-review
> (open `when-it-rains/preview.html` in a browser, and/or run the full Mac
> render). Optional: refresh the STALE `RENDER_REVIEW.md` to 86/274 (see
> residue).**
>
> **P-011 (Browser-playable EDL preview tool) is CLOSED** — build (read-only
> media-data input → HTML artifact; no generation, no source-CSV change), route
> builder → reviewer → qa → archivist. Commits `645df31`
> (`scripts/build_preview.py` — deterministic generator + self-test, 700 ins) +
> `a4266c5` (`preview.html` — self-contained 86-cut browser review tool, 1498 ins),
> base `46adfc0`. `build_preview.py` reads `data/edl.csv` + `data/clips.csv`,
> joins `clip_key → mp4_url`, emits a self-contained `when-it-rains/preview.html`
> that plays all **86** cuts in EDL order, streaming the clip mp4s from the
> Higgsfield CDN; per-cut overlay, C25–C34 highlight + C27/C33 on-model badge,
> click-to-jump, per-cut PASS/FAIL+note (localStorage + export), graceful per-clip
> failure, SILENT/approximate banner. **qa GREEN 10/10 + Commit-1 isolation**
> (86 cuts in EDL order; all mp4_urls + notes verbatim from CSVs; timecodes
> monotonic ending 274.0; new/on-model flags correct; self-contained — no external
> script/link/@import; deterministic — byte-identical re-runs, Commit-1 `645df31`
> regenerates identically; safety clean). **reviewer PASS** (generator
> deterministic; playback engine no stall/double-advance — failed clips degrade
> not hang; self-contained + honest banner + XSS-safe; scope airtight; **Codex
> UNAVAILABLE** — single-reviewer; the live play-test is the user's — CDN
> egress-blocked here). Reviewer-flagged out of scope: `RENDER_REVIEW.md` is STALE
> (logged as residue). Receipt `build-os/receipts/P-011.md`.
> (P-009 — assets.json reconciled to clips.csv — CLOSED, receipt
> `build-os/receipts/P-009.md`; P-008 — docs/manifest refresh + C27/C33 on-model
> verified — CLOSED; P-007 — band coverage inserted + PRE2/CH1 re-timed — CLOSED;
> P-006 — clips generated — CLOSED; P-005 — plan — CLOSED; P-004 — section-sync —
> CLOSED; P-003 — SECTION_TIMES.md — CLOSED; P-002 — RENDER_REVIEW.md — CLOSED;
> P-001 — Install Build OS — CLOSED.)

## Open work (no packet — for the orchestrator to stage next)

1. **User reviews + judges the cut** — **the only remaining real work.** Two
   paths, both the user's: (a) open `when-it-rains/preview.html` in a browser
   (silent, approximate-timing, streams the 86 cuts from the CDN — the P-011
   in-browser review aid), and/or (b) the full Mac render
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`. The human-eye
   confirmation of the 11 regenerated clips, the P-004 section-sync timing, the
   P-006/P-007 band coverage, and overall pacing. **C27 / C33 on-model is
   RESOLVED** (verified on-model in P-008) — no longer a render spot-check item.
2. **Refresh the STALE `RENDER_REVIEW.md` (optional, reviewer-flagged in P-011,
   needs go)** — `when-it-rains/RENDER_REVIEW.md`'s per-cut checklist still
   describes the **pre-band-coverage 76-cut / 276.0s** edit (predates P-004
   section-sync + P-006/P-007 band coverage). `edl.csv` + `preview.html` are
   correct at **86/274**; `preview.html` supersedes the static checklist for the
   live review. A refresh to 86/274 (+ updated watch-points: band coverage added,
   on-model confirmed, section times confirmed) is an OPTIONAL follow-up pending
   the user's decision.
3. **P-010 (optional / low-priority, needs user go)** — stills backfill:
   `clips.csv`'s `source_still` values are **8-char prefixes** that don't resolve
   to `stills.csv`'s **full-UUID** keys (a pre-existing id-format quirk affecting
   all clips; **non-functional** — the render reads `mp4_url` from `clips.csv`
   directly). Also **C04's** `source_still` is a `regenA1` **placeholder**
   (known-incomplete from the earlier C04 partial regen). Touches a source CSV +
   a count → needs explicit go.
4. **Sub-beat beat-grid quantization (optional, deferred)** — snap the cuts to the
   **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session).
5. **Selective 2K/4K upscale** — explicitly LAST, only after the cut is locked.

## Out of scope (explicit, until a fresh go)

- Any **further** Higgsfield generation / upscale (credits = external mutation →
  media packet + explicit go only). The C27/C33 regen is **moot** (verified
  on-model). P-010 (if taken) also needs a go (touches a source CSV + a count).
- The `RENDER_REVIEW.md` refresh (item 2) is **not** authorized — needs go.
- No push / merge / deploy.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).
  HEAD at P-011 close: `a4266c5` (base `46adfc0`). Local commits only — not pushed.

---
_P-011 closed 2026-06-29 (browser preview tool `preview.html` + `build_preview.py`
— qa GREEN 10/10, reviewer PASS, Codex unavailable). No packet active — the user's
render-review (interactive preview and/or full Mac render) is the only open item.
Optional later: refresh the STALE RENDER_REVIEW.md to 86/274; P-010 (stills
backfill)._
