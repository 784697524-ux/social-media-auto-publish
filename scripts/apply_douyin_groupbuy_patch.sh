#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime="${SOCIAL_AUTO_UPLOAD_HOME:-$HOME/.openclaw/workspace/social-auto-upload}"
patch_file="$repo_dir/patches/douyin-groupbuy-location.patch"

if [ ! -d "$runtime/.git" ]; then
  echo "runtime is not a git checkout: $runtime" >&2
  exit 1
fi

if [ ! -f "$patch_file" ]; then
  echo "missing patch: $patch_file" >&2
  exit 1
fi

if git -C "$runtime" apply --reverse --check "$patch_file" >/dev/null 2>&1; then
  echo "douyin group-buy patch already applied: $runtime"
else
  git -C "$runtime" apply --check "$patch_file"
  git -C "$runtime" apply "$patch_file"
  echo "applied douyin group-buy patch: $runtime"
fi

pushd "$runtime" >/dev/null
"$runtime/.venv/bin/python" -m py_compile sau_cli.py uploader/douyin_uploader/main.py
"$runtime/.venv/bin/python" -m unittest \
  tests.test_sau_browser_cli.BrowserCliParserTests.test_douyin_upload_video_accepts_location \
  tests.test_sau_browser_cli.BrowserCliDispatchTests.test_dispatch_douyin_upload_video_uses_dual_thumbnail_request_fields
popd >/dev/null

echo "douyin group-buy CLI is ready. Use: sau douyin upload-video ... --location \"合肥滨湖银泰百货\" --headed"
