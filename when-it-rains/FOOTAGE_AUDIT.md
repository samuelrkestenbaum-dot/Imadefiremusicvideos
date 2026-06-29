# Footage Audit — "When It Rains" (actual clips, not the EDL)

> ## ✅ UPDATE: the failures below have been REGENERATED & verified (this session)
> All 11 flagged clips were regenerated with an on-model reference anchored
> (`5cc8239a` for the man, `1143614b` for the woman), re-animated, and **re-analyzed
> to confirm the fix**. **10 fully accepted** (C01, C06, C07, C13, C15, C16, C19,
> C22, C23, C24 — lead now has hair / inserts have no people / woman is brunette /
> C07's reflection now renders). **C04** adopted a partial (hair fixed + reflection
> kept; head-turn still absent — no regression). `data/clips.csv` now points at the
> fixed clips; originals are in `data/clips_original_backup.csv`. Details in §8 and
> `data/footage_findings.json`. The sections below document what was *found*.

**This is the "capture failures" step — done without a render.** The previous
`REVIEW.md` was *structural* (computed from the EDL + metadata) and explicitly
deferred likeness / woman-consistency / weak-clip calls to "verify-on-playback."
This audit resolves those by **actually looking at every clip's content** via
Higgsfield's server-side `video_analysis` (it ingests each clip by media ID, so
it bypasses this session's CDN egress block — no download, no render, ~16s and
**0 credits** per clip). All 26 clips were analyzed; two cross-clip consistency
panels (man, woman) ran over the results. Machine-readable version:
`data/footage_findings.json`.

**Honesty note.** `video_analysis` is an automated scene description, not a human
eye. Its "bald" reading is *consistent across 8 clips* and matches a known
generative failure mode, so trust the **pattern**. The one thing worth a 10-second
human spot-check is the **severity** on the most prominent clips (C04, C15) —
"fully bald" vs "very short hair over a receding hairline" can look similar in a
dark, rain-streaked shot. Everything else below is high-confidence.

---

## Headline

1. **The male lead is rendered as two different men, by lighting.** Warm
   wood-paneled **performance** clips are on-model (hair present). Cool-toned
   **rain / window / mirror / lightning** clips systematically render him
   **bald or shaved**. This contradicts `EDIT_MAP.md`'s claim that the on-model
   receding-hairline likeness "is used everywhere." It is not — **22 of 76 cuts
   (29%) show an off-model (bald/shaved/buzzed) lead.**
2. **Four hard content failures** — clips that don't do their job at all:
   **C07** (the woman-reflection beat never happens), **C06** (two people instead
   of an empty ocean), **C22** (an unwanted man, no atmosphere beats), **C23**
   (the final shot is missing its turn-to-camera).
3. **The woman is in better shape than feared** — she reads as one remembered
   woman across C11 / C15 / C21 (and C04's reflection). Only **C16** drifts
   (auburn, not brunette). The §4 "highest-risk bridge" panic is overstated
   because **C07 actually contains no woman at all**.

---

## 1. Male lead — likeness (the dominant problem)

Panel verdict: **not consistent · high confidence.** Skin (fair/freckled) and
beard (reddish-ginger) hold everywhere; **hair** and **age** drift.

| On-model (hair present) | Off-model (bald / shaved / buzzed) |
|---|---|
| C02, C09, C12, C17, C20 (clean anchors) · C24, EX1 (on-model but read younger) | **C01** buzz · **C04** bald · **C07** shaved · **C13** shaved/bald · **C15** bald · **C19** shaved · **C23** shaved top · **EX2** bald *(unused)* |

**Pattern:** warm performance world = correct; cool story world = bald. The
start-frame still defines the face, so the fix has to start at the **still**, not
the animation.

**Off-model exposure in the cut**, by EDL usage:

| Clip | Uses | Where | Why it matters |
|---|---|---|---|
| **C07** | 4× | V2 (the reflection verse) | shaved **and** the woman beat is missing — double failure on a narratively central clip |
| **C04** | 4× | INTRO/V1/V2 | bald, man prominent at the window |
| **C13** | 4× | PRE1/V3 | bald/shaved, man prominent |
| **C15** | 4× | V4/CH2/BRIDGE | bald (woman mirror-face is fine) |
| **C23** | 2× | **FINAL** | shaved top — the last face of the whole video |
| **C19** | 2× | CH1/CH2 | shaved, but brief lightning flashes |
| **C01** | 2× | INTRO/V1 | buzz cut, but band-wide so low visibility |
| EX2 | 0× | — | bald, but **not in the EDL** → ignore |

---

## 2. Content / motion failures (independent of hair)

| Clip | Uses | Intended | What the footage actually shows |
|---|---|---|---|
| **C06** | 1× | empty grey ocean heaving, **no people** | a **bald man at a window** then exits frame, leaving a **second distant figure** on the beach; calm water. Wrong clip entirely. |
| **C07** | 4× | woman's reflection surfaces in glass → raindrop breaks it → empty room | **the woman never appears**; only the man's own reflection. The core "memory becomes visual" beat is absent. |
| **C22** | 2× | rainwater spreads, drawer creaks, mirror glows, **no person** | a **man stands center-frame**; none of the atmosphere beats occur. |
| **C23** | 2× | turns his eyes from the window **to the camera**, unresolved | static reflective gaze; **the turn-to-camera never happens** — and this is the film's final emotional beat. |
| C04 | 4× | head-turn "as if touched" + dissolving reflection | reflection is correct; **head-turn missing** (he's static). |
| C15 | 4× | her face dissolves via condensation to his reflection | dissolve is a **digital ripple/liquid effect**, not condensation. |
| C10 | 3× | faint faceless reflection only | an extra **background pedestrian** walks through. Minor. |
| C24 | 1× | warm performance close-up | rendered in the **cool story palette** (world mismatch). Minor. |

---

## 3. Woman — consistency

Panel verdict: **reads as the same woman · medium confidence.**

- **Canonical / keep:** C11 (rain silhouette), C15 (fogged mirror-face — strongest
  identity shot), C21 (golden dissolve), and C04's reflection — all consistent
  long dark-brunette, fair skin.
- **Divergent / fix:** **C16** — hair reads **auburn / reddish-brown**, shown
  relatively clearly (yellow top, warm bathroom) before it fogs. Hair colour is
  the primary identity anchor, so this is the one that risks reading as a
  different person. Fix = regenerate to dark brunette + cooler grade, **or** just
  push more steam so the hue never reads cleanly.
- **Not a woman problem:** C07 — it has no woman at all (see §2).

Recommendation: lock a reference Element/Soul from **C15's** mirror-face and
regenerate only **C16**. Leave C11/C21/C04 alone — their fragmentation *is* the
memory effect.

---

## 4. Confirmed good (no action)

Clean and on-brief: **C02** (the 11× hero — on-model, correct motion), **C09,
C12, C17, C20** (band/rain, on-model), **EX1** (ocean gaze, on-model), and the
inserts **C03, C05, C08, C14, C18** (correct, no people). C11 / C21 (woman) good.

---

## 5. Regeneration plan (ranked by severity × exposure)

**Root cause found (the actual bug).** Inspecting the still-generation recipes
(`show_generations type:image`): **every man-still was generated with
`nano_banana_2` and ZERO reference images attached** — pure text-to-image. The
prompts even say *"THE EXACT SAME MAN as in the reference,"* but **no reference
image was ever wired in.** So the model re-invented the man from words on every
still, and under cool/dark prompts the words "short cropped red-blonde hair,
receding hairline" collapsed to *bald/shaved*. The selfies named in the handoff
were never actually used. (The warm performance stills survived only because the
lighting happened to keep hair; it was luck, not a lock.)

> **Fix: attach a reference.** `nano_banana_2` is image-to-image — it takes a
> `medias:[{role:"image", value:<job_id>}]`. Anchor every regenerated man-still to
> a confirmed on-model frame — **`5cc8239a` (C20's still)** is the best match to
> the *receding-hairline* spec — and keep the explicit *"NOT bald, NOT shaved,
> NOT buzzed; visible hair on top + receding hairline"* line. For a 25-clip
> character the more robust option is to **train a reusable Soul** from the
> selfies + best on-model frames and generate every man-still from it (perfect
> consistency, reusable for future videos) — vs. cheaper per-clip one-off refs.
> Then re-animate (`kling3_0`, the existing recipe) and **re-run `video_analysis`
> to verify on-model before accepting** — the audit loop is closed and free.
> For dark/night scenes pass `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"`
> ("IN THE DARK") so it renders literally.

- **P1 — broken content (do first):** **C07** (woman beat + bald), **C23**
  (ending motion + shaved), **C06** (wrong content), **C22** (unwanted man).
- **P2 — bald lead, story world:** **C04, C13, C15, C19**, and optionally **C01**.
- **P3 — polish:** **C16** (auburn→brunette), **C24** (warm-up the world look),
  **C10** (drop the stray pedestrian).
- **Ignore:** EX2 (bald but unused).

~11 stills + 11 clips for P1+P2+P3, well within the ~2,600 credits available.
P1 alone (4 clips) fixes the most jarring defects.

---

## 6. Also found: the cut is 2 seconds long for this mix

The EDL sums to **276.0s** but the Jun-27 mix targets **274s (4:34)**. The
assembler caps the audio at 274s, which **hard-truncates the final C23 hold ~2s
early** — the "looks to camera" ending gets clipped mid-shot. In the beat-lock
pass, trim ~2s upstream so the last shot resolves *on* the music end (~4:33.8)
instead of being cut off.

---

## 7. What this changes vs the prior `REVIEW.md`

- §4 (woman consistency) "highest-risk bridge, 4 faces" → **mostly fine**; only
  C16 drifts, and C07 has no woman.
- §5 (likeness drift) "verify-on-playback" → **confirmed and worse than feared**:
  systemic bald/shaved lead in cool clips, 22/76 cuts.
- §1 (C02 overused 11×) → still true, but **C02 itself is on-model and good**, so
  the repetition is a pacing issue, not a quality one.
- The §7 band-coverage batch is still valid, but **fixing the lead's hair
  outranks it** — thin coverage is cosmetic; a bald lead in half the film is not.

---

## 8. Regeneration — DONE (this session)

Each flagged clip was regenerated reference-anchored, re-animated, and
**re-analyzed to verify before acceptance** (the same `video_analysis` path used
to find the problems). Total spend: **106.5 credits** (~9/clip; analysis free).
`data/clips.csv` was swapped to the new clips; **originals preserved** in
`data/clips_original_backup.csv` (revert = restore that file).

| Clip | Fix | New clip job id | Verified |
|---|---|---|---|
| C01 | buzz → cropped ginger hair (band) | `c2b90eb1` | ✅ hair + band + warm |
| C04 | bald → hair; reflection kept | `297449bf` | ⚠️ hair+reflection ✅, head-turn still absent |
| C06 | 2 people → **empty ocean** | `148ef95e` | ✅ no people |
| C07 | shaved + **missing woman** → hair + **reflection renders** | `d0c0e4d4` | ✅ both |
| C13 | bald → ginger hair (canary) | `9255cfb3` | ✅ hair |
| C15 | bald → hair; condensation dissolve | `42b95398` | ✅ hair + brunette + soft dissolve |
| C16 | auburn → **dark brunette** | `c31ab9e6` | ✅ brunette, no man |
| C19 | shaved → receding red hair | `075c6af2` | ✅ hair + lightning |
| C22 | unwanted man → **empty room** beats | `f0b1f137` | ✅ no person |
| C23 | shaved + no turn → hair + **turn-to-camera** | `94e1d8b1` | ✅ both (the final shot) |
| C24 | cool palette → **warm** + hair | `e77cd5b3` | ✅ warm + hair |

**Anchor used:** `5cc8239a` (C20 still — best receding-hairline match) for the man;
`1143614b` (C11 still) for the woman. All re-animated with the existing recipe
(`kling3_0`, std, sound off, 5s; night scenes declined the "IN THE DARK" preset).

**Caveats (still verify-on-a-real-render):** verification is the automated
re-analysis, not a human eye — the proxy blocks the CDN so no clip could be
eyeballed here. Two known open items: **C04's head-turn** (optional refinement),
and the lead's exact face still varies slightly clip-to-clip (anchored, not a
trained Soul). For perfect lock, train a Soul from the selfies + best frames and
regenerate from it. **Not yet done:** beat-lock (needs the MP3 + section times),
the 2s FINAL trim (§6), band-coverage (§7), and upscale (last).
