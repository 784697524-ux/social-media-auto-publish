---
name: social-media-auto-publish
description: 使用当前映序发布 CLI 将已获授权的成片发布至抖音、小红书、视频号、快手、B站或优兔；抖音本地生活位置走可回执、可续跑的 publish-batch。
---

# 社媒自动发布

只在用户明确给出本次作品、目标平台、目标账号和发布授权时执行。规划、做封面、生成视频、查询能力或准备清单都不上传、不登录、不投稿。

## 路由选择

| 目的 | 当前入口 |
| --- | --- |
| 抖音国内 POI / 本地生活视频 | `publish publish-batch`，单项或多项清单。 |
| 抖音指定团购商品 | 同一 `publish-batch`，清单只填写 `product`，不能同时填写 `location`。 |
| 小红书、视频号、快手、B站的 AI 单视频 | `social plan/submit/status`，一条作品一个私有 JSON 清单。 |
| 优兔单视频 | `sau youtube login/check/upload-video`；不冒充为 `social` 清单已覆盖平台。 |

不要用旧的 `sau douyin upload-video --location` 开始新抖音位置任务；它只作为兼容入口，缺少 `publish-batch` 的单次点击回执、断点续跑和结果导出。

## 抖音 POI 发布

清单中的 `location` 是完整的国内商场/门店 POI。它是位置标签，不是可购买的团购商品。每个条目必须有真实视频、竖封面、标题、正文、话题和本次获准的素材哈希。

```bash
bin/yingxu-publish publish -- publish-batch \
  --manifest /absolute/path/batch.json --state-dir /absolute/path/publish-state \
  --account <本地Profile别名> --expected-account <实际抖音号>
```

`--dry-run` 仅本地校验；`--prepare-only` 停在已填写编辑器，均不点击发布。收到发布授权后去掉二者并沿用相同清单和状态目录。已登录的本人 Chrome 仅在用户要求复用时添加 `--reuse-browser`；已有明确 OpenCLI 会话时再添加 `--chrome-session <session>`。

提交后立即读取新作品回执。`submitted` 只表示作品提交已核验；审核、公开播放和团购购买卡分别报告。`submission_uncertain` 或 `submitted_unverified` 时停止，先核本地状态和作品列表，绝不重传或再点一次发布。

## 四平台清单发布

私有清单示例：

```json
{
  "platform": "xiaohongshu",
  "account": "my_creator",
  "expected_account": "本人创作端显示名称",
  "file": "./approved.mp4",
  "sha256": "替换为最终获准原片的64位SHA-256",
  "title": "核准标题",
  "description": "核准正文。本视频由AI生成。",
  "tags": ["核准话题"],
  "ai_generated": true
}
```

```bash
bin/yingxu-publish social -- plan --manifest job.json
bin/yingxu-publish social -- submit --manifest job.json --execute
bin/yingxu-publish social -- status --manifest job.json
```

小红书、视频号、快手与B站使用各自账号；B站需要数字 UID、准确分区和标签。视频号、快手的正文须披露 AI 生成。默认封面是此路线的限制：不要悄悄塞入自定义封面、定时、POI 或额外声明参数。

## 账号与运行边界

- 当前 runtime：`${SOCIAL_AUTO_UPLOAD_HOME:-$HOME/.briefrun/publisher/runtime}`；`bin/yingxu-publish` 默认转交 `~/.codex/skills/briefrun-director`，可用 `BRIEFRUN_DIRECTOR_HOME` 覆盖。
- 使用账号所有者自己的运行环境、浏览器和授权；不复制 Cookie、二维码、Profile、日志或发布状态至仓库。
- 不在每次抖音发布前另跑 `check`；`publish-batch` 会在同一浏览器会话核账号。`check` 仅用于明确要求的账号诊断。
- 短信、验证码、扫码和平台风险校验须由账号所有者完成。
- 发布适配器不会编辑视频。若素材需要字幕、配音、裁切、封面或换音，先取得相应授权并在发布前准备好文件。

完整命令、兼容命令和优兔说明见 `references/latest-cli.md`。
