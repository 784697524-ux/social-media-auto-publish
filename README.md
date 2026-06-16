# social-media-auto-publish

Codex project skill for publishing social media content through the local `social-auto-upload` runtime.

## What It Covers

- Xiaohongshu: login check, image-note publishing, video publishing through `sau`
- Douyin: login check, image-note publishing, video publishing through `sau`
- Kuaishou: login check, image-note publishing, video publishing through `sau`
- Bilibili: login check and video upload through `sau`
- 视频号: login, card-image to video conversion, and publish through direct Tencent uploader scripts

## Layout

```text
social-media-auto-publish/
  SKILL.md
  bin/sau
  scripts/
  skills/
  references/
  patches/
```

Runtime state is intentionally excluded from this package:

- cookies
- logs
- QR-code screenshots
- browser profiles
- virtual environments

## Runtime

Default runtime path:

```text
$HOME/.openclaw/workspace/social-auto-upload
```

Override it when needed:

```bash
export SOCIAL_AUTO_UPLOAD_HOME="/path/to/social-auto-upload"
```

The runtime must expose:

```text
$SOCIAL_AUTO_UPLOAD_HOME/.venv/bin/sau
```

## Install For Codex

From this repository:

```bash
./install.sh
```

This copies the skill package into:

```text
~/.codex/skills/social-media-auto-publish
```

For a full Chinese walkthrough, read [USAGE.md](USAGE.md).

## Smoke Checks

```bash
./bin/sau xiaohongshu check --account <xiaohongshu_account>
./bin/sau douyin check --account <douyin_account>
```

## Publish Image Notes

```bash
python scripts/publish_note.py \
  --platform xiaohongshu \
  --images /path/to/01.png /path/to/02.png \
  --title "标题" \
  --body "正文" \
  --tags "AI运营,个人IP"
```

## Publish 视频号 From Image Cards

```bash
python scripts/make_card_video.py \
  --images /path/to/01.png /path/to/02.png \
  --output /path/to/videohao.mp4

python scripts/publish_videohao.py \
  --video /path/to/videohao.mp4 \
  --title "标题" \
  --desc "简介" \
  --tags "AI运营,个人IP"
```

## Important Limits

- Xiaohongshu image-note body should stay under 1000 characters.
- Do not use interaction-bait wording such as asking users to comment, reply with keywords, follow, like, collect, or DM to receive resources.
- For 视频号, confirm the cover dialog before publishing; see `patches/tencent-cover-confirm.patch`.
