# HANDOFF — session state (2026-07-03, mid P-023)

Read PRODUCTION_PLAYBOOK.md (method + laws), ROADMAP.md (story ladder +
likeness lock), INTRO_SCENE_SPEC.md / V1_SCENE_SPEC.md (locked), then this.

## Where the film stands
- LOCKED: chorus_v16.mp4 (CH1 89.8-102), intro_v6.mp4 (0-24), v1_v2.mp4 /
  v2_v2.mp4 (delivered in first70.mp4, now under P-023 revision).
- IN FLIGHT — P-023 (user notes on first70): mug take grain, lip-sync timing,
  AI-look on sung shots, curb finale redesign. Details below.
- NEXT PACKETS (roadmap): P-024 PRE1 (70.3-89.8 darkening walk) -> V3/V4 ->
  PRE2 -> CH2 -> BRIDGE -> FINAL -> full assembly. Credits est. ~950-1100 left.

## P-023 remaining pipeline (exact)
1. QC these 5 stills (SUBAGENT vision only — see Ops notes):
   - kitchen pick K3 scrubbed: job d52d9aeb (chain+ring removed) — verify.
   - awning pick A3 scrubbed: job a919b037 (chain+corner text) — verify.
   - curb REROLLS (chest MUST be covered; old C1/C2 disqualified for open
     jacket/bare chest + 90-degree rotation): 733152dc / 8c9b80ef / 85cb2d58 —
     pick best vs review/ANCHOR_BOARD.png; user gates the curb pick (file).
2. media_import_url the 3 final stills (wan needs IMPORTED ids).
3. wan2_7 (roles EXACTLY start_image + audio_references):
   - kitchen: audio media d68483dc (v1_line3_tight = song 31.2+4.3s), dur 5
   - awning:  audio media 5158896a (v2_line7_tight = song 54.6+4.3s), dur 5
   - curb:    audio media 979f0f26 (v2_line8 = song 58.5+11.9s), dur 12,
     prompt includes world rushing in fast motion behind him.
   (Superseded wan outputs from the AI-look stills: b5754247/c3fb9eca/87d14424
   — do not reuse.)
4. Subagent frame-QC raw wans (mouth onset <=0.3s, likeness, chest covered),
   then bytedance 2K aigc upscales (source 1344x768, fps 24).
5. Recut scripts (grain finish already in their VF):
   - render_v1_v2.sh: mugs.mp4 -> ENHANCED take
     hf_20260703_014921_82720c7f-c1e5-4e93-811e-f18a25dfb81c.mp4 (in-points
     unchanged); sync.mp4 -> new kitchen 2K; sync seg in-point becomes 0.10
     (slice starts 31.2; seg at song 31.3).
   - render_v2_v2.sh: sync.mp4 -> new awning 2K, seg in 0.10 (slice 54.6, seg
     at 54.7); the 50.8-54.7 slot becomes the GHOST puddle (31ccf929, in 0.40
     — figure visible then rippled apart); 58.6-70.3 becomes the CURB ZOOM
     SYNC: new 12s curb 2K at in 0.10 with ACCELERATING push-in + faded
     background, e.g. filter: zoompan=z='1+1.1*pow(in/281,2)':d=1:
     x='iw/2-(iw/zoom/2)':y='ih/3-(ih/zoom/3)':s=1280x720 plus
     vignette and a slow hue=s desaturation ramp. Lip sync law: seg in-point
     = song_time_at_slot_start - slice_start.
   - render_p022.sh (wrapper): point at the new cuts, restitch first70
     (intro gets grain via VFG; sections pass plain), deliver first70 + close
     P-023 receipt (main-loop fallback OK).

## Ops notes (hard-won, do not relearn)
- CI relay: push render_request.txt (line1 = script in when-it-rains/scripts/,
  line2 = "# nonce: ..." to force the path trigger) -> workflow renders/fetches
  -> commits results -> git pull. fetch_review.sh downloads review_urls.txt
  into when-it-rains/review/ (mp4s get 2fps JPEG frames).
- fetch_review SKIPS existing filenames: purge review copies before re-queuing
  the same basename.
- MAIN-CONTEXT IMAGE READS SATURATE in long sessions ("Request is too
  large"): do visual QC via a general-purpose subagent that Reads files and
  returns TEXT; deliver anything user-facing via SendUserFile. Keep review
  artifacts small (JPEG, purge often; review/ kept under ~30MB).
- wan2_7: BOTH inputs imported media; roles start_image/audio_references
  EXACTLY (generic roles silently unbind -> invents a different person);
  verify medias echo in the job result; frame-QC raw before 2K.
- Soul bias: a gold chain necklace appears in nearly every soul_2 still
  (learned from training photos) — zoom-check EVERY still; nano one-pass
  removal is proven. Never say "open" in wardrobe prompts (renders bare
  chest); say "jacket closed/zipped, chest completely covered".
- Likeness law: candidate batches (count 3-4) -> compare vs
  review/ANCHOR_BOARD.png -> user gates picks. Max 2 nano passes on frames
  with his face. kling recipe: duration 5|8|10, sound "off",
  declined_preset_id 24bae836-2c4a-48e0-89b6-49fcc0b21612.
- Audio: song.mp3 (gitignored, 4:44) lives in when-it-rains/ locally; slice
  with the imageio-ffmpeg static binary (pip install imageio-ffmpeg); commit
  slices to audio_relay/ and import via raw.githubusercontent URLs pinned to
  a commit sha. NEVER commit song.mp3 (public repo).
- Residue: training photos remain in PUBLIC git history (purge offered,
  unanswered); archivist subagent may hit usage-credit walls (main-loop
  receipt fallback used for P-020/P-022); rain-blurred red storefront in the
  intro sync bg is user-accepted.
