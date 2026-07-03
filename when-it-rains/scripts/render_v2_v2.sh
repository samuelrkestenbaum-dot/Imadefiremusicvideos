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
get "$B/hf_20260703_010041_c742b889-9c29-4f0d-b214-3b70ea5b794f.mp4" door.mp4       # repaired door take
get "$B/hf_20260703_043914_ab86a6c8-ba25-48b5-9be4-b81f5ae0e58d.mp4" sync.mp4       # awning sync 2K (realism still, continuous line)
get "$B/hf_20260703_010458_31ccf929-5637-4a0d-a75c-ebfbaba8ca51.mp4" ghostpud.mp4   # her reflection, rippled apart
get "$B/hf_20260703_104358_2ad7d2e3-edcd-4672-892b-aacb908698ca.mp4" curbsync.mp4   # 12s curb zoom sync 2K

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v2sec2/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v2sec2/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v2sec2/concat.txt; }

seg door.mp4     1.20 7.80 0   # 43.0-50.8 one take: out -> walk -> LOOK (4.0-6.5 -> song 45.8-48.3) -> walk on
seg ghostpud.mp4 0.40 3.90 1   # 50.8-54.7 GHOST: her reflection in the puddle - a drop hits - rippled apart
seg sync.mp4     0.10 3.90 2   # 54.7-58.6 SYNC "the sky still holds your whisper" (slice 54.6; seg at song 54.7)

# seg 3 — CURB ZOOM SYNC (58.6-70.3): 12s lip-sync hold while the world rushes;
# accelerating push-in on his face, vignette, slow desaturation ramp.
# Lip sync law: seg in = song_time_at_slot_start - slice_start = 58.6 - 58.5 = 0.10.
ffmpeg -nostdin -y -loglevel error -ss 0.10 -t 11.70 -i v2sec2/curbsync.mp4 -vf "\
scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,\
zoompan=z='1+1.1*pow(in/281,2)':d=1:x='iw/2-(iw/zoom/2)':y='ih/3-(ih/zoom/3)':s=1920x1080:fps=24,\
vignette=PI/5,hue=s='max(0.35,1-0.055*t)',\
noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 v2sec2/seg_03.mp4
echo "file 'seg_03.mp4'" >> v2sec2/concat.txt

( cd v2sec2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v2sec2/silent.mp4 -i audio_relay/v2_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v2_v2.mp4
echo "Wrote v2_v2.mp4"
