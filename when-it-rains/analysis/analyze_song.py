#!/usr/bin/env python3
"""Analyze the song's structure to time the edit to the music.

Usage:  python3 analysis/analyze_song.py /path/to/song.mp3
Outputs (next to this script):
  song.json            duration, music_end, tempo, energy transitions
  song_structure.png   energy curve + EDL section lines + detected transitions

Deps:  pip install imageio-ffmpeg numpy matplotlib
(imageio-ffmpeg ships a static ffmpeg, so no system ffmpeg needed.)
"""
import sys, subprocess, json, os
import numpy as np
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 22050

def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"

def main(path):
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    raw = subprocess.run([ff, "-v", "quiet", "-i", path, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], stdout=subprocess.PIPE).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    dur = len(x) / SR

    hop = int(0.25 * SR); frames = len(x) // hop
    env = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(frames)])
    t = np.arange(frames) * 0.25
    k = np.ones(5) / 5
    envs = np.convolve(env, k, mode="same")

    # music end = last frame above 12% of peak
    thr = 0.12 * envs.max()
    above = np.where(envs > thr)[0]
    music_end = float(t[above[-1]]) if len(above) else dur

    # structure transitions = biggest energy changes, min 12s apart
    ec = np.convolve(env, np.ones(12)/12, mode="same")
    d = np.abs(np.diff(ec)); picked = []
    for idx in np.argsort(d)[::-1]:
        if all(abs(t[idx]-p) > 12 for p in picked): picked.append(float(t[idx]))
        if len(picked) >= 12: break
    picked.sort()

    # tempo via onset autocorrelation
    fh = 512; ww = 1024; nf = (len(x)-ww)//fh
    fe = np.array([np.sum(x[i*fh:i*fh+ww]**2) for i in range(nf)])
    on = np.diff(fe); on[on < 0] = 0; on = on - on.mean()
    ac = np.correlate(on, on, "full")[len(on)-1:]
    fr = SR/fh; lo, hi = int(fr*60/160), int(fr*60/60)
    lag = lo + int(np.argmax(ac[lo:hi])); bpm = 60*fr/lag

    json.dump({"duration": dur, "music_end": music_end, "tempo_bpm": float(bpm),
               "transitions": picked}, open(f"{HERE}/song.json", "w"), indent=2)
    print(f"duration {mmss(dur)}  music_end {mmss(music_end)}  tempo {bpm:.1f} BPM")
    print("transitions:", [round(p, 1) for p in picked])

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        edl = [("INTRO",0),("V1",18),("V2",48),("PRE1",78),("CH1",103),("V3",128),
               ("V4",159),("PRE2",189),("CH2",214),("BRIDGE",238),("FINAL",261)]
        fig, ax = plt.subplots(figsize=(16, 5))
        ax.plot(t, envs, color="#2b6cb0", lw=1.2)
        ax.fill_between(t, envs, color="#2b6cb0", alpha=0.15)
        for n, s in edl:
            ax.axvline(s, color="#e53e3e", ls="--", lw=1, alpha=0.8)
            ax.text(s+1, envs.max()*0.95, n, rotation=90, va="top", fontsize=8, color="#c53030")
        for p in picked: ax.axvline(p, color="#38a169", ls=":", lw=1, alpha=0.7)
        ax.axvline(music_end, color="black", lw=1.5, alpha=0.6)
        ax.set_title("When It Rains — energy (red=current EDL sections, green=detected transitions)")
        ax.set_xlim(0, dur)
        xt = np.arange(0, dur, 30); ax.set_xticks(xt)
        ax.set_xticklabels([mmss(v) for v in xt], fontsize=7)
        plt.tight_layout(); plt.savefig(f"{HERE}/song_structure.png", dpi=110)
        print("wrote song_structure.png")
    except Exception as e:
        print("plot skipped:", e)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/../song.mp3")
