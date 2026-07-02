# PRODUCTION PLAYBOOK — the locked canonical style ("the chorus method")

The chorus (render_chorus_v16.sh) is the LOCKED reference cut. This doc is the
copy-paste bible for building every other section: same method, different scenes.

## 1. Locked identities & assets (use these IDs verbatim)
- **HIS trained Soul** (all solo shots of him): soul_id `07822e21-af62-44cc-a8b8-0b27dfe6de8a` (model `soul_2`)
- **Elements** (any frame needing him+her or two likenesses): `wir-him` = `1b581c11-e515-4d88-bb2c-b2b0af3b722d`, `wir-her` = `38ebfd81-9ddb-4b11-b055-b95307d2d5ce` — embed as `<<<uuid>>>` in prompts (nano_banana_2 / kling3_0 support them)
- **HER anchor still**: job `65382e29-3719-4991-9fb6-d1cfd1e98242`
- **HERO clip** (the approved front lip-sync): `hf_20260701_165718_491e39d1-...mp4`
- **Cafe one-take**: `hf_20260701_211804_c1ffc156-...mp4`; **couplet vocal** media `86591b6a-2e79-4ff6-bd65-f11fcf564030`
- **Beat grid**: `analysis/beats.json` (61.5 BPM); line map: `analysis/line_map.json`

## 2. Character bible (in EVERY prompt with a person)
- **HIM**: short buzzed hair, FULL hairline (never "receding"/bald), reddish stubble,
  fit lean build, **bare hands — NO ring, NO jewelry** (single, post-breakup).
  Restrained natural delivery — never screaming. Wardrobe per scene spec.
- **HER (the ex)**: pale skin, long dark wavy hair, late 20s, delicate melancholic.
  Appears OBLIQUELY ONLY — reflections, glass, water, edge of frame. Never literal.
- Always append: "Absolutely NO text, NO signage, NO letters anywhere."

## 3. The method — per scene, in order
0. **DERIVE, DON'T DESCRIBE** (law, learned from intro v4): every asset inside
   a scene derives from that scene's approved MASTER frame — nano reframe /
   removal with the master as source media — NEVER a fresh text prompt. A
   fresh prompt invents its own room, weather, and sheets. Proven chains:
   remove-person, tight-reframe-on-detail, window close-up from room master.
0b. **SANDBOX EYES — QC every asset BEFORE the next spend and BEFORE the user
   sees it** (the review loop): asset URL -> `review_urls.txt`; set
   `render_request.txt` line 1 = `fetch_review.sh` (+ `# nonce:` line 2 to
   force the push trigger); push; CI fetches into `when-it-rains/review/`
   (videos also get 2fps frame PNGs); `git pull` and Read the images. Check:
   same room/light/props as master, bible (hairline, NO ring, NO text),
   locked camera, choreography timing — cut points are MEASURED from the
   timestamped frames (this supersedes video_analysis for timing). The
   finished cut gets the same pass via its raw.githubusercontent URL before
   delivery.
1. **SPEC FIRST, on paper** (template: `CAFE_SCENE_SPEC.md`): locked room geometry,
   blocking that motivates every camera position, reflection physics, and the
   **body-state law**: his body exists in ONE take only — inserts contain no part
   of him, so posture/hands can never mismatch.
2. **Master still** (soul_2 + bible + scene spec). User eyeballs likeness BEFORE
   any animation. The master defines wardrobe/light/geometry for the scene.
3. **ONE continuous take** per setup: kling3_0, duration 10, sound off,
   declined_preset_id `24bae836-2c4a-48e0-89b6-49fcc0b21612`, choreographed
   FIRST/THEN action prompt. The editor cuts away and back INTO THE SAME TAKE —
   continuity by construction.
4. **Measured cuts**: media_import_url the take → video_analysis → beat timestamps
   → exact in-points. Never eyeball.
5. **Inserts**: POV grammar ("the camera IS his eyes..."); for two-likeness frames
   use the elements; for reflections, mirror the ENVIRONMENT (window/lights/room)
   with her inside it — a lone floating figure never reads as a reflection.
6. **Surgical edits** (nano_banana_2, source still as the only media): "Edit this
   exact image with ONE change only: ... Keep absolutely everything else identical."
   Proven for: ring removal, text removal, removing a figure (empty plates).
7. **True composites** (when translucency must be REAL): empty-plate still + ffmpeg
   overlay of the subject clip at `GHOST_OPACITY` (0.40 ghostly – 0.65 present).
   Both layers get `setpts=PTS-STARTPTS` so nothing pops in late.
8. **Lip-sync** (front-facing performance only): wan2_7 with BOTH inputs as
   IMPORTED MEDIA (media_import_url the still png AND the vocal — job ids fail).
   Vocal relay: slice from song.mp3 → commit to `audio_relay/` → push →
   `https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>` → media_import_url.
   In the cut, a lip-sync clip's in_point MUST equal its output-timeline position.
9. **Cut rules**: cut on beats (beats.json); hero holds on the hooks; story beats
   chain notice → reveal → reaction; ONE continuous audio track under all cuts.
10. **Deliver**: commit render script → trigger `.github/workflows/render-chorus.yml`
    (input `script=<name>.sh`) → CI renders with full egress and commits the mp4 →
    `git pull` → send the file into chat.

## 4. Aesthetic (three worlds, one grammar)
- **Performance**: bleach-bypass desaturated steel-blue, silver backlit rain,
  wet black tee, restrained. 2.35:1, film grain.
- **Normal life**: naturalistic, warm tungsten interior vs cool rainy windows.
- **Memory** (if used): warm bloomy overexposed Super-8.

## 5. The locked chorus (reference cut — copy this shape)
`render_chorus_v16.sh`: HERO held (hook) → her oblique (puddle) → HERO return →
story beat 1 (take: notice) → REVEAL (composited reflection) → story beat 2
(same take: turn — no one). 12s, continuous vocal, every cut on the grid.

## 6. The locked intro (second reference cut — the derivation showcase)
`render_intro_v6.sh` (user: "Amazing"): bedroom's own rain-streaked window
(derived close-up) → bed take beat 1 (double bed, lying awake, head turn
measured 6.5-7.5) → HER-half insert (tight close, the pillow no one slept on,
derived) → same take: the rise → V1 window + lip-synced first line (2K
finish) → maybe-her ghost after the line. 24s. Bedroom canon: DOUBLE bed,
charcoal bedding; all bedroom assets derive from master `2d080b77`. Full IDs
in INTRO_SCENE_SPEC.md.
