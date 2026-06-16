#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_dir="${CODEX_HOME:-$HOME/.codex}/skills/social-media-auto-publish"

mkdir -p "$(dirname "$target_dir")"
rm -rf "$target_dir"
rsync -a --exclude '.git' --exclude '.DS_Store' "$source_dir/" "$target_dir/"

echo "Installed social-media-auto-publish skill to: $target_dir"
