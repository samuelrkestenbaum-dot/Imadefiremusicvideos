# EDIT MAP — "When It Rains" (4:34 / 274.0s)

> **AUTHORITY:** `data/edl.csv` is the AUTHORITATIVE live edit — **86 cuts /
> 274.0s (4:34)**, with sections at the P-003-confirmed times. **This EDIT_MAP is
> the narrative / creative reference** (the section-by-section emotional map and
> the creative rules). Where any specific timecode here conflicts with
> `edl.csv`, **`edl.csv` wins.** The per-section START times below are updated to
> the confirmed values; the per-cut sub-timings are illustrative — see
> `data/edl.csv` and `RENDER_REVIEW.md` for the exact live cut list.

Two intercut worlds: **PERFORMANCE** (warm amber band room) and **STORY** (cool
blue-grey rain memory). Target ratio ≈ 45% performance / 45% story / 10% inserts.

Every clip is a silent 5s Higgsfield render (Kling v3.0, start-frame animation).
The EDL trims pieces out of those 5s and reuses clips across sections — that's how
35 distinct clips fill 4:34 with constant cutting (86 cuts total). The
machine-readable version of the table below is `data/edl.csv` (what the assembly
script actually reads).

---

## Clip registry

`Cxx` = newly animated this session. `EXx` = clip from a prior session, reused.
Source still = the Higgsfield image job the clip was animated from.

| Key | Job ID | Source still | Section(s) | The one action |
|-----|--------|--------------|-----------|----------------|
| C01 | 5cdf4041-0f97-49d0-8711-8b726587caa2 | d2848b0e | Intro / band | Band wide; singer leans to mic, cymbal shimmers, lamp flickers |
| C02 | 229bbbc3-52d9-4886-b5fc-57161427509f | 43498158 | Verses / perf | Singer CU; lifts eyes to lens, parts lips to sing |
| C03 | 74079fe6-bb4e-44ba-aff2-21aa172c0d83 | f92d8e71 | Intro / insert | Rain runs/merges down dark glass, warm bokeh beyond |
| C04 | 79124e78-8499-4a5a-8395-b71dd73db0bf | 845dd9a1 | V1 | He turns as if touched; faint reflection forms then dissolves |
| C05 | a1e237a3-5814-4014-8f42-05f088b0f38a | ccc75620 | V1 / insert | Mist drifts over the bending river, surface shifts |
| C06 | 3d48b24c-30cc-4cb0-a028-817a26132cf5 | 29218e14 | V1 / insert | Grey ocean heaves slowly under rain |
| C07 | 8f850d70-5244-4914-ae5d-d77f0256dac1 | d45125d9 | V2 | Woman's reflection surfaces behind shoulder; raindrop breaks it; empty room |
| C08 | b36d8f7e-a070-42f1-963a-eaac7e079504 | aa6784bc | Prechorus1 | Curtains breathe inward; trees sway in the storm |
| C09 | adb501a3-dc3c-46dd-91b7-150e743e0083 | 8fd9fce9 | Prechorus / build | Band gains intensity; drummer enters, push-in |
| C10 | da567b26-5aed-4863-a1e1-b710dc30c0bd | 749d8aeb | Chorus | Puddle ripples; reflection trembles; thunder flicker |
| C11 | f057574f-dd16-44e8-ad2d-ccdfb6151d96 | 1143614b | Chorus / Bridge | Woman in rain turns away, fades into haze |
| C12 | 3bb65d56-bdeb-4897-8ce1-d7b930791440 | 9dc2c514 | Chorus | Full band release; singer opens up, cymbal hit |
| C13 | 3d829f3d-5b12-4582-8948-149d105e210d | 8e1033a4 | V3 | He turns toward the window at thunder; lightning; nothing there |
| C14 | 3a3f4f74-c141-4e84-ae23-7e5ec79c37f5 | 06808897 | V4 | Hand opens drawer; rainlight flickers on old photo |
| C15 | db20c845-d015-4eaa-a0e1-c4d2647cb2be | 76f40277 | V4 / Bridge | Woman's face forms in misted mirror; he reaches; it dissolves |
| C16 | 310513e6-473a-4497-a725-67494a5505c2 | e6d61b52 | V4 / memory | Woman's face softly forms in fogged glass, then fades |
| C17 | ad3d0086-ca15-4aa3-94f0-9b49293956c1 | 99cf778f | Prechorus2 | He lifts eyes to the storm sky, stops fighting |
| C18 | f6484ae3-c098-41e8-82dc-ac95248b6962 | e5978420 | Prechorus2 / insert | Storm clouds churn and drift |
| C19 | 3de61b10-8ebd-410a-9f9b-b88586f6f9b8 | d3db8eb8 | Chorus / Prechorus2 | Lightning splits sky behind him; rain on skin |
| C20 | e6670604-3ac6-4183-af4e-caaf11f70587 | 5cc8239a | Chorus2 / Final | Band at peak; urgent, almost angry |
| C21 | 7826073a-b52d-4740-93b2-aed813a60484 | 76054c72 | Chorus2 / Bridge | Distant memory woman half-turns, dissolves into light |
| C22 | 5365b84b-c8a3-46fe-bec7-ac783213e7a4 | 8d9620d1 | Bridge | Rainwater spreads on floor; drawer creaks open; thunder |
| C23 | 534543f1-9884-46e5-b749-1739661db4c0 | 12a29611 | Final | Alone by window; turns eyes to camera, unresolved |
| C24 | d797ba35-3d41-430f-8e8f-e325efe09bdf | 8de0efa8 | Final | Near-still CU; quiet haunted gaze, slow blink |
| EX1 | a303faab-5926-4f89-a269-584f26f9eb4c | (prior) | V1 / ocean | Man gazes at grey rain-swept ocean through glass |
| EX2 | c1cb27a8-fd89-470a-bbeb-1feb29a80605 | (prior) | Prechorus2 / V3 | Man in rain looks up; lightning flashes on his face **[NOT USED in the live cut]** |

### Band-coverage clips (P-007) — C25–C34

Added to break the C02/C10/C09/C12/C20 recycling and give PRE2 + CH1 their own
band pacing (see `BAND_COVERAGE_PLAN.md`). C25–C30 = the PRE2 storm-build band;
C31–C34 = the CH1 chorus-energy band. All are band-performance world only.

| Key | Section | The one action |
|-----|---------|----------------|
| C25 | PRE2 / band | Drummer's hands & sticks accelerate a tom fill on the storm build |
| C26 | PRE2 / band | Slow dolly push-in toward the full band leaning into the build |
| C27 | PRE2 / band | Singer in profile lifts his chin into a rising vocal |
| C28 | PRE2 / band | Backlit bassist drives the strings, slow forward sway |
| C29 | PRE2 / band | Hands drive hard chords on the keys as the build climbs |
| C30 | PRE2 / band | Full-band wide rises together at the peak of the build |
| C31 | CH1 / band | Drummer hard CU strikes the backbeat, cymbal shimmer |
| C32 | CH1 / band | Guitar hands strum / move along the fretboard, chorus rhythm |
| C33 | CH1 / band | Second front-singer CU sings the chorus with force into the mic |
| C34 | CH1 / band | Keys CU — hands lift into the chorus under a warm lamp |

**The live cut (`data/edl.csv`) uses 35 distinct clips** (C01–C34 + EX1). There
are **36 clips in `data/clips.csv`** — **EX2 is unused** in the live edit.

---

## The edit, section by section

Times are `M:SS`. Each line is one cut: **clip — duration — what it does.**

### 0:00 · INTRO — rain establishes the spell
*(confirmed section starts: INTRO 0:00 → V1 0:18. Per-cut sub-timings below are illustrative; `data/edl.csv` is authoritative.)*
Slow, two worlds introduced.
- 0:00 · C03 · 4s · rain on the window, black-to-image
- 0:04 · C01 · 4s · band room wakes, lamps, singer steps to mic
- 0:08 · C02 · 3s · singer close-up
- 0:11 · C04 · 4s · the man alone by the window
- 0:15 · C03 · 3s · rain, hold into the verse

### 0:18 · V1 — "When it rains I think I feel you…"
He feels her before he sees her.
- 0:18 · C02 · 4s · sings the opening line
- 0:22 · C04 · 5s · **turns as if touched; reflection almost forms, dissolves**
- 0:27 · C01 · 3s · restrained band
- 0:30 · C06 · 4s · grey ocean
- 0:34 · EX1 · 4s · he gazes at the ocean through glass
- 0:38 · C05 · 4s · river bend
- 0:42 · C02 · 3s · singer
- 0:45 · C04 · 3s · back to the window

### 0:41.25 · V2 — "I still look for you beyond my shoulder…"
The memory becomes visual; he searches.
- 0:48 · C07 · 5s · **over the shoulder; her reflection surfaces in the glass**
- 0:53 · C02 · 3s · face-on singing
- 0:56 · C03 · 3s · rain behind him
- 0:59 · C07 · 4s · **a raindrop breaks the reflection; he turns to an empty room**
- 1:03 · C09 · 3s · band fragments
- 1:06 · C02 · 3s · singer, more direct
- 1:09 · C04 · 4s · window
- 1:13 · C07 · 5s · reflection again, gone

### 1:09.75 · PRECHORUS 1 — "And I don't know if you still feel it…"
The world moves like she's still there.
- 1:18 · C08 · 5s · **curtains breathe; trees move outside**
- 1:23 · C13 · 4s · he almost turns toward a sound
- 1:27 · C09 · 4s · drummer enters, band builds
- 1:31 · C02 · 3s · "it's like you never left"
- 1:34 · C08 · 4s · trees move
- 1:38 · C09 · 5s · slow push-in, intensity rising

### 1:29.25 · CHORUS 1 — "When it rains you're in the water…"
First true release. Water everywhere.
- 1:43 · C12 · 4s · band release
- 1:47 · C10 · 3s · **puddle; reflection trembles**
- 1:50 · C19 · 3s · thunder flash
- 1:53 · C11 · 3s · woman from behind, gone
- 1:56 · C12 · 3s · band
- 1:59 · C02 · 3s · chorus with force
- 2:02 · C10 · 3s · water again
- 2:05 · C12 · 3s · band

### 2:08 · V3 — "When it rains, I think I hear you…"
The memory becomes auditory.
- 2:08 · C13 · 5s · **turns toward the window at thunder**
- 2:13 · C18 · 3s · storm clouds
- 2:16 · C09 · 3s · band, warmer, urgent
- 2:19 · C13 · 4s · turns, nothing
- 2:23 · C11 · 3s · distant woman, one shot
- 2:26 · C02 · 4s · singer, less controlled
- 2:30 · C12 · 4s · drummer harder
- 2:34 · C13 · 5s · listening, haunted

### 2:24.5 · V4 — "Tried to hide your face in every mirror…"
He tries to put it away and fails.
- 2:39 · C14 · 5s · **opens the drawer, hides the memory**
- 2:44 · C15 · 5s · **her face in the misted mirror**
- 2:49 · C02 · 3s · CU; band being swallowed by story
- 2:52 · C16 · 4s · face forms in the fog
- 2:56 · C15 · 4s · he reaches; it dissolves to his reflection
- 3:00 · C14 · 4s · drawer closes
- 3:04 · C09 · 5s · shadowy band

### 2:53 · PRECHORUS 2 — "And I keep trying to forget…"
The sky itself contains her; he stops resisting.
- 3:09 · C17 · 5s · **looks up into the storm sky**
- 3:14 · C18 · 4s · clouds move
- 3:18 · C12 · 4s · the band carries the confession
- 3:22 · C02 · 4s · "I still want you / but I just don't know why"
- 3:26 · C17 · 4s · he stops fighting it
- 3:30 · C20 · 4s · band rises

### 3:34 · CHORUS 2 — bigger; worlds start colliding (faster cuts)
- 3:34 · C20 · 3s · band
- 3:37 · C10 · 2.5s · water
- 3:39.5 · C19 · 2.5s · thunder
- 3:42 · C15 · 3s · mirror
- 3:45 · C07 · 3s · window reflection
- 3:48 · C21 · 3s · clean memory shot, she turns away
- 3:51 · C20 · 3s · band
- 3:54 · C02 · 4s · almost angry at himself

### 3:58 · BRIDGE — "Every drop knows where you landed…"
The emotional flood. Most visually active.
- 3:58 · C22 · 5s · **rainwater spreads across the floor**
- 4:03 · C16 · 3s · mirror fogs
- 4:06 · C11 · 3s · she turns away
- 4:09 · C20 · 3s · band at peak
- 4:12 · C22 · 3s · drawer creaks open
- 4:15 · C21 · 3s · she vanishes
- 4:18 · C15 · 3s · he reaches for the mirror

### 4:21 · FINAL — "And I still wonder"
No resolution. End on him, not her.
- 4:21 · C20 · 3s · final chorus, band plays out
- 4:24 · C24 · 3s · singer, direct, almost still
- 4:27 · C23 · 4s · **alone by the window**
- 4:31 · C03 · 2s · rain continues
- 4:33 · C23 · 3s · **he looks to camera — unresolved.** End.

**Total: 274.0s (4:34)** — authoritative count in `data/edl.csv` (86 cuts). The
per-cut sub-timings above are the illustrative narrative map; `edl.csv` is the
live edit.

---

## Notes for the finishing pass

- **Hero clips to upscale (2K/4K)** before final delivery — the ones held longest
  and most "lead": C02, C04, C07, C12/C20 (band), C15, C17, C23. Use Higgsfield
  `upscale_video`. Leave inserts at standard res.
- **Woman consistency:** her memory shots (C11, C16, C21, C15) were generated
  across separate prompts, so her exact face varies slightly. Because she is
  always distant / fogged / turning away, this reads as "fading memory" rather
  than continuity error — but if you want her locked, train a Soul or save her as
  a reference Element from the single best frame and regenerate the others from it.
- **Off-model stills NOT used:** earlier "buzzed/near-bald" versions
  (22e02845, b0f3fd47, 26443c5f, ff3797c3) were excluded — the on-model
  receding-hairline likeness is used everywhere instead.
- **Crossfades:** the EDL hard-cuts. For the dreamier transitions (reflections
  forming, mirror dissolves) a 6–10 frame dissolve in your NLE sells the memory
  better than a hard cut. Hard-cut the band; dissolve the memory.
