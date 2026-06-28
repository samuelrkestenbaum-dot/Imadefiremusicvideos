# Pre-Render Edit Review — "When It Rains" (4:36)

**Method & honesty note.** This is a *structural* review computed from the 76-cut
EDL + asset metadata — **not** a viewing. I could not render or watch the cut in
the cloud session (the Higgsfield CDN and the song WAV are both unreachable here,
and ffmpeg won't install). So findings split into two kinds:

- **STRUCTURAL** — provable from the edit data (usage counts, ratios, pacing).
  Trust these now.
- **VERIFY-ON-PLAYBACK** — likeness drift, woman consistency, "weak clip" calls.
  These need your eyes on the actual footage. I've pointed you to the exact
  timecodes so you can confirm/deny each in seconds.

Do the render first (below), then watch with this open.

---

## Step 0 — render the rough cut (on your machine)

```bash
cd when-it-rains
brew install ffmpeg            # or: sudo apt-get install ffmpeg
bash scripts/fetch_assets.sh   # downloads 26 clips + 42 stills
cp /path/to/when_it_rains.wav song.wav
bash scripts/assemble_rough_cut.sh   # -> when_it_rains_roughcut.mp4
```

---

## Overall shot ratio (actual vs treatment target)

| | Performance | Story (man) | Woman | Insert |
|---|---|---|---|---|
| **Actual** | 37% | 38% | 8% | **18%** |
| **Target** | 45% | 45% | 10% | 10% |

Two structural gaps fall straight out of this: **performance is under-weight** and
**inserts are nearly double target.** The fix is the same one your instinct
named — add band coverage, and convert some abstract-rain insert slots to it.
Don't add *more* inserts; you're already over.

---

## 1. Overused shot — the #1 structural problem  ·  STRUCTURAL

**`C02` (the single singer close-up) appears 11 times for 37 seconds** — that's
13% of the whole video carried by one clip. The "performance" 37% is really
*4 recycled band wides + 1 singer CU on repeat.*

Every C02 placement (watch for the repeat becoming visible):
`0:08 · 0:18 · 0:42 · 0:53 · 1:06 · 1:31 · 1:59 · 2:26 · 2:49 · 3:22 · 3:54`

→ These are the prime slots to **swap for new band coverage** once it exists
(rows 6, 15, 19, 33, 41, 46, 54, 64 especially — keep a couple of true singer CUs
at 0:08 intro and 2:26/3:54 emotional peaks).

The other recycled clips are fine but worth noting: `C09/C12/C20` (band) 5× each,
`C13/C07/C04/C15` 4× each, `C03` (rain glass) 4×.

## 2. Band coverage is thin — only 5 distinct performance setups  ·  STRUCTURAL

Distinct band assets: **4 instrument/band wides** (C01, C09, C12, C20) + **1
singer CU** (C02) + 1 final CU (C24). No drummer CU, no guitar hands, no keys, no
bass, no mic/cable/amp/cymbal inserts. That's why the performance side leans so
hard on C02. Band coverage is the editing glue that lets the memory shots breathe
without overusing them — this is the highest-leverage next generation batch.
**Held shot list in §7** (not generated yet, per your call).

## 3. Montage-risk sections  ·  STRUCTURAL + VERIFY

- **V1 (0:18–0:48)** — 12s of inserts (ocean/river/rain/EX1) in a 30s verse. Risk:
  pretty-but-floaty, "AI wallpaper." Watch whether it tracks as *him remembering*
  or just B-roll. Likely fix: replace one insert (row 11 river or row 9 ocean) with
  a band or held-on-his-face beat.
- **CH2 (3:34–3:58)** — 8 cuts, 3.0s avg, rapid water/thunder/mirror/woman fire.
  Intended to be fast, but with 3 woman shots in it (see §4) it can tip into
  trailer-montage. Watch 3:42–3:51.
- **BRIDGE (3:58–4:21)** — **performance-starved: 3s of band, 0s singer**, vs 9s
  woman + 11s story. This is your emotional peak, but a peak with almost no band
  cutting can *sag* energetically. Watch whether it feels like a climax or a
  slow-down. Likely fix: add 1–2 band-at-peak cuts here (drummer-hard CU is ideal).

## 4. Woman-consistency risk zones  ·  VERIFY-ON-PLAYBACK

She's generated from **4 different source stills** that were never locked to one
face, so the risk is concentrated where those sources sit *back-to-back*. If at
these moments she reads as the same remembered woman → leave it (memory
fragmentation, a feature). If she reads as **different women** → that's where to
lock a Soul/Element and regenerate just those.

| Zone | Timecodes | Clips (sources) | What to check |
|------|-----------|-----------------|---------------|
| **V4 mirror run** | 2:44 → 2:52 → 2:56 | C15, C16, C15 (76f40277, e6d61b52) | two different mirror faces ~8s apart |
| **CH2 burst** | 3:42 → 3:45 → 3:48 | C15, C07, C21 (76f40277, d45125d9, 76054c72) | three sources in 9s |
| **BRIDGE flood** | 4:03 → 4:06 → 4:15 → 4:18 | C16, C11, C21, C15 (four different sources) | **highest risk** — 4 faces in 15s |

If only one zone reads wrong, fix only that zone. The distant/turning shots
(C11, C21) are lower risk than the face-forward mirror shots (C15, C16).

## 5. Likeness-drift watch points (the man)  ·  VERIFY-ON-PLAYBACK

His face comes from two still families — the **band stills** (warm, one set) and
the **story stills** (cool, another set). Drift shows worst where the two families
cut against each other on his face:

- **INTRO/V1:** `0:04 C01 → 0:08 C02 → 0:11 C04` (band-face → singer-face → story-face)
- **FINAL:** `4:24 C24 (8de0efa8 portrait) → 4:27 C23 (12a29611 window)` — last
  impression of him; if these two faces don't match it's the worst place for it.
- The 11× C02 also means: if C02's likeness is even slightly off, that error
  repeats 11 times. Confirm C02 is your best-likeness singer take before relying on it.

## 6. Sections that should hold (structural confidence)

- **V2 (0:48–1:18)** — best-balanced story verse: 18s story, the C07 reflection
  beat anchors it, paced 3.8s. Should track well.
- **V4 (2:39–3:09)** — strong narrative spine (drawer → mirror → he reaches),
  story-led as intended. Only risk is the §4 mirror-face match.
- **CH1 (1:43–2:08)** — clean first release: band-forward (13s perf), water punches,
  one woman glimpse. Good template for what CH2 should feel like.

---

## 7. HELD — band-coverage generation plan (not run yet)

Fire this **only after** the rough cut confirms the §1/§2 thinness (it will). All
animate from new stills built on the man's locked selfies / existing band stills;
silent 5s, one motion each — same recipe as the current library. ~8 clips ≈ 60
credits.

1. Drummer CU — sticks/cymbal hit, hard on the backbeat (chorus/bridge glue)
2. Guitar hands — fretboard + strum, rhythm motion
3. Keys/piano — hands on keys, warm lamp
4. Bassist silhouette — backlit, slow sway
5. Full-band chorus push-in — slow dolly toward the stage (new angle, not C12 recycle)
6. Singer profile — side-light, into the mic (breaks the C02 front-on monotony)
7. Singer straight-to-lens — a *second* front CU so C02 isn't alone
8. Detail inserts — mic head / coiled cable / amp grille / cymbal shimmer (4 micro-shots)

Then EDL edits: swap ~6 of the 11 C02 placements for #1–#7, drop 1–2 V1 inserts,
add #1 (drummer) into the BRIDGE at ~4:09.

## 8. Do-NOT-do-yet (your call, agreed)

- ❌ No upscale until the cut is emotionally locked.
- ❌ No brunette re-gen unless §4 reads as multiple women on playback.
- ❌ No broad new generation — only the targeted §7 batch, and only after the render.

---

### TL;DR
The edit is structurally sound and paced right. Two provable problems: **one
singer CU doing 11× the work**, and **band coverage too thin (5 setups)** — both
solved by §7. Everything else (woman consistency, likeness drift, weak clips) is
**verify-on-playback** — render it, watch with §4/§5 timecodes open, and the fix
list writes itself.
