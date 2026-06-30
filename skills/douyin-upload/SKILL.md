---
name: douyin-upload
description: 当 agent 需要通过已安装的 `sau` CLI 完成抖音登录、cookie 校验、视频上传或图文发布时使用这个 skill。该 skill 适用于已经安装 `social-auto-upload` 且可调用 `sau` 命令的环境。优先使用这个 skill 进行稳定的命令式抖音工作流，而不是一开始就阅读 uploader 源码。
---

# 抖音上传 Skill

优先把 `sau` 作为主接口。

不要假设当前环境一定能读取仓库源码。
不要一开始就去读 `uploader/`。
只有在命令不可用或 CLI 执行失败时，才回退到故障排查说明。

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| 抖音登录 | `sau douyin login --account <name>` | 生成或刷新指定账号的 cookie |
| cookie 校验 | `sau douyin check --account <name>` | 检查指定账号 cookie 是否有效 |
| 视频上传 | `sau douyin upload-video ...` | 上传并发布抖音视频 |
| 本地团购视频 | `sau douyin upload-video ... --location "<POI>" --headed` | 发布视频并挂国内 POI 位置 |
| 图文上传 | `sau douyin upload-note ...` | 上传并发布抖音图文 |

元数据约定：

- 视频使用 `title + desc + tags`
- 本地团购视频额外使用 `location`，建议传完整 POI 名称
- 图文使用 `title + note + tags`

## 默认工作流

1. 先确认 `references/runtime-requirements.md` 里的运行前提。
2. 再确认 `references/cli-contract.md` 里的命令契约。
3. 执行匹配的 `sau douyin ...` 命令。
4. 如果命令失败，再看 `references/troubleshooting.md`。

## 支持动作

- 使用 `sau douyin login --account <name>` 登录抖音
- 使用 `sau douyin check --account <name>` 校验 cookie 是否有效
- 使用 `sau douyin upload-video ...` 上传抖音视频
- 使用 `sau douyin upload-video ... --location "<POI>"` 发布本地团购视频并挂 POI
- 使用 `sau douyin upload-note ...` 上传抖音图文

## 命令选择建议

- 当用户需要新的 cookie，或现有 cookie 已失效时，使用 `login`
- 当用户只需要确认 cookie 状态时，使用 `check`
- 当用户要发布视频时，使用 `upload-video`
- 当用户要发布本地团购视频、探店视频、挂地理位置或 POI 时，使用 `upload-video --location "<POI>" --headed`
- 当用户要发布图文时，使用 `upload-note`

## 执行前检查

- 先确认当前 shell 里是否可以调用 `sau`
- 如果 `sau` 不可用，按 `references/runtime-requirements.md` 里的回退方式处理
- 当用户明确指定无头或有头模式时，显式传 `--headless` 或 `--headed`
- 只有用户明确要求定时发布时，才使用 `--schedule`
- 本地团购视频首次跑新账号时优先显式传 `--headed`，方便确认平台弹窗、封面诊断和位置候选
- `--location` 要写完整商场/门店 POI，例如 `合肥滨湖银泰百货`
- 如果登录流程生成了本地二维码图片，不要只把图片路径告诉用户
- 二维码图片本身就是给用户扫码的，优先直接把本地图片展示/发送给用户

## 模板文件

当你需要稳定的命令模板时，使用 `scripts/examples/` 下的文件：

- `douyin_commands.ps1`
- `douyin_commands.sh`
- `douyin_cli_template.py`

## 本地团购视频命令模板

```bash
sau douyin upload-video \
  --account <account> \
  --file /path/to/video.mp4 \
  --title "标题" \
  --desc "简介" \
  --tags "合肥探店,合肥团购,合肥本地生活" \
  --location "合肥滨湖银泰百货" \
  --headed
```

执行逻辑：

1. 填标题、简介、话题
2. 等视频上传完成
3. 在 `添加标签` 选择 `位置`
4. 选择 `带货模式`
5. 切到 `国内`
6. 搜索并选择 `--location` 对应 POI
7. 点击发布

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 故障排查：`references/troubleshooting.md`
