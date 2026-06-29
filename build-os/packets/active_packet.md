# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-003 (Section-Time Proposal — `when-it-rains/SECTION_TIMES.md`) is CLOSED**
> — qa GREEN 9/9, reviewer PASS, receipt at `build-os/receipts/P-003.md` (closed
> 2026-06-29, commit `39f84d7`). **P-003 CLOSED → the next packet (beat-lock)
> awaits the user's confirmed section times from `when-it-rains/SECTION_TIMES.md`**
> — especially the **CH1 chorus downbeat: 1:29 vs 1:51** (which also settles
> PRE1). (P-002 — Render-Review Checklist `RENDER_REVIEW.md` — also CLOSED, receipt
> `build-os/receipts/P-002.md`; P-001 — Install Build OS + seed memory — CLOSED,
> receipt `build-os/receipts/P-001.md`.)
>
> The footage audit + regeneration is DONE, the render-review checklist exists
> (P-002), and the section-time proposal worksheet exists (P-003). Two user-driven
> inputs are now outstanding and gate the build packets below: (a) the user's
> human-eye render review via `RENDER_REVIEW.md` (off-machine, user's Mac — the
> cloud session cannot render: CDN egress-blocked, no system ffmpeg), and (b) the
> user's confirm/correct of `SECTION_TIMES.md`. Do not start a packet without
> confirming scope.

## Next-packet candidates (from `when-it-rains/HANDOFF.md`)

1. **User renders + reviews the rough cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`, walking
   `when-it-rains/RENDER_REVIEW.md`. This is the final human-eye confirmation of
   the 11 regenerated clips. Blocks final lock.
2. **User confirms/corrects `SECTION_TIMES.md`** — fills the "Your call" column,
   resolving the SUGGESTED starts (V2/PRE1/CH1, V4/PRE2). Key question: **CH1
   chorus downbeat 1:29 vs 1:51** (also settles PRE1). Gates the beat-lock packet.
3. **Beat-lock the EDL** — once the user confirms section times → build the
   beat-lock script and apply it to `data/edl.csv`: snap the 76 cuts to the
   **0.97524s** beat grid (61.5234375 BPM) **and** trim ~2s so the 276s EDL
   resolves on the 274s mix end (`FOOTAGE_AUDIT.md` §6). Needs the MP3 re-attached
   (it is staged this session but won't survive a new one) + the user's section
   times.
4. **Band-coverage batch (optional, lower priority)** — ~8 clips to reduce C02's
   11× overuse (a pacing issue; C02 is itself on-model). Fire only after the lead
   is locked. **Marketing/media authority — generation = credits = STOP** unless
   inside a confirmed media packet with explicit go.

## Out of scope (explicit)

- Any Higgsfield generation / upscale (credits = external mutation → media packet
  + explicit go only). Upscale is explicitly LAST, after the cut is locked.
- Editing `data/edl.csv`, `clips.csv`, or other `when-it-rains/**` product files
  without a confirmed packet and the user's confirmed section-time inputs.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** _to be defined when a packet is cut._
2. **Commit 2 (optional, same packet):** _to be defined when a packet is cut._

---
_No packet in flight (P-003 closed 2026-06-29). Define/confirm one here before
delegating to builder._
