#!/usr/bin/env python3
"""import_relay.py — the PROVEN git->media_import audio relay for the lip-sync pipeline.

CODE ONLY. This tool DOES NOT push, DOES NOT call any MCP tool, DOES NOT spend
credits, and makes ZERO network calls. It is pure, deterministic plan/plumbing.
The live steps (git push, media_import_url, wan2_7) are run LATER by the assistant
under an explicit human go — this module only builds the exact commands + call
plan for them.

Why a relay at all
------------------
The audio byte-PUT to the Higgsfield presigned upload host (upload.higgsfield.ai)
is EGRESS-BLOCKED in this sandbox (403). The PROVEN in-session ingestion path that
avoids it: the repo is PUBLIC, so a committed file is fetchable at its raw
GitHub URL, and media_import_url(<that raw url>, type=audio) returns an audio
media_id. Verified live this session: audio_relay/hook_vocal.mp3 at commit
8a5048c fetched and returned media_id 082e40a0. Downstream, wan2_7(start_image=<
the still, itself media_import_url'd from its CDN png>, audio_references=[<the
vocal media_id>]) produced a lip-synced clip (still 8ec708fb imported as
686b2b8a).

The relay in four assistant/human-run steps (NOT run by this script)
--------------------------------------------------------------------
  1. git add -f <each segment>   (segments may be *.mp3 = gitignored -> -f)
  2. ONE commit, ONE push        (the ONLY external mutation; needs a go)
  3. for each line:
        media_import_url(raw_url(<pushed sha>, <repo relpath>), type=audio)
            -> vocal media_id
        media_import_url(<still cdn png url>, type=image) -> still media_id
        wan2_7(start_image=<still media_id>, audio_references=[<vocal media_id>])
            -> job -> poll -> mp4
  4. record the produced job_id/mp4 per line.

Steps 2-4 are credit-/mutation-gated and are performed by the assistant with the
user's explicit go. This file NEVER performs them; it only emits the commands and
the ordered call plan (see build_relay_plan / emit_runbook).

HARD REFUSAL: any path that references the egress-blocked upload host
(upload.higgsfield.ai) is refused via assert_no_upload_host (assert-never). The
whole point of the relay is to NOT touch that host.
"""
import sys, os, json, argparse, shutil, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LINE_MAP   = os.path.join(ROOT, "analysis", "line_map.json")
RELAY_DIR  = os.path.join(ROOT, "audio_relay")
PLAN_JSON  = os.path.join(RELAY_DIR, "relay_plan.json")
RUNBOOK_MD = os.path.join(RELAY_DIR, "relay_runbook.md")

# repo-relative prefix for the raw URL + git commands (the project lives under
# when-it-rains/ inside the repo, so relay files are when-it-rains/audio_relay/...)
PROJECT_PREFIX = "when-it-rains"

LIPSYNC_MODEL = "wan2_7"

# The PUBLIC repo the raw URLs resolve against (owner made it public this session).
GH_OWNER = "samuelrkestenbaum-dot"
GH_REPO  = "Imadefiremusicvideos"
RAW_HOST = "raw.githubusercontent.com"

# The egress-blocked host the relay exists to AVOID. Referencing it is a hard error.
FORBIDDEN_UPLOAD_HOST = "upload.higgsfield.ai"


# --------------------------------------------------------------------------- #
# hard refusal — the relay must never touch the egress-blocked upload host
# --------------------------------------------------------------------------- #
def assert_no_upload_host(*values):
    """assert-never: refuse if any value references the egress-blocked upload host.

    The relay's entire reason to exist is to avoid upload.higgsfield.ai (403 here).
    Any code path that lets that host back in is a bug; fail loudly.
    """
    for v in values:
        if v is None:
            continue
        if FORBIDDEN_UPLOAD_HOST in str(v):
            raise AssertionError(
                f"forbidden upload host {FORBIDDEN_UPLOAD_HOST!r} referenced in "
                f"the relay plan ({v!r}) — the git->media_import relay exists "
                f"precisely to avoid it; never PUT to it."
            )


# --------------------------------------------------------------------------- #
# raw URL — the exact public raw.githubusercontent.com string
# --------------------------------------------------------------------------- #
def raw_url(commit_sha, repo_relpath):
    """Return the exact public raw URL for a committed file.

    Shape (verified live): https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>
    repo_relpath is the path FROM THE REPO ROOT (e.g.
    'when-it-rains/audio_relay/hook_vocal.mp3'), with no leading slash.
    """
    rel = str(repo_relpath).lstrip("/")
    url = f"https://{RAW_HOST}/{GH_OWNER}/{GH_REPO}/{commit_sha}/{rel}"
    assert_no_upload_host(url)
    return url


# --------------------------------------------------------------------------- #
# stage a segment — copy it under audio_relay/ and return the `git add -f` cmd
# --------------------------------------------------------------------------- #
def _repo_relpath(dest_abspath):
    """repo-root-relative path for a file under this project (POSIX slashes)."""
    rel_to_project = os.path.relpath(dest_abspath, ROOT)
    return f"{PROJECT_PREFIX}/{rel_to_project}".replace(os.sep, "/")


def stage_segment(seg_path, dest_relpath, copy=True):
    """Place a vocal segment at audio_relay/<dest_relpath> and return its staging info.

    Does NOT run git and does NOT push. Returns a dict:
      dest_abspath   — where the segment lives on disk
      repo_relpath   — path from the repo root (used to build the raw_url after push)
      git_add_cmd    — the EXACT `git add -f ...` command to stage it

    `git add -f` (force) is required because *.mp3 (and *.wav) are gitignored
    (when-it-rains/.gitignore); a plain `git add` would silently skip the segment.
    Set copy=False to compute paths/commands without touching disk (used to build
    a plan when the segment already sits in place / isn't present in this sandbox).
    """
    dest_rel = str(dest_relpath).lstrip("/")
    dest_abspath = os.path.join(RELAY_DIR, dest_rel)
    repo_relpath = _repo_relpath(dest_abspath)
    assert_no_upload_host(seg_path, dest_rel, repo_relpath)

    if copy:
        os.makedirs(os.path.dirname(dest_abspath), exist_ok=True)
        if os.path.abspath(seg_path) != os.path.abspath(dest_abspath):
            shutil.copyfile(seg_path, dest_abspath)

    # -f is load-bearing: mp3/wav are gitignored, plain `add` would skip them.
    git_add_cmd = f"git add -f {repo_relpath}"
    return {
        "dest_abspath": dest_abspath,
        "repo_relpath": repo_relpath,
        "git_add_cmd": git_add_cmd,
    }


# --------------------------------------------------------------------------- #
# build the relay plan — one entry per in-scope line, pure data
# --------------------------------------------------------------------------- #
def _still_png_hint(still_id):
    """The still is imported from its Higgsfield CDN png URL by the assistant.

    We do NOT know the CDN url here (it is a live lookup on the still job_id), so
    the plan records a placeholder the assistant fills in-session. This keeps the
    plan deterministic (no live data baked in) while naming the exact call.
    """
    return f"<cdn png url for still job {still_id}>"


def build_relay_plan(manifest, segment_ext="mp3"):
    """Return the deterministic relay plan for every in-scope line in the line-map.

    `manifest` is the loaded analysis/line_map.json (has 'lines' with in_scope +
    still_id). Pure data — no network, no MCP, no git. The raw_url per line is
    LEFT NULL here (it can only be built after the ONE push, from the real commit
    sha); the assistant fills it via raw_url(<pushed sha>, repo_relpath). The
    media_import_url + wan2_7 calls are recorded as the ordered plan to run.
    """
    lines = manifest.get("lines", [])
    model = manifest.get("lipsync_model", LIPSYNC_MODEL)
    entries = []
    for ln in lines:
        if not ln.get("in_scope"):
            continue
        lid = ln["line_id"]
        still_id = ln["still_id"]
        dest_rel = f"{lid}.{segment_ext}"
        # segment source lives under audio_segments/ (produced by slice_vocals);
        # we do NOT require it to be present to build the plan (copy=False).
        seg_path = f"audio_segments/{lid}.{segment_ext}"
        staged = stage_segment(seg_path, dest_rel, copy=False)
        entry = {
            "line_id": lid,
            "section": ln.get("section"),
            "lyric": ln.get("lyric", ""),
            "target_perf_key": ln.get("target_perf_key"),
            "still_id": still_id,
            "duration_s": ln.get("duration_s"),
            "seg_path": seg_path,
            "dest_relpath": dest_rel,
            "repo_relpath": staged["repo_relpath"],
            "git_add_cmd": staged["git_add_cmd"],
            # raw_url is filled AFTER the push, from the real commit sha:
            #   raw_url(<pushed_sha>, repo_relpath)
            "raw_url": None,
            "calls": [
                {"tool": "media_import_url",
                 "args": {"url": "<raw_url(pushed_sha, repo_relpath)>",
                          "type": "audio"},
                 "returns": ["media_id"],
                 "note": ("import the pushed vocal segment from its PUBLIC raw "
                          "GitHub URL -> audio media_id. This REPLACES the "
                          "egress-blocked presigned-PUT upload endpoint.")},
                {"tool": "media_import_url",
                 "args": {"url": _still_png_hint(still_id), "type": "image"},
                 "returns": ["media_id"],
                 "note": ("import the in-scope still from its Higgsfield CDN png "
                          "url -> image media_id (the wan2_7 start_image must be "
                          "a media, not a raw job_id). Verified: still 8ec708fb "
                          "-> 686b2b8a.")},
                {"tool": model,
                 "args": {"start_image": "<still media_id from step 2>",
                          "audio_references": ["<vocal media_id from step 1>"],
                          "params": {"prompt": ln.get("lyric", ""),
                                     "duration_s": ln.get("duration_s")}},
                 "note": ("audio-driven lip-sync; PROVEN shape start_image + "
                          "audio_references=[media_id]. Poll the job, record the "
                          "mp4. Credit-gated — assistant runs it with a go.")},
            ],
        }
        # defense in depth: nothing in this entry may reference the forbidden host
        assert_no_upload_host(json.dumps(entry, sort_keys=True))
        entries.append(entry)

    plan = {
        "relay": "git-push -> media_import_url(raw github url) -> wan2_7",
        "lipsync_model": model,
        "public_repo": f"{GH_OWNER}/{GH_REPO}",
        "raw_host": RAW_HOST,
        "segment_ext": segment_ext,
        "in_scope_line_count": len(entries),
        "entries": entries,
        "gating": ("PLAN ONLY. No git push, no media_import_url, no wan2_7 in this "
                   "file executes. The assistant runs the ONE push then the "
                   "per-line media_import_url + wan2_7 later, with explicit go. "
                   "raw_url per line is filled after the push from the real sha."),
    }
    assert_no_upload_host(json.dumps(plan, sort_keys=True))
    return plan


# --------------------------------------------------------------------------- #
# runbook — the exact assistant/human-run sequence, documented not executed
# --------------------------------------------------------------------------- #
def emit_runbook(plan):
    """Return the relay runbook markdown (the exact sequence a human/assistant runs)."""
    n = plan["in_scope_line_count"]
    add_cmds = "\n".join(e["git_add_cmd"] for e in plan["entries"])
    lines = [
        "# Relay runbook — git -> media_import_url -> wan2_7 lip-sync",
        "",
        "PROVEN live this session. This runbook is the EXACT sequence the "
        "assistant/human runs. `scripts/import_relay.py` builds the plan + these "
        "commands but RUNS NONE OF THEM — push + media_import + wan2_7 are "
        "credit-/mutation-gated and need an explicit human go.",
        "",
        f"- public repo: `{plan['public_repo']}`  (raw host `{plan['raw_host']}`)",
        f"- lip-sync model: `{plan['lipsync_model']}`",
        f"- in-scope lines: {n}",
        "- the relay deliberately avoids the egress-blocked presigned-PUT upload "
        "endpoint (403 here) — it imports from the public raw GitHub URL instead.",
        "",
        "## Step 1 — stage every segment  (assistant/human)",
        "",
        "Segments are per-line vocal slices under `audio_segments/` (from "
        "`scripts/slice_vocals.py`). They are `*.mp3`/`*.wav` = **gitignored**, so "
        "staging needs `-f` (force). `stage_segment()` copies each into "
        "`audio_relay/` and returns exactly these commands:",
        "",
        "```sh",
        add_cmds if add_cmds else "# (no in-scope lines)",
        "```",
        "",
        "## Step 2 — ONE commit, ONE push  (GATED — needs a human go)",
        "",
        "```sh",
        'git commit -m "Add vocal segments for wan2_7 lip-sync relay"',
        "git push        # the ONLY external mutation in this relay; needs a go",
        "```",
        "",
        "Record the pushed commit sha — every raw URL is built from it.",
        "",
        "## Step 3 — per line: import audio + still, then wan2_7  (GATED — credits)",
        "",
        "For each in-scope line, with `<sha>` = the pushed commit sha:",
        "",
        "```",
        "raw = raw_url(<sha>, <repo_relpath>)          # public GitHub raw URL",
        "vocal_id = media_import_url(raw, type=audio)   # -> audio media_id",
        "still_id = media_import_url(<still cdn png>, type=image)  # -> image media_id",
        "job = wan2_7(start_image=still_id, audio_references=[vocal_id], ...)",
        "poll(job) -> mp4                               # record job_id + mp4 url",
        "```",
        "",
        "Verified live: `audio_relay/hook_vocal.mp3` @ `8a5048c` imported to audio "
        "media `082e40a0`; still `8ec708fb` imported to image media `686b2b8a`; "
        "wan2_7(start_image=686b2b8a, audio_references=[...]) produced a lip-synced "
        "clip.",
        "",
        "## Per-line plan",
        "",
    ]
    for e in plan["entries"]:
        lines.append(f"- **{e['line_id']}** ({e['section']}, {e['target_perf_key']}) "
                     f'"{e["lyric"]}"')
        lines.append(f"  - stage: `{e['git_add_cmd']}`")
        lines.append(f"  - raw_url: `raw_url(<sha>, {e['repo_relpath']})`")
        lines.append(f"  - still: import `{e['still_id']}` (png) -> image media_id")
        lines.append(f"  - wan2_7(start_image=<still media_id>, "
                     f"audio_references=[<vocal media_id>])")
    lines.append("")
    lines.append("## Step 4 — record results")
    lines.append("")
    lines.append("Record `{line_id, vocal_media_id, still_media_id, job_id, mp4_url}` "
                 "per line; hand off to `scripts/swap_lipsync_clips.py` (non-destructive "
                 "repoint) once clips are approved.")
    lines.append("")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# load + main
# --------------------------------------------------------------------------- #
def load_line_map():
    if not os.path.isfile(LINE_MAP):
        raise SystemExit(
            f"missing {os.path.relpath(LINE_MAP, ROOT)} — run "
            f"`python3 scripts/slice_vocals.py --analyze-only` first."
        )
    return json.load(open(LINE_MAP))


def print_plan(plan):
    print("=" * 70)
    print(f"git->media_import relay plan  (model={plan['lipsync_model']}, "
          f"{plan['in_scope_line_count']} in-scope lines)")
    print(f"public repo {plan['public_repo']} via {plan['raw_host']}")
    print("=" * 70)
    for e in plan["entries"]:
        print(f"\n-- {e['line_id']} ({e['section']}, {e['target_perf_key']}) --")
        print(f"   stage : {e['git_add_cmd']}")
        print(f"   raw   : raw_url(<pushed_sha>, {e['repo_relpath']})")
        for i, c in enumerate(e["calls"], 1):
            print(f"   {i}. {c['tool']}({json.dumps(c['args'])})")
    print("\n" + "-" * 70)
    print(plan["gating"])
    print("-" * 70)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="build the git->media_import->wan2_7 relay plan (PLAN ONLY; "
                    "never pushes, imports, or generates)")
    ap.add_argument("--ext", default="mp3", choices=["mp3", "wav"],
                    help="segment file extension to relay (default mp3)")
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="(default) build + write the plan/runbook; NO network, NO MCP")
    ap.add_argument("--go", action="store_true",
                    help="request the live relay — REFUSED here; push + media_import "
                         "+ wan2_7 are run by the assistant with an explicit go")
    args = ap.parse_args(argv)

    if args.go:
        # Hard gate: this script never pushes, imports, or generates.
        raise SystemExit(
            "live relay (git push -> media_import_url -> wan2_7) is NOT performed "
            "by this script — it is credit-/mutation-gated. The assistant runs it "
            "with an explicit human go; this tool only plans it. See relay_runbook.md."
        )

    manifest = load_line_map()
    plan = build_relay_plan(manifest, segment_ext=args.ext)

    os.makedirs(RELAY_DIR, exist_ok=True)
    with open(PLAN_JSON, "w") as f:
        json.dump(plan, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(RUNBOOK_MD, "w") as f:
        f.write(emit_runbook(plan))
    print_plan(plan)
    print(f"\nwrote {os.path.relpath(PLAN_JSON, ROOT)} and "
          f"{os.path.relpath(RUNBOOK_MD, ROOT)} (no network / MCP / git calls made).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
