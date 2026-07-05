# HANDOFF — session state (2026-07-03, QUALITY PASS delivered)

> CANONICAL LIKENESS = BALD/SHAVED + LIGHT GINGER STUBBLE (2026-07-05, user-validated
> from snapshots): the user confirmed the ORIGINAL MIC (bald+beard), the AWNING (0:58,
> IMG_2938), and the CAFE (1:39) all "look like me"; he REJECTED the curb's fuller-beard-
> +-buzzed-hair look and my ginger-HAIR refit. So his true look is bald/shaved head, LIGHT
> thin ginger stubble, freckled — NOT the fuller-hair wir-him element. Use the AWNING frame
> (awn_02, ab86a6c8) as the likeness reference for any future face fix, NOT wir-him.
> CURB REGEN (delivered): curb face was refit to the awning look — nano_banana with
> [curb_00 base ae8bd038 + awn_02 ref f2fa436c] -> refit still 2a836342 (imported c303a963)
> -> wan lip-sync to curb_vocal.mp3 (song 58.5+, imported 56ff79be) = new curb 8237e4ae
> (NATIVE 1080p, so sharp + gentle 1.10x zoom = no waxy degrade). render_v2_v2 curbsync
> now = 8237e4ae. Old curbsync 17d2a03f (Topaz-716) RETIRED.
> REFLECTION (delivered): cafe glass reveal reworked from opaque overlay (0.55) to a faint
> softened overlay; user said "split the difference" -> REFL_OP=0.42 + gblur=3 in
> render_chorus_v18.sh seg4 (screen-blend attempt FAILED = magenta wash, reverted). chorus_v18
> = v16 (ORIGINAL mic) + reflection fix; full102 uses chorus_v18.
> OPEN: the "like you never left" street CU (pre1 turnsync d07ecfa1) still has hair+beard;
> user approved it earlier but flagged it might want the same bald refit — OFFERED, awaiting.
> CURRENT DELIVERY: full102.mp4 (13.2MB, 101.88s), full-timeline verified.

> MIC REVERTED + CURB DE-ZOOMED (2026-07-05, from user snapshots IMG_2933/34/35).
> LIKENESS LAW (important): the user is the ONLY ground truth on his own face. He said
> the ORIGINAL chorus mic (bald/shaved + darker beard, hero 491e39d1) "looked exactly
> like me" — my ginger element-refit (chorus_v17, wir-him 1b581c11) was WRONG and is
> REVERTED. full102 uses chorus_v16 (original mic) again. DO NOT refit the mic. Do NOT
> assume the ginger wir-him element = his true look; he validates the bald/beard mic.
> The review's "off-model mic" call was a MISTAKE to act on (only the user can judge likeness).
> CURB (1:00-1:10): user confirmed it "degrades as it zooms in" (waxy/plastic at ~1:09).
> Root cause = 716p source magnified by the push-in. FIX (no regen — avoid another wrong
> face): reduced curb zoom 1.65x -> 1.10x and dropped the 4K intermediate to 1080
> (render_v2_v2.sh seg_03/seg_05 z='1+0.10*pow(...)'), so the face holds the sharp wide
> framing and never enlarges into plastic. Curb likeness UNCHANGED (kept ginger-buzzed).
> render_full102 rebuilds intro+v2 (v2 fast now, no 4K), reuses committed pre1+chorus_v16.
> OPEN (offered): if "not canonical" curb meant a likeness change (e.g. match the bald
> mic look), that's a separate regeneration the user must green-light. chorus_v17 +
> refit assets (02659799/a05621d2/8f3bd7ea) stay in repo but are UNUSED.

> TWO BUGS FIXED (2026-07-05, after user "all messed up, no changing in scenes"):
> (1) INTRO ZOOMPAN BALLOON: the cold-open push-in (render_intro_v6.sh seg0 PUSHWIN
>     zoompan) ballooned intro_v6.mp4 to 51 MINUTES (zoompan is a stills/Ken-Burns
>     filter; on video with d=1 it multiplied frames). full102 took the first 24s =
>     one frozen window, and the bed/wake/sing beats were trimmed off. FIX: reverted
>     seg0 to plain VF. LAW: never zoompan a video clip for a push; use a time-based
>     crop (crop=w='iw/(1+k*min(t,T)/T)':...) which is frame-count-safe. This bug was
>     ALSO latent in "recut pass v1" (only 0-7s was QC'd) — ALWAYS map the FULL
>     timeline of a delivery (fps=1/2 tile), not just sampled regions.
> (2) MASTER >100MB PUSH REJECT: full102_master.mp4 hit 100.16MB > GitHub's 100MB
>     hard limit -> CI push rejected (render succeeded, push failed). FIX: render_full102
>     now `rm -f full102_master.mp4` after deriving the delivery + QC frames; only the
>     720p delivery (full102.mp4 ~13MB) + review frames are committed. git-rm'd the old
>     tracked master. QC locally from the committed 720p delivery, not the master.
> Also: render_full102 no longer rebuilds v2_v2/pre1 (reuses committed correct copies) —
> saves the slow double-4K curb re-render; only intro is rebuilt.
> CURRENT GOOD DELIVERY: full102.mp4 (13.5MB, 101.88s) — fixed intro + canonical mic +
> curb cutaway + street transition, full-timeline verified.

> MIC FACE FIX DELIVERED (2026-07-05) — the #1 likeness miss (chorus mic, was bald/dark-beard
> off-model) is now CANONICAL ginger. Chain: probe hero frame (491e39d1 -> hero_02) ->
> nano element-refit with wir-him 1b581c11 (2 cands, picked 02659799 = full ginger hairline)
> -> imported a05621d2 -> wan2_7 lip-sync to chorus_couplet.mp3 (a2393356) = mic hero
> 8f3bd7ea (1080p, 8s, faces mic, no turn) -> render_chorus_v17.sh (v16 with hero.mp4 swapped)
> = chorus_v17.mp4 -> render_full102.sh now uses chorus_v17. QC: canonical ginger across all
> frames, montage intact. Delivered full102.mp4 (12.7MB) + master (101.87s). Sync unchanged.
> REMAINING face items (deferred, lower pri): curb sev4 + awning sev3 skin refits (same
> refit->wan chain), cafe sev2 bald/soft (incidental profile — re-upscale + optional hair refit).
> NOTE: render_full102 rebuilds intro+v2+pre1 each run (~10-12min CI due to the curb's DOUBLE
> 4K zoompan since the recut split); chorus_v17 is committed so it's not rebuilt.

> DIRECTOR/FACE REVIEW + RECUT PASS v1 (2026-07-04). Ran an 8-agent review (editor/
> mv-director/story/dp lenses + 2 face-QC + synthesis) over 2fps sheets of full102.
> VERDICT: flow = MIXED (flat front half, strong finish). Dead spots: curb 58.6-70.3
> (11.7s single hold) was the real one; intro window is ~6s (review over-stated it as
> 13s — always ground-truth durations from the section scripts, contact-sheet cells of a
> static shot inflate perceived seconds). FACE MISSES ranked: (1) MIC 1:31-1:36 sev5 =
> the ONE true identity break (bald crown + heavy DARK beard + harder jaw = reads as a
> different man, on the chorus money shot; original hero 491e39d1, never refit to
> canonical); (2) CURB sev4 waxy/plasticky at push-in, stubble drifts dark; (3) AWNING
> 0:56 sev3 older non-refit; (4) CAFE sev2 soft/720; (5) STREET sev2 soft-but-on-model.
> Identity nuance: intro/V1/cafe "bald" reads are mostly the ginger crop vanishing at
> distance/low-light (0:20 window CU confirms crop intact) — NOT true breaks; only MIC is.
> Skin tone + brown eyes consistent, no eye drift. Full report: workflow wf_40d8e17b-068.
> RECUT PASS v1 DELIVERED (flow, no regen): intro cold-open push-in (render_intro_v6.sh
> seg0 PUSHWIN zoompan) + curb split by a 1.3s ghostpud apparition flash with zoom/hue
> continuing across the cut (render_v2_v2.sh seg_03/04/05; piece2 offsets in+161, t+6.70).
> render_full102.sh now rebuilds intro+v2+pre1. Duration unchanged 101.87s.
> STILL PENDING (user-deferred tracks): (A) deeper V1 kitchen trim; (B) FACE-FIX pass —
> refit/regen MIC to canonical ginger FIRST, then curb/awning refits, cafe/street
> re-upscale; (C) motif seeding (her face in early reflections) + two-mugs insert.

> FULL ~102s CUT DELIVERED (2026-07-04) — full102.mp4 (720/13.7MB) + full102_master.mp4
> (1080/101.87s). Built by scripts/render_full102.sh. Folds BOTH approved fixes:
> (1) 4K curb-zoom (render_v2_v2.sh, 17d2a03f 4K + zoom-within-4K, no head-crop — VERIFIED);
> (2) street->chorus transition (flow_demo3, APPROVED "good enough"). PRE1 turnsync now =
> no-turn street 84b73e44 Topaz'd to 1080 (d07ecfa1) — replaces old exit-turn e15b36e1.
> Grid = 576/456/655/468 + storm 37f (trees 3d0619c6 in 2.80) + chorus_v16 from in 1.50
> (frame 7) 252f. Bed = audio_relay/first102.mp3 (song 0-102). OPEN: chorus tail
> (cafe/mic 89.8-101.8) is 720-native upscaled to 1080 = soft; offered dedicated upscale
> pass if user flags it. flow_demo2 (extended-street, hair change) = DEAD, do not use.
>
> STREET->CHORUS TRANSITION rework (2026-07-04) — flow_demo3.mp4 APPROVED ("good enough").
> User intent (final, after 2 misreads): keep chorus_v16's montage in its ORIGINAL
> order (mic->puddle->mic->cafe); ONLY trim the dead FRONT of the mic clip and drop a
> connective beat in front of it. DO NOT regenerate the street take — a fresh wan gen
> (1cfafdb2, the "extended street sings the hook" idea) CHANGED HIS HAIR and was
> rejected. flow_demo2.mp4 (extended-street + puddle-first) = REJECTED/superseded.
> CORRECT build = scripts/render_flow_demo3.sh:
>   seg0 original street take 84b73e44 (8.0s src) "like you never left" 82.02-89.82
>   seg1 storm insert trees 3d0619c6, in 2.80 t 1.50 -> covers 89.82-91.32
>   seg2 chorus_v16 from in 1.50 (== FRAME 7 @ 4fps sheet == native song 91.32, so
>        mic lip-sync stays perfect) to end -> mic->puddle->mic->cafe intact
>   bed audio_relay/flow_demo_bed.mp3 (song 82.02 +20s) continuous -> all synced.
> KEY LAW: trimming the front of a lip-synced clip only stays in-sync if you place it
> at its NATIVE song position and fill the freed gap with an insert (don't slide the
> synced clip under different audio). Assets probed live: street src=8.0s (can't
> stretch), trees=outdoor storm (good connective), rain 41b05e2e=indoor window (mismatch).
> IF APPROVED: fold seg pattern into the full first90 re-render alongside the staged
> 4K curb-zoom fix (render_v2_v2.sh, task #19).

> LIP-SYNC MODEL (2026-07-04): user A/B'd wan2_7 vs seedance_2_0 on the turn (same face db667b65 + vocal) — WAN WON, seedance worse. wan2_7 is the lip-sync model; sync is approximate (AI mouth-from-still, tech ceiling) and the user accepts it. Do NOT re-sync with seedance. Higgsfield has no dedicated phoneme-accurate lip-sync engine (models_explore: seedance/kling/wan/grok all general).

## QUALITY PASS addendum (first90 resolution + face consistency) — read first
User feedback on the P-024/P-025 first90: shots looked "extremely like AI /
degraded, not realistic". Root cause found: the whole render pipeline was
1280x720 and the cut DOWNSCALED even the high-res takes. Two-part fix delivered:
- RESOLUTION: all render scripts converted to 1920x1080 (scale/pad, PUNCH crop,
  curb zoompan s=). Findings: the 4 sync takes + mugs were natively 1440p (the
  bytedance "2K" really was ~1440p, but earlier I misread its echo as 720p);
  the 6 kling takes (walk/door/rain/ghostwin/ghostpud/trees) were真 ~716p.
  TOPAZ-upscaled the 716p kling takes to 1080p (topaz "prob-4", real detail,
  beats bytedance); kept 1440p sources native (downscale in render). Delivered
  1080p first90 (89.79s) — "degraded body" fixed.
- FACE CONSISTENCY: element-refit the AI-looking sync faces with wir-him
  (<<<1b581c11...>>>) then re-sync. User gated: KITCHEN refit b4afd0c6 ->
  wan 68b54a2a -> topaz1080 a608a76d (swapped into render_v1_v2 sync.mp4);
  CURB needed a TIGHTER re-refit (1st round widened pose/added people; 2nd
  round ac4c68dc held it) -> wan 55a4ddff -> topaz1080 a3b89b9b (render_v2_v2
  curbsync.mp4). AWNING kept at 1080p per user (older face, not refit — the
  one remaining non-canonical face; offer to refit if user notices). walk+turn
  already canonical from P-025.
- NEW LAWS: (1) render at 1080p, never downscale high-res takes to 720p;
  (2) Topaz (not bytedance) for real detail on <1080p takes; (3) nano
  element-refit REIMAGINES composition ~half the time (pose/framing/adds
  people) — lock pose explicitly ("arms straight down at sides, do NOT widen/
  reframe, NO other people") and expect a reroll; (4) chat delivery: 37MB
  the real silent-fail threshold is ~25MB (22MB delivered fine w/ file_uuid;
  35-37MB came back with NO file_uuid = failed). DELIVER SMALL: 720p crf26
  faststart = ~12MB for 90s, opens reliably. ALWAYS -movflags +faststart
  (moov at front, else phones can't start playback) and check the SendUserFile
  result prints "-> file_uuid:" (no uuid line = it did NOT deliver).
- Credits: 1371.75, unchanged across the whole pass — the user's "enhanced"
  Higgsfield account is absorbing generation cost (flagged; verify in UI).

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

## P-025 addendum (PRE1 realism repair — CLOSED)
- User rejected P-024 PRE1 faces as AI-looking. Repair: nano ELEMENT-REFIT of
  the two masters with wir-him (1b581c11) embedded <<<uuid>>> — element BOUND
  (verify reference_elements in job echo). Realism: turn 4.5->9/10 at
  delivery res, walk 5->8/10. User gated WC(+chain paint-out)/TA.
- Final assets: walk take kling d035bb3b (from walk_final.png = WC d19e7262
  + local chain paint-out; imported d6142bc8; slots A in 0.00 / B in 5.50);
  turn sync wan 7db11194 (from TA 557974ad imported c7a5e1c1; behavioral-pin
  prompt reused, passed first try) -> 2K e15b36e1. Delivered repaired
  pre1_v1.mp4 + first90.mp4 (89.79), final QC SHIP, phone encode uuid-checked.
- LEARNINGS: (1) element-refit is THE fix for AI-look faces — same scene,
  face pulled to canonical; expect ~1/6 refits to add a chain and ~1/3 to
  drift EYE COLOR (check brown eyes explicitly in QC). (2) chain paint-out
  on DARK chains: one-sided luminance LIFT + adopt row-local SKIN CHROMA
  (keeping original chroma at lifted luma = orange line, fails QC).
  (3) realism survives kling/wan animation and the 2K+grain+compression
  pipeline — verify at delivery res in the final pass anyway.

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
