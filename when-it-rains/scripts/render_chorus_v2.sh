#!/usr/bin/env bash
# render_chorus_v2.sh — director's cut of the chorus couplet (~12s), performance-forward,
# cut on the beat: front lip-sync takes (mouth locked to your vocal) intercut with other
# angles of you + story/atmosphere scenes. Audio is the continuous couplet vocal (from
# take B), so cuts stay smooth and in sync. Needs only ffmpeg (no song file).
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v2.sh && open chorus_v2.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus2; : > chorus2/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { # url dest
  [ -s "chorus2/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus2/$2" "$1"; }
}
# sources
get "$B/hf_20260701_171803_25a4e947-d49d-47f4-a675-01ac8b375d42.mp4" takeB.mp4   # front lip-sync (buzz OK)
get "$B/hf_20260701_171806_68df0466-bad2-4a86-9c8f-1943a602f19f.mp4" takeD.mp4   # front lip-sync (buzz OK)
get "$B/hf_20260701_151152_c6d30594-2cf7-4902-be60-856573cd52c7.mp4" profile.mp4 # you, profile
get "$B/hf_20260701_151427_960758d1-ebb5-44ec-a24e-ac3ed7a35437.mp4" reach.mp4   # you, reaching into rain
get "$B/hf_20260701_151159_33e0fa39-3ebf-4476-9955-9c9a08cfea33.mp4" outside.mp4 # you, from behind, soaked
get "$B/hf_20260701_151102_ba6f80d3-bf4e-4dad-8ad0-bc9191d231e7.mp4" her.mp4      # her, in the rain
get "$B/hf_20260701_151505_19aef6dc-3648-4166-8477-f5e1a7337298.mp4" lightning.mp4

# cut list: file  in_point  duration  (lip-sync takes' in_point == output start so audio stays synced)
CUTS=(
  "takeB.mp4 0.00 1.97"    # HERO open — "when it rains you're in the water"  (hold)
  "profile.mp4 0.60 0.98"  # cut: you, profile
  "takeD.mp4 2.95 0.97"    # lip-sync, angle 2
  "her.mp4 1.00 0.98"      # scene: her in the rain
  "takeB.mp4 4.90 0.97"    # lip-sync
  "reach.mp4 1.00 0.98"    # cut: you reaching up into the rain
  "takeD.mp4 6.85 0.97"    # lip-sync
  "lightning.mp4 0.40 0.98" # scene: lightning ("thunder")
  "takeB.mp4 8.80 0.97"    # lip-sync
  "outside.mp4 1.00 0.98"  # cut: you from behind, soaked
  "takeD.mp4 10.75 1.25"   # HERO close — "like the thunder"  (hold)
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus2/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus2/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus2/concat.txt
  i=$((i+1))
done

( cd chorus2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
# audio = the continuous couplet vocal baked into take B
ffmpeg -nostdin -y -loglevel error -i chorus2/silent.mp4 -i chorus2/takeB.mp4 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v2.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v2.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v2.mp4  (${dur}s — performance-forward chorus: lip-sync + your angles + story, cut on the beat)"
