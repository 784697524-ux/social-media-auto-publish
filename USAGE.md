# social-media-auto-publish 使用教程

这是一个给 Codex 使用的社媒自动发布技能包。它负责把已准备好的标题、正文、图片、视频交给本机 `social-auto-upload` runtime 发布。

它不包含账号密码、cookie、二维码、日志、浏览器配置或虚拟环境。使用者需要在自己的电脑上完成 runtime 安装和平台登录。

## 1. 支持平台

| 平台 | 图文 | 视频 | 入口 |
| --- | --- | --- | --- |
| 小红书 | 支持 | 支持 | `sau xiaohongshu ...` |
| 抖音 | 支持 | 支持 | `sau douyin ...` |
| 快手 | 支持 | 支持 | `sau kuaishou ...` |
| Bilibili | 不适用 | 支持 | `sau bilibili ...` |
| 视频号 | 图片转视频 | 支持 | `scripts/publish_videohao.py` |

## 2. 前置依赖

先准备 `social-auto-upload` runtime，并确保下面的命令可用：

```bash
$SOCIAL_AUTO_UPLOAD_HOME/.venv/bin/sau --help
```

如果 runtime 放在默认位置，可以不设置环境变量：

```text
$HOME/.openclaw/workspace/social-auto-upload
```

如果 runtime 在其他位置，先设置：

```bash
export SOCIAL_AUTO_UPLOAD_HOME="/path/to/social-auto-upload"
```

## 3. 安装到 Codex

克隆仓库后执行：

```bash
cd social-media-auto-publish
./install.sh
```

安装后会复制到：

```text
~/.codex/skills/social-media-auto-publish
```

后续 Codex 看到社媒发布任务时，就可以使用这个技能。

## 4. 登录检查

发布前先检查平台登录状态：

```bash
./bin/sau xiaohongshu check --account <xiaohongshu_account>
./bin/sau douyin check --account <douyin_account>
./bin/sau kuaishou check --account <kuaishou_account>
./bin/sau bilibili check --account <bilibili_account>
```

返回 `valid` 再发布。返回 `invalid` 时重新登录：

```bash
./bin/sau xiaohongshu login --account <xiaohongshu_account>
```

登录过程中如生成二维码，需要由当前账号使用者自行扫码。

## 5. 发布图文

小红书、抖音、快手共用 `scripts/publish_note.py`：

```bash
python scripts/publish_note.py \
  --platform xiaohongshu \
  --account <xiaohongshu_account> \
  --images /path/to/01.png /path/to/02.png \
  --title "标题" \
  --body "正文" \
  --tags "AI运营,个人IP"
```

`--platform` 可选：

```text
xiaohongshu
douyin
kuaishou
```

小红书图文正文建议控制在 1000 字以内。不要写“评论关键词”“关注后领取”“私信领取”“点赞收藏后获取”等诱导互动表达。

## 6. 抖音本地团购视频发布

本仓库提供一个 runtime patch，用于给 `sau douyin upload-video` 增加团购版位置发布能力：

```bash
./scripts/apply_douyin_groupbuy_patch.sh
```

应用后，视频发布命令可以增加 `--location`：

```bash
./bin/sau douyin upload-video \
  --account <douyin_account> \
  --file /path/to/video.mp4 \
  --title "合肥滨湖银泰119双人逛吃卡，真的别划走" \
  --desc "别人突然加你好友，说能给你打折。合肥滨湖银泰119双人逛吃卡，电影+餐饮+体验课，周末直接安排。" \
  --tags "合肥探店,合肥团购,合肥本地生活,滨湖银泰,逛吃卡" \
  --location "合肥滨湖银泰百货" \
  --headed
```

CLI 会按抖音发布页的团购路径执行：

1. 在 `添加标签` 行选择 `位置`
2. 第二个下拉选择 `带货模式`
3. 打开地理位置输入框
4. 切换到 `国内`
5. 搜索 `--location` 指定的 POI
6. 选择包含目标城市地址的候选位置
7. 继续发布

发布前仍然要先检查账号：

```bash
./bin/sau douyin check --account <douyin_account>
```

返回 `valid` 后再发布。首次使用某个账号跑团购位置建议加 `--headed`，方便观察平台弹窗、封面诊断和位置候选，避免重复发布。

## 7. 发布视频号

视频号使用 direct scripts。先把图片卡片转成竖屏视频：

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

如果视频号出现封面编辑弹窗，需要先确认封面，再点发表。相关修复记录见：

```text
patches/tencent-cover-confirm.patch
```

## 8. 隐私边界

可以提交到 Git 的内容：

- `SKILL.md`
- `README.md`
- `USAGE.md`
- `bin/`
- `scripts/`
- `skills/`
- `references/`
- `patches/`

不要提交：

- cookie
- 二维码截图
- 登录态 JSON
- 日志
- 浏览器 profile
- `.venv` / `venv`
- 真实账号密码、token、secret

## 9. 常见问题

| 问题 | 原因 | 处理 |
| --- | --- | --- |
| 找不到 `sau` | runtime 路径不一致 | 设置 `SOCIAL_AUTO_UPLOAD_HOME` |
| cookie invalid | 登录过期 | 重新执行 login 并扫码 |
| 小红书审核不通过 | 有诱导互动表达 | 删除评论、领取、私信、关注等 CTA |
| 小红书点发布没反应 | 正文过长或页面限制 | 压缩正文，长内容做成图片卡片 |
| 视频号卡在封面 | 封面弹窗未确认 | 确认封面后再发表 |
| 抖音位置候选不对 | 未切到国内或浏览器定位偏到外地 | 使用 `--location` 并加 `--headed`，确认候选包含目标城市地址 |
| 抖音重复发布风险 | 用完整发布命令做测试 | 测试时只跑 `check`、`--help`、参数解析和 patch 脚本，不要重复跑完整发布 |

## 10. Codex 使用顺序

1. 先读本目录 `SKILL.md`。
2. 再读对应平台子技能，比如 `skills/xiaohongshu-upload/SKILL.md`。
3. 先执行登录检查。
4. 登录有效后再发布。
5. 失败时先看平台提示和日志，不要重复点击导致重复发布。
