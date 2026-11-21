# Local Install Notes（旧版 sau runtime）

> 当前映序 `publish-batch` / `social` 命令由根目录的 `bin/yingxu-publish` 转交已安装的 `briefrun-director`。本页只适用于保留的旧 `sau` 兼容入口。

This project keeps only the Codex-facing skill bundle. The full runtime remains in:

```text
$HOME/.openclaw/workspace/social-auto-upload
```

Why not copy the full runtime here:

- The runtime is large because it includes browser dependencies.
- Cookies and logs are runtime state and should not be copied into project files.
- The verified executable already exists at:

```text
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/sau
```

If `sau` is missing, reinstall from the runtime repo:

```bash
cd $HOME/.openclaw/workspace/social-auto-upload
uv pip install -e .
```

Useful checks:

```bash
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/sau --help
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/sau xiaohongshu check --account <xiaohongshu_account>
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/sau douyin check --account <douyin_account>
```

If the runtime moves, set:

```bash
export SOCIAL_AUTO_UPLOAD_HOME="/path/to/social-auto-upload"
```

Install this skill into Codex:

```bash
cd /path/to/social-media-auto-publish
./install.sh
```

Do not store QR codes, cookie JSON, or log files in this project folder.
