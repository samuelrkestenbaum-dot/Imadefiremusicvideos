# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-005 CLOSED → next = P-006 generation (GATED: credits) then P-007 edl
> insert/re-time (GATED). Plan in `when-it-rains/BAND_COVERAGE_PLAN.md`.**
>
> **P-005 (Band-coverage add-cuts plan — `when-it-rains/BAND_COVERAGE_PLAN.md`,
> spec only) is CLOSED** — qa GREEN 10/10 + Commit-1 isolation, reviewer PASS
> (Codex second-eyes unavailable — single-reviewer), receipt at
> `build-os/receipts/P-005.md` (closed 2026-06-29; commits `cff6043` plan +
> `bbd952a` REVIEW §7 pointer, base `5d61a89`, not pushed). It specifies 10 new
> band-only cuts (C25–C30 PRE2, C31–C34 CH1), each fully recipe'd, to break the long
> PRE2 / CH1 holds. **No generation, no edl edit** — both deferred to the gated
> packets below. (P-004 — EDL section-sync — CLOSED, receipt
> `build-os/receipts/P-004.md`; P-003 — SECTION_TIMES.md — CLOSED; P-002 —
> RENDER_REVIEW.md — CLOSED; P-001 — Install Build OS + seed memory — CLOSED.)

## Next-packet candidates (P-005 residue)

1. **P-006 — generate the 10 staged clips on Higgsfield (GATED).** Generate
   C25–C34 per the recipes in `when-it-rains/BAND_COVERAGE_PLAN.md`. **Marketing/media
   authority — generation = credits = external mutation = STOP** unless inside a
   confirmed media packet with the user's explicit go.
2. **P-007 — insert the 10 clips into `data/edl.csv` + re-time PRE2 / CH1 (GATED).**
   After P-006 lands the clips, splice them into the EDL and re-time PRE2 / CH1 to
   ~3.3s avg per cut. **Edit authority — needs explicit go** (and follows P-006).
   At generation/insert time, mind the 2 non-blocking notes: (a) make C26 (full-band
   push-in) read distinct from existing C09 (also a push-in); (b) the plan's relative
   `data/edl.csv` path is correct from `when-it-rains/` — from repo root use
   `when-it-rains/data/edl.csv`.
3. **User renders + judges the section-synced cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md` — still-open human-eye confirmation of the 11
   regenerated clips AND the P-004 section-sync timing.
4. **Sub-beat beat-grid quantization (optional, deferred)** — snap the 76 cuts to
   the **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (won't survive a new
   session). Section-sync (P-004) was the coarser confirmed-times pass.

## Out of scope (explicit)

- Any Higgsfield generation / upscale (credits = external mutation → media packet
  + explicit go only). P-006 generation is GATED. Upscale is explicitly LAST, after
  the cut is locked.
- Editing `data/edl.csv`, `clips.csv`, or other `when-it-rains/**` product files
  (incl. the P-007 insert/re-time) without a confirmed packet and explicit go.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** _to be defined when a packet is cut._
2. **Commit 2 (optional, same packet):** _to be defined when a packet is cut._

---
_No packet in flight (P-005 closed 2026-06-29). Define/confirm one here before
delegating to builder._
