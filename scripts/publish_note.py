#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


RUNTIME = Path(os.environ.get("SOCIAL_AUTO_UPLOAD_HOME", Path.home() / ".openclaw/workspace/social-auto-upload"))
SAU = RUNTIME / ".venv" / "bin" / "sau"
ACCOUNTS = {
    "xiaohongshu": "<xiaohongshu_account>",
    "douyin": "<douyin_account>",
    "kuaishou": "<kuaishou_account>",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish image-note content through sau.")
    parser.add_argument("--platform", choices=sorted(ACCOUNTS), required=True)
    parser.add_argument("--account")
    parser.add_argument("--images", nargs="+", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--tags", default="")
    parser.add_argument("--schedule")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--headed", action="store_true")
    mode.add_argument("--headless", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    images = [Path(image).expanduser() for image in args.images]
    missing = [str(image) for image in images if not image.is_file()]
    if missing:
        raise SystemExit("missing images:\n" + "\n".join(missing))

    account = args.account or ACCOUNTS[args.platform]
    cmd = [
        str(SAU),
        args.platform,
        "upload-note",
        "--account",
        account,
        "--images",
        *[str(image) for image in images],
        "--title",
        args.title,
        "--note",
        args.body,
    ]
    if args.tags:
        cmd.extend(["--tags", args.tags])
    if args.schedule:
        cmd.extend(["--schedule", args.schedule])
    if args.headed:
        cmd.append("--headed")
    else:
        cmd.append("--headless")

    return subprocess.run(cmd, cwd=RUNTIME).returncode


if __name__ == "__main__":
    raise SystemExit(main())
