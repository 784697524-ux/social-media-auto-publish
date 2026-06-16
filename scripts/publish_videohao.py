#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

RUNTIME = Path(os.environ.get("SOCIAL_AUTO_UPLOAD_HOME", Path.home() / ".openclaw/workspace/social-auto-upload"))
sys.path.insert(0, str(RUNTIME))

from conf import BASE_DIR
from uploader.tencent_uploader.main import TENCENT_PUBLISH_STRATEGY_IMMEDIATE
from uploader.tencent_uploader.main import TencentVideo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a video to WeChat Channels / 视频号.")
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--desc", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--thumbnail")
    parser.add_argument("--short-title", default="")
    parser.add_argument("--draft", action="store_true")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    video = Path(args.video).expanduser()
    if not video.is_file():
        raise SystemExit(f"missing video: {video}")

    thumbnail = Path(args.thumbnail).expanduser() if args.thumbnail else None
    if thumbnail and not thumbnail.is_file():
        raise SystemExit(f"missing thumbnail: {thumbnail}")

    account_file = Path(BASE_DIR) / "cookies" / "tencent_uploader" / "account.json"
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    app = TencentVideo(
        title=args.title,
        file_path=str(video),
        tags=tags,
        publish_strategy=TENCENT_PUBLISH_STRATEGY_IMMEDIATE,
        publish_date=0,
        account_file=str(account_file),
        desc=args.desc,
        thumbnail_path=str(thumbnail) if thumbnail else None,
        short_title=args.short_title or args.title[:16],
        category=None,
        is_draft=args.draft,
        headless=False,
    )
    await app.tencent_upload_video()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
