#!/usr/bin/env bash
# render_v1_v2.sh — V1 kitchen, likeness-era recut: identical to v1_v1 except
# the outro rain-window now carries the LADDER INSERT (rung 0.5): the ghost
# take blended at 45% over the plain take (same source frame = perfect
# registration) — a faint figure smear behind the glass that HE never sees.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/v1_bed.mp3 ] || { echo "ERROR: audio_relay/v1_bed.mp3 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
GHOST_OPACITY=0.65
mkdir -p v1sec2; : > v1sec2/concat.txt
VF="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
PUNCH="crop=768:432:256:144,scale=1920:1080,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
get() { [ -s "v1sec2/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "v1sec2/$2" "$1"; }; }
get "$B/hf_20260703_014921_82720c7f-c1e5-4e93-811e-f18a25dfb81c.mp4" mugs.mp4   # 2K-enhanced take
get "$B/hf_20260703_043220_c3cddeb8-178a-445c-ae62-16a067042fd5.mp4" sync.mp4   # new kitchen 2K lip-sync
get "$B/hf_20260703_145649_41b05e2e-63fb-4845-873a-785776ace7d6.mp4" rain.mp4
get "$B/hf_20260703_145652_9c97e121-7949-4810-b4fe-c876baa45613.mp4" ghostwin.mp4

seg() { local vf="${5:-$VF}"
  ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v1sec2/$1" -vf "$vf,fps=24,format=yuv420p" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v1sec2/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v1sec2/concat.txt; }

seg mugs.mp4 0.70 7.80 0            # 0-7.8    the two mugs: touch -> pickup -> carry
seg sync.mp4 0.10 3.90 1            # 7.8-11.7 SYNC "my heart had crossed the ocean" (slice 31.2; seg at song 31.3)
seg rain.mp4 0.60 3.00 2 "$PUNCH"   # 11.7-14.7 rivers on the glass (plain)
seg mugs.mp4 8.40 1.60 3            # 14.7-16.3 the mug goes back, door closes

# seg 4 — LADDER 0.5 (16.3-19.5): ghost take blended over plain take @45%
ffmpeg -nostdin -y -loglevel error \
  -ss 1.20 -t 3.20 -i v1sec2/rain.mp4 \
  -ss 0.30 -t 3.20 -i v1sec2/ghostwin.mp4 \
  -filter_complex "[0:v]${PUNCH},setpts=PTS-STARTPTS[bg];[1:v]${PUNCH},setpts=PTS-STARTPTS,format=yuva420p,colorchannelmixer=aa=${GHOST_OPACITY}[fg];[bg][fg]overlay=shortest=1,fps=24,format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 v1sec2/seg_04.mp4
echo "file 'seg_04.mp4'" >> v1sec2/concat.txt

( cd v1sec2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v1sec2/silent.mp4 -i audio_relay/v1_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v1_v2.mp4
echo "Wrote v1_v2.mp4"
