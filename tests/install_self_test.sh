#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
sandbox="$(mktemp -d "${TMPDIR:-/tmp}/social-media-auto-publish-install.XXXXXX")"
trap 'rm -rf "$sandbox"' EXIT

export CODEX_HOME="$sandbox/codex"
"$repo_dir/install.sh"

target="$CODEX_HOME/skills/social-media-auto-publish"
test -f "$target/SKILL.md"
touch "$target/.self-install-marker"

"$target/install.sh"

test -f "$target/.self-install-marker"
test -f "$target/SKILL.md"
