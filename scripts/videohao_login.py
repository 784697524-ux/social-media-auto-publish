#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

RUNTIME = Path(os.environ.get("SOCIAL_AUTO_UPLOAD_HOME", Path.home() / ".openclaw/workspace/social-auto-upload"))
sys.path.insert(0, str(RUNTIME))

from conf import BASE_DIR
from uploader.tencent_uploader.main import tencent_setup


async def main() -> int:
    account_file = Path(BASE_DIR) / "cookies" / "tencent_uploader" / "account.json"
    account_file.parent.mkdir(parents=True, exist_ok=True)
    result = await tencent_setup(str(account_file), handle=True, return_detail=True, headless=False)
    print(result)
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
