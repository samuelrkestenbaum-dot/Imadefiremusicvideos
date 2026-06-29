# BAND_COVERAGE_PLAN — staged ADD-CUTS spec for PRE2 + CH1 pacing

> **This packet (P-005) PLANS ONLY.** It generates nothing and edits no product
> file. It is the precise spec that two downstream, separately-gated packets read:
> - **P-006** — generate the 10 stills + 10 clips on Higgsfield. **Spends credits →
>   gated media packet, explicit go required.** Do NOT generate from this doc.
> - **P-007** — insert + re-time the 10 new cuts into `data/edl.csv`. **Gated edit
>   to a product file.** Do NOT touch `edl.csv` from this doc.
>
> Lineage: `REVIEW.md` §7 (held band-coverage idea list — this doc is the concrete
> realization of it, not a duplicate), §1/§2 (C02 11× overuse; C12/C10/C09/C20
> recycling; only 5 distinct performance setups), §6 (CH1 = the good first-release
> chorus template). `FOOTAGE_AUDIT.md` §8 / §5 (the bald root-cause = **zero-reference
> stills**; the recipe + on-model anchor `5cc8239a`). `HANDOFF.md` "Higgsfield
> working context" (recipe params, the 3 selfie media IDs, the preset id).

## 1. Why these two sections, and the pacing target

P-004 section-synced the EDL to the user's confirmed section times. That stretched
two rising sections so their **cut count** no longer matches their (now fixed) span
— they **drag**:

| Section | Span (FIXED) | Cuts now | avg now | max now | New count | New avg | Add |
|---|---|---|---|---|---|---|---|
| **PRE2** | **41.00s** | 6 | 6.83s | 8.2s (C17) | **12** | **3.42s** | **+6** |
| **CH1**  | **38.75s** | 8 | 4.84s | 6.2s (C12) | **12** | **3.23s** | **+4** |

**Pacing math (qa re-derives from the fixed spans):**
- PRE2: 41.00 / 6 = **6.83s** avg today → 41.00 / 12 = **3.42s** avg after +6.
- CH1: 38.75 / 8 = **4.84s** avg today → 38.75 / 12 = **3.23s** avg after +4.

**Spans are FIXED** — section start/end times are locked by P-004; only the cut
**count** changes. The new + existing cuts re-distribute *within* the fixed span.
**P-007 owns the actual re-time** (it will re-balance all 12 durations to fill the
span exactly). This doc only gives each NEW cut a **target duration** consistent
with hitting the ~3.2–3.4s average, and the existing row it slots after. P-007 may
shave the existing PRE2/CH1 holds (e.g. C17's 8.2s, C12's 6.2s) to absorb the new
cuts without changing the span.

## 2. Content rule (narrative-safe by construction)

Every new cut is **band-performance world ONLY** — no woman, no story/reflection
content. Reasons: (a) keeps the locked narrative intact (PRE2/CH1 are performance
beats, not memory beats); (b) avoids the woman-likeness-consistency risk
(`FOOTAGE_AUDIT.md` §3, C16 auburn drift); (c) directly attacks the §1/§2 problem —
breaks the **C12 / C10 / C09 / C20 / C02 recycling** by adding genuinely new band
setups (drummer CU, guitar hands, keys, second front singer, profile, push-in).

- **PRE2 = RISING-intensity band** (storm build): drummer building, full-band
  push-in, singer profile turning up, bass/keys driving. Storm/dark-lit world.
- **CH1 = CHORUS-energy band** (the good release template, §6): drummer hard CU,
  guitar hands, a *second* front-singer CU, keys — warm performance room.

## 3. Shared recipe (matches `HANDOFF.md` + `FOOTAGE_AUDIT.md` §8 EXACTLY)

> Every still **MUST be reference-anchored.** The bald failures (`FOOTAGE_AUDIT.md`
> §5) came from `nano_banana_2` stills generated with **zero reference images** —
> pure text — so the lead drifted bald under dark prompts. Never repeat that here.

**Still (per new cut):**
- model `nano_banana_2`, **16:9**, **1k**.
- **reference-anchored** via `medias:[{role:"image", value:<id>}]`, using the man's
  three uploaded selfie media IDs and/or the proven on-model anchor:
  - selfie `fd3902a2-34d6-41a8-92c4-cb1082cb633d`
  - selfie `81d923ee-cc81-41ea-9dc0-39d40b3d8cd4`
  - selfie `bb1fa35c-6c75-42ad-93f5-48de485e35b6`
  - on-model anchor **`5cc8239a`** (C20's still — best receding-hairline match)
- **on-model line (verbatim in every man-facing prompt):** "short cropped
  red-blonde hair, receding hairline, reddish beard, NOT bald."

**Clip (per new cut):**
- `generate_video`, model `kling3_0`, `mode:"std"`, `sound:"off"`, `duration:5`,
  role `start_image` (the still is the start frame).
- **`declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"`** (declines the
  "IN THE DARK" preset intercept) **only for storm/dark-lit shots** — i.e. **all 6
  PRE2 cuts** (PRE2 is a storm build). **Warm interior CH1 band shots do NOT need
  it** — the 4 CH1 cuts omit the declined preset. (Each cut below says which.)

Clips render at 5s; P-007 trims each to the **target duration** below when placing.

## 4. The 10 new cuts

Clip-ids start at **C25** and run **C25–C34** in order. Existing EDL ids are
**C01–C24 + EX1** (C25+ does NOT collide; EX2 appears in docs but is not in the EDL).

### PRE2 — +6 cuts (C25–C30), storm-build band, RISING intensity
*All 6 are storm/dark-lit → include `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"`.*
*All anchored on `5cc8239a` + the man's selfies for any singer-facing shot.*

| clip-id | shot | still anchor | declined preset? | still prompt (draft) | slot after row | target dur |
|---|---|---|---|---|---|---|
| **C25** | Drummer CU, sticks building — accelerating fills on the rising build | `5cc8239a` + selfies | **yes** | "1970s rain drama, storm-lit band room, close-up of the drummer's hands and sticks building an accelerating fill on the toms, lightning glow through the window, motion blur on the sticks, moody blue-grey key light, film grain" | **51** (C17, 8.2s) | **3.4s** |
| **C26** | Full-band push-in — slow dolly toward the stage as intensity rises (NEW angle, not a C12/C20 recycle) | `5cc8239a` | **yes** | "1970s rain drama, slow dolly push-in toward a full band mid-performance in a storm-lit wood-panelled room, the whole group leaning into a rising build, rain on the windows behind, warm-to-cool contrast, cinematic 35mm" | **52** (C18, 6.56s) | **3.4s** |
| **C27** | Singer PROFILE turning up — side-light, chin lifting into the build (breaks C02 front-on) | `5cc8239a` + selfies | **yes** | "1970s rain drama, side-lit profile of the male singer (short cropped red-blonde hair, receding hairline, reddish beard, NOT bald) lifting his chin and leaning into a rising vocal, storm light raking across his face, dark band room, film grain" | **53** (C12, 6.56s) | **3.4s** |
| **C28** | Bassist driving — backlit, hand working the strings, slow forward sway | `5cc8239a` | **yes** | "1970s rain drama, backlit bassist silhouette in a storm-lit band room, hand driving low on the strings, slow forward sway, rim light from a window, blue-grey haze, cinematic" | **54** (C02, 6.56s) | **3.4s** |
| **C29** | Keys driving — hands pushing chords harder under a lamp as the build climbs | `5cc8239a` | **yes** | "1970s rain drama, close on hands driving hard chords on an electric piano under a warm lamp in a storm-lit room, lightning flash on the keys, intensity rising, shallow depth of field, film grain" | **55** (C17, 6.56s) | **3.4s** |
| **C30** | Full-band wide at the top of the build — group rising together just before release | `5cc8239a` | **yes** | "1970s rain drama, wide of the full band rising together at the peak of a storm-build, arms and instruments lifting, rain lashing the windows, dramatic blue-grey storm light, anamorphic cinematic" | **56** (C20, 6.56s) | **3.4s** |

### CH1 — +4 cuts (C31–C34), warm chorus-energy band (the §6 good template)
*All 4 are warm interior performance → **OMIT** the declined preset.*
*Anchored on `5cc8239a` + the man's selfies for any singer-facing shot.*

| clip-id | shot | still anchor | declined preset? | still prompt (draft) | slot after row | target dur |
|---|---|---|---|---|---|---|
| **C31** | Drummer HARD CU — backbeat hit, cymbal shimmer on the chorus accent | `5cc8239a` | **no** | "1970s rain drama, hard close-up of the drummer striking the backbeat, cymbal shimmer catching warm lamp light in a wood-panelled band room, decisive motion, film grain, chorus energy" | **29** (C10, 4.65s) | **3.2s** |
| **C32** | Guitar hands — fretboard + strum, driving the chorus rhythm | `5cc8239a` | **no** | "1970s rain drama, close-up of hands on an electric guitar fretboard mid-strum, warm wood-panelled band room, rhythmic chorus motion, shallow depth of field, golden lamp light, film grain" | **31** (C11, 4.65s) | **3.2s** |
| **C33** | SECOND front-singer CU, straight-to-lens — so C02 isn't carrying the chorus alone | `5cc8239a` + selfies | **no** | "1970s rain drama, straight-to-lens close-up of the male singer (short cropped red-blonde hair, receding hairline, reddish beard, NOT bald) singing the chorus with force into the mic, warm performance room, golden key light, film grain" | **33** (C02, 4.65s) | **3.2s** |
| **C34** | Keys CU — hands on the keys, warm lamp, chorus lift | `5cc8239a` | **no** | "1970s rain drama, close-up of hands on an electric piano under a warm lamp, lifting into the chorus in a wood-panelled band room, warm golden light, shallow depth of field, film grain" | **35** (C12, 4.65s) | **3.2s** |

**Placement rationale.** New cuts are interleaved between existing rows so no two
new band setups land back-to-back and so the recycled clips they break up (PRE2:
C17/C12/C02/C20; CH1: C10/C11/C02/C12) are separated. P-007 owns final ordering and
the exact re-time; the "slot after row" + target durations here are the intent it
must honour while keeping each span fixed (PRE2 41.00s / CH1 38.75s).

## 5. What downstream packets do (gates — restated)

- **P-006 (generate, GATED — credits):** generate stills C25–C34 with the §3 recipe
  (reference-anchored, on-model line), animate each with `kling3_0`/std/off/5s,
  then `video_analysis`-verify on-model **before** acceptance (free, no download).
  ~10 stills + 10 clips ≈ ~90 credits (≈9/clip, per `FOOTAGE_AUDIT.md` §8). **This
  spends credits — do not run without an explicit go.**
- **P-007 (insert + re-time edl.csv, GATED):** insert C25–C34 at the slots in §4 and
  re-balance the 12 PRE2 + 12 CH1 durations to fill the fixed spans (41.00s / 38.75s)
  exactly. Updates `data/clips.csv` / `data/stills.csv` to point at the new assets.
  **Edits product files — do not run without a confirmed packet.**

**P-005 (this packet) plans only — it generates nothing and edits no product file.**
