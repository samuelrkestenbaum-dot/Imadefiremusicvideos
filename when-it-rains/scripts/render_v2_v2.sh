#!/usr/bin/env bash
# render_v2_v2.sh — V2 street, P-023 recut: door take unchanged; the GHOST
# puddle (her reflection, rippled apart) moves up into the 50.8-54.7 slot;
# the awning sync is the new realism-still 2K; the whole back half 58.6-70.3
# is the CURB ZOOM SYNC finale: he sings "and I need my world to stop" while
# the world rushes behind him and the camera pushes in with accelerating
# zoom, vignette and a slow desaturation ramp.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/v2_bed.mp3 ] || { echo "ERROR: audio_relay/v2_bed.mp3 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p v2sec2; : > v2sec2/concat.txt
VF="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
get() { [ -s "v2sec2/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "v2sec2/$2" "$1"; }; }
get "$B/hf_20260703_145638_9015cb88-1322-4ad6-8849-524ca144423f.mp4" door.mp4       # repaired door take
get "$B/hf_20260706_013609_8c119ef1-f4c6-4b0a-b14c-b65028c0f6d6.mp4" sync.mp4       # awning refit (bc3bb964) -> FRESH audio-driven wan re-sync 9910f6d1 -> Topaz 2160 8c119ef1 [0:55 lip-sync redo]
get "$B/hf_20260703_145655_4be8a2d0-a1d1-4b46-8b67-06381b6039a6.mp4" ghostpud.mp4   # her reflection, rippled apart
get "$B/hf_20260706_013652_e6b78790-8bc3-4163-983e-111ab4d3a6d7.mp4" curbsync.mp4   # curb refit (ffcd446e) -> FRESH audio-driven wan re-sync 821739da -> Topaz 2160 e6b78790 [0:59 lip-sync redo]

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v2sec2/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v2sec2/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v2sec2/concat.txt; }

seg door.mp4     1.20 7.80 0   # 43.0-50.8 one take: out -> walk -> LOOK (4.0-6.5 -> song 45.8-48.3) -> walk on
seg ghostpud.mp4 0.40 3.90 1   # 50.8-54.7 GHOST: her reflection in the puddle - a drop hits - rippled apart
seg sync.mp4     0.10 3.90 2   # 54.7-58.6 SYNC "the sky still holds your whisper" (slice 54.6; seg at song 54.7)

# seg 3/4/5 — CURB ZOOM SYNC (58.6-70.3), now BROKEN by a 1.3s apparition flash so
# the pre-chorus has rhythm instead of one 12s single-composition hold. The
# accelerating push-in, vignette and desaturation ramp CONTINUE across the cut
# (zoom 'in' and hue 't' are offset in piece 2 so it resumes where it left off),
# so the emotional build isn't lost — it just breathes once.
#   piece 1  58.6-64.0 (5.40s, zoom frames 0-129)
#   cutaway  64.0-65.3 (1.30s, her puddle reflection — seeds the 1:33 payoff)
#   piece 2  65.3-70.3 (5.00s, zoom continues from frame ~161)
# Lip-sync law: curbsync in = song - slice_start(58.5); piece2 in = 0.10 + (65.3-58.6) = 6.80.
CURBZOOM_TAIL="vignette=PI/5,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03,format=yuv420p"
ffmpeg -nostdin -y -loglevel error -ss 0.10 -t 5.40 -i v2sec2/curbsync.mp4 -vf "\
scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,\
zoompan=z='1+0.10*pow(in/281,2)':d=1:x='iw/2-(iw/zoom/2)':y='ih*0.22-(ih/zoom/2)':s=1920x1080:fps=24,\
hue=s='max(0.35,1-0.055*t)',${CURBZOOM_TAIL}" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 v2sec2/seg_03.mp4
echo "file 'seg_03.mp4'" >> v2sec2/concat.txt
# cutaway: her reflection flickers in the puddle (apparition motif, pre-chorus)
seg ghostpud.mp4 2.50 1.30 4
# piece 2: zoom + desaturation resume (offsets: in+161 frames, t+6.70s)
ffmpeg -nostdin -y -loglevel error -ss 6.80 -t 5.00 -i v2sec2/curbsync.mp4 -vf "\
scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,\
zoompan=z='1+0.10*pow((in+161)/281,2)':d=1:x='iw/2-(iw/zoom/2)':y='ih*0.22-(ih/zoom/2)':s=1920x1080:fps=24,\
hue=s='max(0.35,1-0.055*(t+6.70))',${CURBZOOM_TAIL}" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 v2sec2/seg_05.mp4
echo "file 'seg_05.mp4'" >> v2sec2/concat.txt

( cd v2sec2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v2sec2/silent.mp4 -i audio_relay/v2_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v2_v2.mp4
echo "Wrote v2_v2.mp4"
