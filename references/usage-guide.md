# 社媒自动发布技能使用教程

## 1. 技能定位

`social-media-auto-publish` 是给 Codex 使用的项目级社媒发布技能。它不保存账号密码，不保存 cookie，只负责把已经准备好的标题、正文、图片或视频交给本机 `social-auto-upload` runtime 发布。

支持平台：

| 平台 | 图文 | 视频 | 入口 |
| --- | --- | --- | --- |
| 小红书 | 支持 | 支持 | `sau xiaohongshu ...` |
| 抖音 | 支持 | 支持 | `sau douyin ...` |
| 快手 | 支持 | 支持 | `sau kuaishou ...` |
| Bilibili | 不适用 | 支持 | `sau bilibili ...` |
| 视频号 | 图片转视频 | 支持 | `scripts/publish_videohao.py` |

## 2. 安装方式

默认安装到 Codex 技能目录：

```bash
cd /path/to/social-media-auto-publish
./install.sh
```

安装后位置：

```text
~/.codex/skills/social-media-auto-publish
```

## 3. Runtime 路径

默认 runtime：

```text
$HOME/.openclaw/workspace/social-auto-upload
```

如果 runtime 换了位置，先设置环境变量：

```bash
export SOCIAL_AUTO_UPLOAD_HOME="/path/to/social-auto-upload"
```

技能会调用：

```text
$SOCIAL_AUTO_UPLOAD_HOME/.venv/bin/sau
```

## 4. 账号名称

| 平台 | account |
| --- | --- |
| 小红书 | `<xiaohongshu_account>` |
| 抖音 | `<douyin_account>` |
| 快手 | `<kuaishou_account>` |
| Bilibili | `<bilibili_account>` |
| 视频号 | `cookies/tencent_uploader/account.json` |

## 5. 发布前检查

每次发布前先检查登录状态：

```bash
./bin/sau xiaohongshu check --account <xiaohongshu_account>
./bin/sau douyin check --account <douyin_account>
./bin/sau kuaishou check --account <kuaishou_account>
```

返回 `valid` 才继续发布。返回 `invalid` 时先登录：

```bash
./bin/sau xiaohongshu login --account <xiaohongshu_account>
```

如果命令生成二维码图片，Codex 要直接展示图片给用户扫码。

## 6. 小红书图文发布

小红书正文最多 1000 字。不要写诱导互动表达，例如：

- 评论关键词
- 回复领取
- 关注后发送
- 点赞收藏后获取
- 私信领取资料

发布命令：

```bash
python scripts/publish_note.py \
  --platform xiaohongshu \
  --images /path/to/01.png /path/to/02.png \
  --title "运营人别只追AI工具了" \
  --body "1000字以内正文" \
  --tags "AI运营,个人IP,自媒体运营"
```

成功信号：

```text
图文发布成功
```

## 7. 抖音 / 快手图文发布

```bash
python scripts/publish_note.py \
  --platform douyin \
  --images /path/to/01.png /path/to/02.png \
  --title "标题" \
  --body "正文" \
  --tags "AI运营,个人IP"
```

快手把 `--platform douyin` 改成 `--platform kuaishou`。

## 8. 视频号发布

视频号当前不走 `sau` 子命令，使用本技能的 direct scripts。

先把图片卡片转成竖屏 H.264 视频：

```bash
python scripts/make_card_video.py \
  --images /path/to/01.png /path/to/02.png \
  --output /path/to/videohao.mp4
```

再发布：

```bash
python scripts/publish_videohao.py \
  --video /path/to/videohao.mp4 \
  --title "标题" \
  --desc "简介" \
  --tags "AI运营,个人IP"
```

视频号发布时如出现封面编辑弹窗，需要确认后才能点发表；补丁记录在：

```text
patches/tencent-cover-confirm.patch
```

## 9. 常见问题

| 问题 | 原因 | 处理 |
| --- | --- | --- |
| 小红书点发布没反应 | 正文超过 1000 字 | 压缩正文，长内容放到图片卡片 |
| 笔记审核不通过 | 有诱导互动表达 | 删除评论、领取、私信、关注等 CTA |
| cookie invalid | 登录过期 | 重新执行 login 并扫码 |
| 视频号卡在封面 | 封面弹窗未确认 | 应用补丁或使用已修复 runtime |
| 找不到 sau | runtime 路径不一致 | 设置 `SOCIAL_AUTO_UPLOAD_HOME` |

## 10. Codex 执行原则

1. 先读 `SKILL.md` 和对应平台子技能。
2. 先查 cookie，再发布。
3. 不把 cookie、日志、二维码提交到 Git。
4. 不用浏览器手工流程替代 CLI，除非平台要求扫码或确认弹窗。
5. 发布失败时先看平台提示，不要重复点击导致重复发布。
