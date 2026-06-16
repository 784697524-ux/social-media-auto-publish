---
name: social-media-auto-publish
description: Use this project-local skill when Codex needs to publish content from this project to Xiaohongshu, Douyin, Kuaishou, Bilibili, or WeChat Channels/视频号 through the local social-auto-upload tooling.
---

# Social Media Auto Publish

Use this skill first for social publishing tasks in this project.

## Local Runtime

- Project skill bundle: `/path/to/social-media-auto-publish`
- Runtime repo: `${SOCIAL_AUTO_UPLOAD_HOME:-$HOME/.openclaw/workspace/social-auto-upload}`
- CLI: `${SOCIAL_AUTO_UPLOAD_HOME:-$HOME/.openclaw/workspace/social-auto-upload}/.venv/bin/sau`
- Local wrapper: `/path/to/social-media-auto-publish/bin/sau`
- Cookies: runtime `cookies/`
- Logs: runtime `logs/`

Do not copy cookies, QR codes, or logs into this project folder.

Set `SOCIAL_AUTO_UPLOAD_HOME` first if the runtime is not in the default path.

## Platform Accounts

- Xiaohongshu: `<xiaohongshu_account>`
- Douyin: `<douyin_account>`
- Kuaishou: `<kuaishou_account>`
- Bilibili: `<bilibili_account>`
- 视频号: `$HOME/.openclaw/workspace/social-auto-upload/cookies/tencent_uploader/account.json`

## Workflow

1. For Xiaohongshu, Douyin, Kuaishou, and Bilibili, use the matching sub-skill under `skills/`.
2. Prefer `bin/sau` or the absolute `sau` path above.
3. Check cookies before publishing. If invalid, run the platform login command and display the QR image directly.
4. Publish only after local file paths, title, body, tags, and platform account are clear.
5. For 视频号, use `scripts/videohao_login.py`, `scripts/make_card_video.py`, and `scripts/publish_videohao.py`.

## Common Commands

```bash
/path/to/social-media-auto-publish/bin/sau xiaohongshu check --account <xiaohongshu_account>
/path/to/social-media-auto-publish/bin/sau douyin check --account <douyin_account>
```

Generic note publishing:

```bash
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/python \
  /path/to/social-media-auto-publish/scripts/publish_note.py \
  --platform douyin \
  --images /path/to/01.png /path/to/02.png \
  --title "标题" \
  --body "正文" \
  --tags "AI运营,个人IP"
```

视频号 card-to-video publishing:

```bash
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/python \
  /path/to/social-media-auto-publish/scripts/make_card_video.py \
  --images /path/to/01.png /path/to/02.png \
  --output /path/to/videohao.mp4

$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/python \
  /path/to/social-media-auto-publish/scripts/publish_videohao.py \
  --video /path/to/videohao.mp4 \
  --title "标题" \
  --desc "简介" \
  --tags "AI运营,个人IP"
```

## References

- Local install notes: `references/local-install.md`
- Usage guide: `references/usage-guide.md`
- Platform accounts: `references/platform-accounts.md`
- 视频号 notes: `references/videohao.md`
- Platform sub-skills:
  - `skills/xiaohongshu-upload/SKILL.md`
  - `skills/douyin-upload/SKILL.md`
  - `skills/kuaishou-upload/SKILL.md`
  - `skills/bilibili-upload/SKILL.md`
