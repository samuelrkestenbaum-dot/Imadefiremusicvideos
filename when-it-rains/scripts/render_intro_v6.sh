#!/usr/bin/env bash
# render_intro_v6.sh — v5 with the OPENING MATCHED to the bedroom:
#   the old rain-on-glass opener showed a different street; the new opener is
#   a close-up of the BEDROOM's own window (derived from approved master
#   2d080b77), so shot 1 and the bed scene share one world. All other segments
#   identical to v5 (double-bed take, her-pillow insert, sync line, maybe-her).
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/intro_open24.mp3 ] || { echo "ERROR: audio_relay/intro_open24.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
GHOST_OPACITY=0.30
mkdir -p intro6; : > intro6/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
# slow push-in for the cold-open window so shot 1 isn't a locked-off frozen frame
# (scale up first so the zoom crop stays sharp, zoom within, output 1280x720)
PUSHWIN="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,zoompan=z='min(1.15,1+0.15*in/143)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24"
get() { [ -s "intro6/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "intro6/$2" "$1"; }; }
get "$B/hf_20260702_140435_371791eb-362a-4d16-8510-5af28934f31d.mp4" rain.mp4    # bedroom's own window (derived from master)
get "$B/hf_20260702_131248_eea03072-8e77-486f-9cac-289f6382decc.mp4" bed.mp4      # NEW double-bed take (from approved master)
get "$B/hf_20260702_132700_8bd72a9d-b8c5-49d7-a417-119421449565.mp4" herhalf.mp4  # tight close: her untouched pillow (same-master derivation)
get "$B/hf_20260701_234439_2280a662-c5e2-4bf2-aa65-4d5535bd6783.mp4" window.mp4
get "$B/hf_20260702_115455_24c8dda3-562c-4b43-affb-d5fbb6d894c9.mp4" sync.mp4    # through-glass lip-sync (song 18.5s == clip 0)
get "$B/hf_20260701_234443_f4405992-922d-448f-af9b-4806393a556e.png" shape.png

seg() { local vf="${5:-$VF}"; ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "intro6/$1" -vf "$vf,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "intro6/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> intro6/concat.txt; }

seg rain.mp4    0.50 6.00 0 "$PUSHWIN"   # 0-6      the first breath (slow push-in, no longer locked-off)
seg bed.mp4     1.70 5.80 1   # 6-11.8   lying still; head turn lands 6.5-7.5 (measured)
seg herhalf.mp4 0.60 3.90 2   # 11.8-15.7 his eyeline: her untouched pillow
seg bed.mp4     7.60 2.30 3   # 15.7-18  back into the take: he rises (7.6-9.9 measured)
seg window.mp4  0.80 1.30 4   # 18-19.3  inside, at the window
seg sync.mp4    0.80 3.70 5   # 19.3-23  THROUGH THE GLASS: he sings the line (clip0=song18.5 -> in 0.8)

# seg 6 — the maybe-her, AFTER the line (23-24): interior take + shape @ GHOST_OPACITY
ffmpeg -nostdin -y -loglevel error \
  -ss 2.40 -t 1.00 -i intro6/window.mp4 \
  -loop 1 -t 1.00 -i intro6/shape.png \
  -filter_complex "[0:v]${VF},setpts=PTS-STARTPTS[bg];[1:v]${VF},setpts=PTS-STARTPTS,format=yuva420p,colorchannelmixer=aa=${GHOST_OPACITY}[fg];[bg][fg]overlay=shortest=1,fps=24,format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 intro6/seg_06.mp4
echo "file 'seg_06.mp4'" >> intro6/concat.txt

( cd intro6 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i intro6/silent.mp4 -i audio_relay/intro_open24.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest intro_v6.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 intro_v6.mp4 2>/dev/null || echo "?")
echo "Wrote intro_v6.mp4  (${dur}s — first line lip-synced through the glass; maybe-her after the line)"
