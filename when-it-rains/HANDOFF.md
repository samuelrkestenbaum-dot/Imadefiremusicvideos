# HANDOFF — session state (2026-07-03, P-024 CLOSED)

## P-024 addendum (PRE1 delivered — read with the P-023 notes below)
- DELIVERED: pre1_v1.mp4 (19.51s) + first90.mp4 (89.79s, frame-exact grid,
  July Reverb mix bed). Final QC: SHIP, PRE1 likeness 9/10.
- Masters (user-gated): walk = W2 4aaefb8b + chain scrub -> 361af0a5; turn =
  T3 d1688201 -> LOCAL rotate90CW + chest-up crop (turn_master_crop.png,
  imported b59d18d8, ZERO nano passes on this face); trees derived from
  scrubbed walk (b6f2262e). Takes: walk-stop-breath kling 584f5e2b (10s),
  gust kling 8543a623 (5s). Sync: wan RETRY 97a9771e (8s) -> 2K c6888a50.
- NEW LAWS/LEARNINGS (P-024):
  1. AUDIO MIX SWAP: song is now the JULY REVERB mix (300s file, same clock —
     verified by envelope cross-correlation at 31.2/58.5/89.8/109.3, all 0ms
     offset; music rings to ~277s vs old 273.8). ALWAYS cross-correlate
     anchors before slicing any new mix. song.mp3 gitignored as ever.
  2. FRAME-EXACT STITCH LAW: section video streams run a few frames short of
     their audio; naive concat accumulates EARLY drift (~0.3s by 70s). All
     stitch wrappers must tpad+trim each seg to exact frame counts
     (render_p024.sh pattern: 576/456/655/468). Apply to every future stitch.
  3. WAN BEHAVIORAL PINNING: wan may invent staging that breaks lip-sync
     (turned his back to camera for 4.5s mid-line). Pin performance
     explicitly: "sings DIRECTLY INTO THE CAMERA... NEVER turns away, NEVER
     shows the back of his head" + exit choreography confined to a stated
     final window + "no hand near the lens" (first take had a warped hand
     smear at exit). Retry with pins worked first time (9/10).
  4. soul_2 chest-up+facing-camera prompts rendered ROTATED 90 degrees 4/4;
     salvage = local rotate+crop (deterministic, no face passes) beats
     rerolling. kling sound:"off" must be passed explicitly (2 takes rendered
     sound-on; harmless, segs are -an, but it may cost more).
- DIRECTORS_NOTES.md exists (six-lens review, verdict: story works, demo
  level -> label-pitch after must-fixes). NEXT PAPER PACKET before P-025:
  re-time ROADMAP to the real section clock (CH1 is 43s! FINAL is 16s! —
  verified table at the bottom of DIRECTORS_NOTES.md), write the APPARITION
  LEGIBILITY STANDARD, add the waterfront-photo plant to V3/V4.
- Credits at P-024 close: 1371.75 (packet cost ~34 vs 150-200 est).
- DELIVERY LAW: chat file sends >~50MB FAIL SILENTLY (no file_uuid in the
  receipt). Always check the uuid; for big cuts send a phone encode
  (crf 23 ~= 22MB for 90s) — the full-quality master stays in the repo.

# P-023 notes (previous close, still-valid ops reference)

Read PRODUCTION_PLAYBOOK.md (method + laws), ROADMAP.md (story ladder +
likeness lock), INTRO_SCENE_SPEC.md / V1_SCENE_SPEC.md (locked), then this.

## Where the film stands
- LOCKED: chorus_v16.mp4 (CH1 89.8-102), intro_v6.mp4 (0-24).
- DELIVERED (P-023, final frame-QC = SHIP): first70.mp4 v2 — the continuous
  0-70.3 with the enhanced mugs take, tight kitchen + awning lip-syncs
  (onset on the first beat), and the CURB ZOOM FINALE (58.6-70.3: 12s sync,
  world rushing behind him, accelerating push-in + vignette + desat ramp).
  Section cuts: v1_v2.mp4 (19.5s), v2_v2.mp4 (27.3s). Receipt:
  build-os/receipts/P-023.md.
- NEXT PACKETS (roadmap): P-024 PRE1 (70.3-89.8 darkening walk) -> V3/V4 ->
  PRE2 -> CH2 -> BRIDGE -> FINAL -> full assembly.
- Credits at close: 1405.71 (P-023 finish cost ~46 this session; roadmap
  estimate for everything remaining was 950-1100 — comfortable).

## Final asset IDs from P-023 (all QC'd, all bound-verified)
- Kitchen sync 2K: job c3cddeb8 (wan 552f47fe from imported still 08515f10 =
  scrubbed pick d52d9aeb; audio d68483dc v1_line3_tight, song 31.2+4.3s).
- Awning sync 2K: job ab86a6c8 (wan ee8d1c61 RETRY — first wan 3397e6b4 went
  static after 2.5s; retry prompt demands CONTINUOUS singing; from imported
  still 4953e937 = scrubbed pick a919b037; audio 5158896a v2_line7_tight,
  song 54.6+4.3s).
- Curb finale 2K: job 2ad7d2e3 (12s wan da598028 from imported media eac51105
  = review/curb_final.png; audio 979f0f26 v2_line8, song 58.5+11.9s).
- curb_final.png provenance: soul_2 roll 85cb2d58 (C5) -> nano pass 1
  bcf30501 (zip jacket, remove chain/ring/sign) -> nano pass 2 12d07ba3
  (zip to collar, hand glints, USER-approved 3rd-pass exception... face held
  9/10 all passes) -> LOCAL deterministic paint-out of 2 residual hand glints
  (one-sided luminance compression, 168 px, face byte-identical; script
  pattern in session scratchpad, approach documented in receipt).
- Enhanced mugs take: hf_20260703_014921_82720c7f-...mp4 (in render_v1_v2.sh).

## Ops notes (hard-won, do not relearn) — additions in P-023 marked NEW
- CI relay: push render_request.txt (line1 = script in when-it-rains/scripts/,
  line2 = "# nonce: ..." to force the path trigger) -> workflow renders/fetches
  -> commits results -> git pull. fetch_review.sh downloads review_urls.txt
  into when-it-rains/review/ (mp4s get 2fps JPEG frames).
- NEW: render-chorus.yml now checks out/pushes ${{ github.ref_name }} — the
  relay follows whatever branch triggered it. Current branch:
  claude/when-it-rains-handoff-l0u075 (supersedes ...-fetr0z, same history).
- fetch_review SKIPS existing filenames: purge review copies before re-queuing
  the same basename. Keep review/ under ~30MB (purge after every QC pass).
- MAIN-CONTEXT IMAGE READS SATURATE in long sessions: do visual QC via a
  general-purpose subagent that Reads files and returns TEXT; deliver
  user-facing media via SendUserFile.
- wan2_7: BOTH inputs imported media; roles start_image/audio_references
  EXACTLY; verify medias echo in job_display (the immediate generate_video
  response shows only "reference_images" — that is normal, check job_display).
  Frame-QC raw before 2K. NEW: wan honors breath gaps in the vocal — before
  failing a take for "mouth stops moving", check the slice's vocal-band
  energy envelope (mid-band FFT per 100ms, imageio-ffmpeg decode); closed
  mouth on an energy dip is CORRECT sync, not a defect.
- NEW HARD RULE (user, 2026-07-03): NO bare chest, ever. Any generation
  showing bare chest gets deleted immediately (repo copies purged from git
  HISTORY via commit rewrite, not just tip). soul_2 ignored "closed and
  zipped" wardrobe locks 3 rolls in a row (plus 90-degree rotations on 2) —
  do NOT reroll wardrobe fixes; salvage the best frame via nano edit instead.
  MCP cannot delete Higgsfield-library generations — the 3 bare-chest curb
  rolls (733152dc, 8c9b80ef, 85cb2d58) still exist in the account; user was
  told to delete them in the Higgsfield UI.
- NEW: tiny deterministic pixel fixes (jewelry glints etc.) are better done
  LOCALLY (numpy/PIL one-sided luminance suppression: compress only
  above-local-median luma, multiplicative per-pixel, no synthetic noise —
  synthetic per-channel noise FAILS QC as chroma confetti) than by another
  nano pass; commit the png and media_import_url the raw.githubusercontent
  URL pinned to the commit sha.
- Soul bias: gold chain in nearly every soul_2 still — zoom-check EVERY still.
- Likeness law: candidate batches -> compare vs review/ANCHOR_BOARD.png ->
  user gates picks. Max 2 nano passes on frames with his face (a 3rd needs
  explicit user go — granted once in P-023, face held; do not make it habit).
  kling recipe: duration 5|8|10, sound "off", declined_preset_id
  24bae836-2c4a-48e0-89b6-49fcc0b21612 (wan dark/rain prompts ALSO trigger
  the IN THE DARK intercept — same declined_preset_id works).
- Audio: song.mp3 (gitignored, 4:44) is NOT in this container — re-attach if
  new slices are needed. Existing slices live in audio_relay/ (committed);
  import via raw.githubusercontent URLs pinned to a commit sha. NEVER commit
  song.mp3 (public repo). imageio-ffmpeg (pip) provides the local ffmpeg.
- nano model id: catalog name is nano_banana_2 (server may echo/route
  nano_banana_flash — same thing; "nano_banana_flash" as a request id fails).

## Residue / open items
- Training photos remain in PUBLIC git history (purge offered, unanswered —
  re-raised at P-023 close).
- QC flagged (record only, LOCKED section): intro window sync ~f19-21s shows
  a thin chain + ring — predates P-023, inside user-locked intro_v6. Flag to
  user before FINAL assembly; fixing means reopening the lock.
- The 3 bare-chest curb generations still in the Higgsfield library (above).
- Archivist subagent may hit usage-credit walls; main-loop receipt fallback
  is accepted (used for P-020/P-022).
