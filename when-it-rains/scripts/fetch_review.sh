#!/usr/bin/env bash
# fetch_review.sh — CI-side asset fetcher. The dev sandbox cannot reach the
# Higgsfield CDN, so it cannot LOOK at generated stills/clips before using
# them. CI has full egress: this script downloads every URL listed in
# review_urls.txt into when-it-rains/review/, the workflow commits them, and
# the sandbox pulls + inspects them (Read renders images) before they are
# approved into a cut.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p review
: > review/.fetched
while IFS= read -r url; do
  url="$(echo "$url" | tr -d '[:space:]')"
  [ -z "$url" ] && continue
  case "$url" in \#*) continue ;; esac
  f="review/$(basename "$url")"
  if [ ! -s "$f" ]; then
    echo "fetch $(basename "$url")"
    curl -fSL --retry 4 --retry-delay 2 -o "$f" "$url"
  fi
  echo "$f" >> review/.fetched
  # for video takes, extract 2fps thumbnails so the sandbox can eyeball motion
  case "$f" in
    *.mp4)
      d="review/$(basename "$f" .mp4)_frames"
      if [ ! -d "$d" ] && command -v ffmpeg >/dev/null 2>&1; then
        mkdir -p "$d"
        ffmpeg -nostdin -y -loglevel error -i "$f" -vf "fps=2,scale=640:-2" -q:v 4 "$d/f_%03d.jpg"
      fi
      ;;
  esac
done < review_urls.txt
ls -la review/
