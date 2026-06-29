# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-004 (EDL section-sync to confirmed times — `when-it-rains/data/edl.csv`
> rewrite) is CLOSED** — qa GREEN 10/10 + Commit-1 isolation, reviewer PASS, receipt
> at `build-os/receipts/P-004.md` (closed 2026-06-29; commits `0ac19d2` script +
> `72dff55` artifacts, base `bbcc36f`, not pushed). **P-004 CLOSED → the next packet
> awaits the user's render-judgment of the section-synced cut** on their Mac.
> Candidate follow-ups: **added cuts for the ballooned CH1 / PRE2** (band-coverage
> batch — those sections were stretched ×1.55 / ×1.64 and may drag), and an
> **optional sub-beat beat-grid quantization** (still deferred — needs a rigorous
> downbeat phase reference). (P-003 — SECTION_TIMES.md — CLOSED, receipt
> `build-os/receipts/P-003.md`; P-002 — RENDER_REVIEW.md — CLOSED, receipt
> `build-os/receipts/P-002.md`; P-001 — Install Build OS + seed memory — CLOSED,
> receipt `build-os/receipts/P-001.md`.)
>
> The user has now CONFIRMED the section times (CH1 = 1:29 etc.) and the EDL is
> section-synced to them (cumulative starts exact, total 274s; original backed up
> byte-exact at `data/edl_original_backup.csv`). The remaining user-driven inputs:
> (a) the user's render-judgment of the re-timed cut, and (b) the broader human-eye
> render review via `RENDER_REVIEW.md` — both off-machine on the user's Mac (the
> cloud session cannot render: CDN egress-blocked, no system ffmpeg). Do not start a
> packet without confirming scope.

## Next-packet candidates (HANDOFF + P-004 residue)

1. **User renders + judges the section-synced cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md`. This is the human-eye confirmation of both the
   11 regenerated clips AND the new section-sync timing. Blocks the follow-ups below.
2. **Added-cuts packet for ballooned CH1 / PRE2 (conditional)** — fire only **if**
   the user reports CH1 (×1.55, cuts now ~5–6.5s) and/or PRE2 (×1.64) DRAG on
   playback. The fix is **added cuts** (band-coverage batch, `RENDER_REVIEW.md` §7),
   NOT stretched holds. **Marketing/media authority — generation = credits = STOP**
   unless inside a confirmed media packet with explicit go.
3. **Sub-beat beat-grid quantization (optional, deferred)** — snap the 76 cuts to
   the **0.97524s** beat grid (61.5234375 BPM) on top of the section-sync. Needs a
   rigorous downbeat phase reference + the MP3 re-attached (staged this session, will
   not survive a new one). Section-sync (P-004) was the coarser confirmed-times pass.
4. **Band-coverage batch (optional, lower priority)** — ~8 clips to reduce C02's 11×
   overuse (a pacing issue; C02 is itself on-model); overlaps with candidate 2. Fire
   only after the lead is locked. **Media authority — credits = STOP** without go.

## Out of scope (explicit)

- Any Higgsfield generation / upscale (credits = external mutation → media packet
  + explicit go only). Upscale is explicitly LAST, after the cut is locked.
- Further editing `data/edl.csv`, `clips.csv`, or other `when-it-rains/**` product
  files without a confirmed packet and the user's render-judgment of the current
  section-synced cut.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** _to be defined when a packet is cut._
2. **Commit 2 (optional, same packet):** _to be defined when a packet is cut._

---
_No packet in flight (P-004 closed 2026-06-29). Define/confirm one here before
delegating to builder._
