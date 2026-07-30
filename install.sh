#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
target_dir="${CODEX_HOME:-$HOME/.codex}/skills/social-media-auto-publish"

mkdir -p "$(dirname "$target_dir")"
target_dir="$(cd "$(dirname "$target_dir")" && pwd -P)/$(basename "$target_dir")"

if [[ -d "$target_dir" ]] && [[ "$source_dir" == "$(cd "$target_dir" && pwd -P)" ]]; then
  echo "Already installed at: $target_dir"
  exit 0
fi

rm -rf "$target_dir"
rsync -a --exclude '.git' --exclude '.DS_Store' "$source_dir/" "$target_dir/"

echo "Installed social-media-auto-publish skill to: $target_dir"
