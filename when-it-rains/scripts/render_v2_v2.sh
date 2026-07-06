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
get "$B/hf_20260706_130438_b515ffe6-3a91-4f35-84b4-a756b9450637.mp4" wide.mp4       # WIDE establishing (still B 7219b256 -> kling3_0 d8608711 -> Topaz 2160 b515ffe6): lone man, rushing rainy city, NO lip-sync [0:55 awning replaced per director note]
get "$B/hf_20260703_145655_4be8a2d0-a1d1-4b46-8b67-06381b6039a6.mp4" ghostpud.mp4   # her reflection, rippled apart
get "$B/hf_20260706_013652_e6b78790-8bc3-4163-983e-111ab4d3a6d7.mp4" curbsync.mp4   # curb refit (ffcd446e) -> FRESH audio-driven wan re-sync 821739da -> Topaz 2160 e6b78790 [0:59 lip-sync redo]

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v2sec2/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v2sec2/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v2sec2/concat.txt; }

seg door.mp4     1.20 7.80 0   # 43.0-50.8 one take: out -> walk -> LOOK (4.0-6.5 -> song 45.8-48.3) -> walk on
seg ghostpud.mp4 0.40 3.90 1   # 50.8-54.7 GHOST: her reflection in the puddle - a drop hits - rippled apart
seg wide.mp4     0.60 3.90 2   # 54.7-58.6 WIDE establishing "the sky still holds your whisper" — lone man, rushing rainy city (replaces awning close-up; breaks the two-close-ups + kills lip-sync exposure, sets up the curb push-in)

# CURB ZOOM SYNC (58.6-70.3, 11.7s) — the wan close-up lip-sync can't hold across a
# 12s tight face (AI-from-still ceiling), so we NEVER stay on the mouth for more than
# ~2.3s: FOUR close-up bursts (A/B/C/D) interleaved with THREE 1.1s her-puddle
# reflection flashes. The accelerating push-in + vignette + desaturation ramp run
# CONTINUOUSLY across the whole beat (each burst's zoom 'in' and hue 't' are offset by
# its song-time position), so the emotional build to "I need my world to stop" is
# preserved — the mouth just isn't on screen long enough for the sync to read as off.
# Lip-sync law: curbsync in = song - slice_start(58.5). Zoom off = (Ts-58.6)*24 frames.
#   A 58.60-60.90 (2.30) | cut 60.90-62.00 | B 62.00-64.30 (2.30) | cut 64.30-65.40 |
#   C 65.40-67.70 (2.30) | cut 67.70-68.80 | D 68.80-70.30 (1.50)
CURBZOOM_TAIL="vignette=PI/5,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03,format=yuv420p"
cz() { # $1=curbsync -ss(in)  $2=dur  $3=zoom-off frames  $4=hue-off sec  $5=seg index
  ffmpeg -nostdin -y -loglevel error -ss "$1" -t "$2" -i v2sec2/curbsync.mp4 -vf "\
scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,\
zoompan=z='1+0.10*pow((in+$3)/281,2)':d=1:x='iw/2-(iw/zoom/2)':y='ih*0.22-(ih/zoom/2)':s=1920x1080:fps=24,\
hue=s='max(0.35,1-0.055*(t+$4))',${CURBZOOM_TAIL}" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf 'v2sec2/seg_%02d.mp4' "$5")"
  echo "file '$(printf 'seg_%02d.mp4' "$5")'" >> v2sec2/concat.txt; }
cz 0.10  2.30 0   0.00  3   # A  58.60-60.90
seg ghostpud.mp4 0.40 1.10 4   # cut1 her puddle
cz 3.50  2.30 82  3.40  5   # B  62.00-64.30  (in 3.50, off 82f, hue +3.40)
seg ghostpud.mp4 1.60 1.10 6   # cut2 her puddle (later ripple)
cz 6.90  2.30 163 6.80  7   # C  65.40-67.70  (in 6.90, off 163f, hue +6.80)
seg ghostpud.mp4 2.80 1.10 8   # cut3 her puddle
cz 10.30 1.50 245 10.20 9   # D  68.80-70.30  (in 10.30, off 245f, hue +10.20) — tightest, ends at 1.10x

( cd v2sec2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v2sec2/silent.mp4 -i audio_relay/v2_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v2_v2.mp4
echo "Wrote v2_v2.mp4"
