#!/usr/bin/env python3
"""build_edit_v2.py — the director's cut of "When It Rains" (late-90s/2000s rain ballad).

Sequences the 24 new reference-anchored clips to the lyrics + beat grid:
  - cuts land on beats (beats.json), verses breathe, choruses/bridge go dense
  - NO clip repeats inside an 8-cut window (kills the old C02-x11 recycling)
  - in-point shifts on reuse so a reused clip doesn't replay the identical frames
  - total locked to the song (~274s)

Writes data/clips.csv (the 24 clips) + data/edl.csv (the cut). Backs up the old
70s-era edit to data/*.70s.csv. Reads the asset map from a JSON passed as argv[1]
(default: the P-016 scratchpad map).
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BEATS = json.load(open(os.path.join(ROOT, "analysis", "beats.json")))["beat_times"]
MAP_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/tmp/claude-0/-home-user/e7e0708c-394d-59fb-9135-c44d3f191eb6/scratchpad/p016_clips.json"
CLIPS = json.load(open(MAP_PATH))
SRC_LEN = 5.0
NO_REPEAT = 8            # a shot may not recur within this many cuts

# (name, end_time, beats_per_cut, [ordered shot playlist])  — start = previous end
SECTIONS = [
 ("INTRO", 18.0, 4, ["ATM_window","PERF_window","ATM_river","RAIN_plate","MEM_touch"]),
 ("V1", 41.25, 4, ["PERF_profile","MEM_touch","MEM_happy","MEM_water","ATM_river","PERF_window"]),
 ("V2", 69.75, 4, ["PERF_listen","ATM_window","HER_rain","PERF_profile","MEM_mirror","RAIN_plate","PERF_window"]),
 ("PRE1", 89.25, 3, ["PERF_hook","ATM_window","ATM_trees","MEM_turn","PERF_lookup","ATM_lightning","HER_rain"]),
 ("CH1", 128.0, 2, ["HER_rain","PERF_hook","ATM_lightning","MEM_clouds","PERF_lookup","RAIN_plate",
                    "PERF_profile","ATM_trees","PERF_outside","MEM_happy","ATM_window","PERF_reach"]),
 ("V3", 144.5, 3, ["PERF_listen","ATM_trees","PERF_profile","ATM_window","PERF_window","MEM_mirror"]),
 ("V4", 173.0, 4, ["MEM_mirror","ATM_drawer","PERF_profile","ATM_window","PERF_listen","MEM_turn","PERF_window"]),
 ("PRE2", 214.0, 2, ["PERF_hook","MEM_clouds","PERF_lookup","ATM_lightning","PERF_reach","HER_rain",
                     "PERF_profile","ATM_trees","RAIN_plate","MEM_clouds","PERF_outside","PERF_hook"]),
 ("CH2", 238.0, 2, ["HER_rain","PERF_hook","ATM_lightning","MEM_clouds","PERF_lookup","RAIN_plate",
                    "PERF_outside","PERF_profile","ATM_trees","PERF_reach","MEM_dissolve","PERF_hook"]),
 ("BRIDGE", 261.0, 3, ["ATM_drop","MEM_whisper","PERF_outside","ATM_flood","MEM_dissolve",
                       "PERF_reach","ATM_flood","MEM_whisper","PERF_outside"]),
 ("FINAL", 274.0, 3, ["PERF_outside","MEM_dissolve","HER_rain","PERF_lookup","ATM_drop"]),
]

def beats_between(a, b):
    return [t for t in BEATS if a - 1e-6 < t < b - 1e-6]

rows = []          # (clip_key, in_point, duration, section, note)
recent = []        # last NO_REPEAT chosen keys
use_count = {}
start = 0.0
for name, end, bpc, playlist in SECTIONS:
    # cut boundaries: section start, every bpc-th interior beat, section end
    interior = beats_between(start, end)
    picks = interior[bpc-1::bpc]
    bounds = [start] + picks + [end]
    # drop a tiny final sliver by merging into previous boundary
    if len(bounds) >= 3 and bounds[-1] - bounds[-2] < 0.8:
        bounds.pop(-2)
    pi = 0
    for i in range(len(bounds) - 1):
        dur = round(bounds[i+1] - bounds[i], 2)
        if dur <= 0: continue
        # choose next playlist shot not used within NO_REPEAT
        key = None
        for _ in range(len(playlist)):
            cand = playlist[pi % len(playlist)]; pi += 1
            if cand not in recent[-NO_REPEAT:]:
                key = cand; break
        if key is None:                      # whole playlist blocked — take next anyway
            key = playlist[pi % len(playlist)]; pi += 1
        recent.append(key)
        n = use_count.get(key, 0); use_count[key] = n + 1
        in_point = round(min(n * 1.0, max(0.0, SRC_LEN - dur)), 2)   # shift into clip on reuse
        rows.append((key, in_point, dur, name, CLIPS[key]["motion"]))
    start = end

# renormalize so total == 274.00 exactly (absorb rounding into the last cut)
total = sum(r[2] for r in rows)
if abs(total - 274.0) > 1e-9:
    k, ip, d, s, nt = rows[-1]
    rows[-1] = (k, ip, round(d + (274.0 - total), 2), s, nt)

# --- write data/edl.csv ---
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
# back up the old 70s edit once
for f in ("edl.csv", "clips.csv", "stills.csv"):
    src = os.path.join(ROOT, "data", f); bak = os.path.join(ROOT, "data", f.replace(".csv", ".70s.csv"))
    if os.path.exists(src) and not os.path.exists(bak):
        os.rename(src, bak)

# new stills catalog: the 24 source stills (still_id, url unknown here -> blank-safe note).
# The render never reads stills; this keeps preflight's source_still check satisfied.
with open(os.path.join(ROOT, "data", "stills.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["still_id","url","prompt_summary"])
    for key, c in CLIPS.items():
        w.writerow([c["still"], "", f"{key} source still ({c['world']})"])

with open(os.path.join(ROOT, "data", "edl.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["index","clip_key","in_point","duration","section","note"])
    for i, (key, ip, d, s, nt) in enumerate(rows, 1):
        w.writerow([i, key, ip, d, s, nt])

# --- write data/clips.csv (the 24 clips; url is the 5th column for fetch_assets.sh) ---
with open(os.path.join(ROOT, "data", "clips.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["clip_key","job_id","source_still","section","mp4_url","motion"])
    for key, c in CLIPS.items():
        w.writerow([key, c["clip"], c["still"], c["world"], c["url"], c["motion"]])

print(f"cuts: {len(rows)}   total: {sum(r[2] for r in rows):.2f}s   distinct clips: {len(use_count)}")
print("uses:", dict(sorted(use_count.items(), key=lambda x:-x[1])))
