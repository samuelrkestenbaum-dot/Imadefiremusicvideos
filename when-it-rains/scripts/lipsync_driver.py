#!/usr/bin/env python3
"""lipsync_driver.py — Higgsfield-native lip-sync stage 2: plan the generation.

CODE ONLY by default. This tool DOES NOT generate, DOES NOT spend credits, and in
its default mode makes ZERO network calls. It consumes the deterministic
segments_manifest.json from slice_vocals.py and produces the exact Higgsfield MCP
call plan (media_upload -> byte-PUT -> media_confirm -> wan2_7) for the artist to
run under the assistant with an explicit go.

Two upload paths (the audio bytes cannot leave this sandbox — the presigned PUT
to upload.higgsfield.ai is egress-blocked / 403 here — so the byte-PUT is always
done on the artist's Mac):

  path-b  (mint here, PUT on the Mac):
            1. media_upload(type=audio)           -> {media_id, upload_url, expiry}
            2. curl -T <wav> <upload_url>          (RUN ON THE MAC — see upload_segments.sh)
            3. media_confirm(media_id, type=audio)
            4. wan2_7(start_image=<still_id>, audio_references=[media_id], ...)
          This driver EMITS upload_segments.sh (the curl-PUT script) with a
          presigned-url expiry note; minting (step 1) and confirm/generate
          (steps 3-4) are the gated live MCP calls.

  path-c  (upload in the Higgsfield web-app, paste media_ids back):
            You upload each WAV in the web UI, collect the returned media_id per
            line, and feed them in via --media-ids <json>. Then the driver only
            needs wan2_7(start_image, audio_references=[media_id]).

Gating (hard rule — a subagent/build step must NEVER generate)
--------------------------------------------------------------
  * default = --dry-run: prints the full MCP call sequence + writes
    upload_segments.sh. NO network, NO MCP.
  * --go: the ONLY flag that would permit live calls. Even with --go this script
    does NOT itself call the network — the live functions (mint_and_confirm /
    generate_lipsync) are DOCUMENTED, UN-EXECUTED stubs that raise SystemExit.
    The assistant runs the live MCP tools itself, later, with the user's go.

Usage
-----
  python3 scripts/lipsync_driver.py --dry-run --path b     # plan + upload_segments.sh
  python3 scripts/lipsync_driver.py --dry-run --path c --media-ids ids.json
  python3 scripts/lipsync_driver.py --go ...               # refuses; see gating

CAVEAT on the wan2_7 parameter shape: this session verified wan2_7 is the
audio-driven lip-sync model whose media roles are `start_image` + `audio_references`.
The EXACT request field names (e.g. audio_references as a list of {media_id} vs a
list of ids, and the params block) are model-catalog-dependent; the call plan
below encodes the assumed shape and is the single thing to reconcile at the gated
one-shot validation. Nothing here executes it.
"""
import sys, os, json, argparse, stat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SEG_DIR   = os.path.join(ROOT, "audio_segments")
MANIFEST  = os.path.join(SEG_DIR, "segments_manifest.json")
UPLOAD_SH = os.path.join(SEG_DIR, "upload_segments.sh")
PLAN_JSON = os.path.join(SEG_DIR, "lipsync_plan.json")

LIPSYNC_MODEL = "wan2_7"
UPLOAD_HOST = "upload.higgsfield.ai"     # presigned PUT target (egress-blocked here)
PRESIGN_TTL_MIN = 15                      # typical presigned-url lifetime; re-mint if expired


# --------------------------------------------------------------------------- #
# plan construction (pure — no network, no MCP)
# --------------------------------------------------------------------------- #
def load_manifest():
    if not os.path.isfile(MANIFEST):
        raise SystemExit(
            f"missing {os.path.relpath(MANIFEST, ROOT)} — run "
            f"`python3 scripts/slice_vocals.py` first (needs song.mp3)."
        )
    return json.load(open(MANIFEST))


def build_plan(manifest, path, media_ids=None):
    """Return the ordered MCP call plan for every in-scope segment. Pure data.

    media_ids: optional {line_id: media_id} for path-c (pre-supplied uploads).
    """
    media_ids = media_ids or {}
    steps = []
    for seg in manifest["segments"]:
        lid = seg["line_id"]
        still = seg["still_id"]
        wav_rel = seg["path"]
        if path == "b":
            steps.append({
                "line_id": lid,
                "calls": [
                    {"tool": "media_upload",
                     "args": {"type": "audio", "filename": os.path.basename(wav_rel)},
                     "returns": ["media_id", "upload_url", "expires_at"],
                     "note": "mint a presigned PUT url (host " + UPLOAD_HOST + ")"},
                    {"tool": "curl-PUT (ON THE MAC)",
                     "args": {"file": wav_rel, "url": "<upload_url from media_upload>"},
                     "note": ("byte-PUT is EGRESS-BLOCKED in the build sandbox (403); "
                              "run upload_segments.sh on the artist's Mac within "
                              f"{PRESIGN_TTL_MIN} min of minting or the url expires")},
                    {"tool": "media_confirm",
                     "args": {"media_id": "<media_id from media_upload>", "type": "audio"},
                     "note": "confirm the uploaded audio media"},
                    {"tool": LIPSYNC_MODEL,
                     "args": {"start_image": still,
                              "audio_references": ["<confirmed media_id>"],
                              "params": {"prompt": seg.get("lyric", ""),
                                         "duration_s": seg.get("duration_s")}},
                     "note": ("audio-driven lip-sync; start_image = in-scope still, "
                              "audio_references = the confirmed vocal segment. "
                              "SHAPE ASSUMED — reconcile at gated validation.")},
                ],
            })
        elif path == "c":
            mid = media_ids.get(lid, f"<media_id for {lid} from web-app upload>")
            steps.append({
                "line_id": lid,
                "calls": [
                    {"tool": LIPSYNC_MODEL,
                     "args": {"start_image": still,
                              "audio_references": [mid],
                              "params": {"prompt": seg.get("lyric", ""),
                                         "duration_s": seg.get("duration_s")}},
                     "note": ("path-c: audio already uploaded+confirmed in the "
                              "Higgsfield web-app; media_id supplied via --media-ids. "
                              "SHAPE ASSUMED — reconcile at gated validation.")},
                ],
            })
        else:
            raise SystemExit(f"unknown --path {path!r} (use 'b' or 'c')")
    return {
        "lipsync_model": LIPSYNC_MODEL,
        "upload_path": path,
        "presigned_ttl_minutes": PRESIGN_TTL_MIN,
        "segment_count": len(steps),
        "steps": steps,
        "gating": ("DRY-RUN plan only. No MCP call in this file executes. The "
                   "assistant runs media_upload/media_confirm/wan2_7 later, with "
                   "explicit user go."),
    }


def write_upload_script(manifest, path):
    """Emit the curl-PUT script the Mac runs after minting (path-b only)."""
    lines = [
        "#!/usr/bin/env bash",
        "# upload_segments.sh — RUN ON THE ARTIST'S MAC (not in the build sandbox).",
        "#",
        "# The presigned PUT to " + UPLOAD_HOST + " is egress-blocked here (403), so the",
        "# audio byte-upload must happen on your machine. For EACH segment:",
        "#   1. the assistant mints a presigned upload_url via media_upload (in-session),",
        "#   2. you paste that url below (or the assistant fills it in),",
        "#   3. this script PUTs the WAV bytes to it,",
        "#   4. the assistant calls media_confirm then wan2_7.",
        "#",
        f"# EXPIRY: presigned upload_urls expire ~{PRESIGN_TTL_MIN} min after minting.",
        "#         If a PUT returns 403/expired, RE-MINT (media_upload) and retry.",
        "set -euo pipefail",
        'cd "$(dirname "$0")"',
        "",
        "put() {  # put <wav_file> <presigned_url>",
        '  local f="$1" url="$2"',
        '  echo "PUT $f -> ${url%%\\?*} (expires ~' + str(PRESIGN_TTL_MIN) + ' min after mint)"',
        '  curl -sS -f -X PUT -T "$f" -H "Content-Type: audio/wav" "$url"',
        "}",
        "",
    ]
    if path == "b":
        for seg in manifest["segments"]:
            wav = os.path.basename(seg["path"])
            lines.append(f'# {seg["line_id"]}  ({seg["target_perf_key"]})  '
                         f'"{seg.get("lyric","")}"')
            lines.append(f'# put "{wav}" "<PRESIGNED_URL_FOR_{seg["line_id"]}>"')
            lines.append("")
    else:
        lines.append("# path-c selected: no byte-PUT needed here (uploaded in the "
                      "Higgsfield web-app). This script is a no-op placeholder.")
        lines.append("")
    lines.append('echo "done — now the assistant runs media_confirm + ' + LIPSYNC_MODEL + '"')
    with open(UPLOAD_SH, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(UPLOAD_SH, os.stat(UPLOAD_SH).st_mode | stat.S_IXUSR | stat.S_IXGRP)


def print_plan(plan):
    print("=" * 66)
    print(f"Higgsfield lip-sync call plan  (model={plan['lipsync_model']}, "
          f"path={plan['upload_path']}, {plan['segment_count']} segments)")
    print("=" * 66)
    for step in plan["steps"]:
        print(f"\n-- {step['line_id']} --")
        for i, c in enumerate(step["calls"], 1):
            print(f"  {i}. {c['tool']}({json.dumps(c['args'])})")
            if c.get("note"):
                print(f"     # {c['note']}")
    print("\n" + "-" * 66)
    print(plan["gating"])
    print("-" * 66)


# --------------------------------------------------------------------------- #
# LIVE path — DOCUMENTED, UN-EXECUTED. Never called by this script.
# --------------------------------------------------------------------------- #
def mint_and_confirm(*_a, **_k):  # pragma: no cover - intentionally never run here
    """LIVE: media_upload -> (Mac PUT) -> media_confirm. Assistant-only, gated.

    This is a placeholder describing the live MCP sequence. A build step / subagent
    MUST NOT generate, so this raises rather than acting. The assistant performs
    the real media_upload / media_confirm MCP calls in-session with explicit go.
    """
    raise SystemExit(
        "live media_upload/media_confirm requires MCP; run under the assistant "
        "with explicit go — this driver never mints/confirms on its own."
    )


def generate_lipsync(*_a, **_k):  # pragma: no cover - intentionally never run here
    """LIVE: wan2_7(start_image, audio_references=[media_id]). Assistant-only, gated.

    Un-executed on purpose. The one-shot wan2_7 validation is a separate, gated
    step the assistant runs later with the user's go. This function exists only to
    name the live call site; it never executes here.
    """
    raise SystemExit(
        "live generation requires MCP; run under the assistant with explicit go "
        "— this driver plans the wan2_7 call but never executes it."
    )


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="plan the Higgsfield wan2_7 lip-sync (DRY-RUN by default; never generates)")
    ap.add_argument("--path", choices=["b", "c"], default="b",
                    help="b = mint here + PUT on the Mac; c = pre-supplied media_ids")
    ap.add_argument("--media-ids", metavar="JSON",
                    help="path-c: JSON {line_id: media_id} from the web-app upload")
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="(default) print the MCP plan + write upload_segments.sh; NO network")
    ap.add_argument("--go", action="store_true",
                    help="request live generation — REFUSED here; the assistant runs "
                         "live MCP with explicit go (see gating in the module docstring)")
    args = ap.parse_args(argv)

    if args.go:
        # The hard gate: this script never generates. --go routes to the
        # documented, un-executed live stub, which stops immediately.
        print("!! --go: live generation is NOT performed by this script.")
        generate_lipsync()      # raises SystemExit — never returns
        return 2                # unreachable

    manifest = load_manifest()
    media_ids = {}
    if args.media_ids:
        media_ids = json.load(open(args.media_ids))

    os.makedirs(SEG_DIR, exist_ok=True)
    plan = build_plan(manifest, args.path, media_ids)
    with open(PLAN_JSON, "w") as f:
        json.dump(plan, f, indent=2)
        f.write("\n")
    write_upload_script(manifest, args.path)
    print_plan(plan)
    print(f"\nwrote {os.path.relpath(PLAN_JSON, ROOT)} and "
          f"{os.path.relpath(UPLOAD_SH, ROOT)} (no network calls made).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
