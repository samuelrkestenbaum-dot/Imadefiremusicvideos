# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

> **P-001 (Install Build OS + seed memory) is CLOSED** — qa GREEN, reviewer PASS,
> receipt at `build-os/receipts/P-001.md` (closed 2026-06-29).
>
> The footage audit + regeneration is DONE. The true next step is **off-machine**:
> the user must render and eyeball the rough cut on their Mac (the cloud session
> cannot render — Higgsfield CDN egress-blocked, no system ffmpeg). So there is no
> cloud-buildable packet in flight until that review returns. Candidates below,
> in HANDOFF "Open threads" order — do not start one without confirming scope.

## Next-packet candidates (from `when-it-rains/HANDOFF.md`)

1. **User renders + reviews the rough cut** (off-machine, user's Mac):
   `scripts/fetch_assets.sh` → `scripts/assemble_rough_cut.sh`. This is the final
   human-eye confirmation of the 11 regenerated clips. Blocks the packets below.
2. **Beat-lock the EDL** — once the user confirms the ambiguous mid-song section
   times (V2/PRE1/CH1, V4/PRE2), regenerate `data/edl.csv` to snap cuts to the
   beat grid **and** trim ~2s so the 276s EDL resolves on the 274s mix end
   (`FOOTAGE_AUDIT.md` §6). Needs the MP3 re-attached + the user's section times.
3. **Band-coverage batch (optional, lower priority)** — ~8 clips to reduce C02's
   11× overuse (a pacing issue; C02 is itself on-model). Fire only after the lead
   is locked. **Marketing/media authority — generation = credits = STOP** unless
   inside a confirmed media packet with explicit go.

## Out of scope (explicit)

- Any Higgsfield generation / upscale (credits = external mutation → media packet
  + explicit go only). Upscale is explicitly LAST, after the cut is locked.
- Editing `data/edl.csv`, `clips.csv`, or other `when-it-rains/**` product files
  without a confirmed packet and the user's section-time inputs.

## Branch base

- `claude/when-it-rains-music-video-fetr0z` (no trunk; judged against branch tip).

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** _to be defined when a packet is cut._
2. **Commit 2 (optional, same packet):** _to be defined when a packet is cut._

---
_No packet in flight (P-001 closed 2026-06-29). Define/confirm one here before
delegating to builder._
