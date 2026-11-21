# social-media-auto-publish

面向 Codex 的社媒自动发布技能包。它只提交已经获准的成片和文案；不生成、裁切、加字幕、替换音轨或修改视频文件，也不保存账号密码、Cookie、二维码、浏览器 Profile 或发布回执。

## 当前发布入口

| 平台 | 首选入口 | 交付边界 |
| --- | --- | --- |
| 抖音本地生活 / 挂位置 | `publish-batch` | 一条作品一个清单项；核账号、AI 声明、竖封面、国内 POI 和新作品回执；可导出短视频链接。 |
| 小红书视频笔记 | `social` | 清单式提交，核本人创作端昵称、文案、话题、AI 声明和默认封面。 |
| 微信视频号 | `social` | 清单式提交，核视频号 ID；正文必须披露 AI 生成，并处理“直接发表”确认。 |
| 快手视频 | `social` | 清单式提交，核创作端昵称、组合文案和 AI 生成披露。 |
| B 站视频 | `social` | 清单式提交，核数字 UID、分区、标签和 AI 声明；短信验证须由账号所有者完成。 |
| 优兔（YouTube） | `sau youtube` | runtime 原生单视频入口；不属于当前 `social` 清单适配器的实发范围。 |

完整命令、清单模板、登录和回执语义见 [最新 CLI 指南](references/latest-cli.md)。

## 抖音自动挂位置

抖音的国内 POI 是**位置标签**，不等于绑定可购买的团购商品；一条清单只能使用 `location` 或 `product`，不能同时填写。现行位置发布使用 `publish-batch`：

```bash
bin/yingxu-publish publish -- publish-batch \
  --manifest /absolute/path/douyin-poi.json \
  --state-dir /absolute/path/douyin-poi-state \
  --account <本地账号别名> \
  --expected-account <创作者主页显示的抖音号>
```

该命令会在同一浏览器会话中选择“添加标签 → 位置 → 带货模式 → 国内”，检索完整商场/门店 POI、读回选择结果，并在一次发布点击后核对新作品回执。重跑相同清单和状态目录会跳过已核验提交；结果不明时停止，不换目录重传。

`sau douyin upload-video --location ...` 和本仓库的 patch 保留给旧调用方；不要把它当作新的批量回执入口。详见 [抖音 POI 与团购商品](references/latest-cli.md#抖音-poi-与团购商品)。

## 安装与运行环境

当前映序发布环境默认使用：

```text
$HOME/.briefrun/publisher/runtime
```

可用 `SOCIAL_AUTO_UPLOAD_HOME` 指向账号所有者自己的独立 runtime。运行环境与账号授权按映序的可移植安装流程准备；仓库不应复制其他人的浏览器数据。

旧版 `social-auto-upload` runtime 的默认路径 `$HOME/.openclaw/workspace/social-auto-upload` 仍可通过 `SOCIAL_AUTO_UPLOAD_HOME` 显式指定，但它没有自动获得新的 `social` 和 `publish-batch` 契约。

本仓库用 `bin/yingxu-publish` 转交已安装的映序 `briefrun-director` 发布 CLI。默认查找 `~/.codex/skills/briefrun-director`；非默认安装位置设置 `BRIEFRUN_DIRECTOR_HOME`，已验证的 Python 解释器设置 `BRIEFRUN_PYTHON`。

## 安全发布原则

- 只有已明确指定作品、目标平台、账号和本次发布授权时才上传。
- 发布前若结果不明，先读本地状态/回执和平台作品列表，绝不靠再次上传“试一下”。
- `--dry-run` 只做离线校验；`--prepare-only` 只填写编辑器，都不代表已发布。
- 发布回执证明提交，不证明审核通过、公开可见、播放正常或团购可购买；这些是独立核验项。
- 平台登录、短信和验证码由账号所有者在自己的浏览器完成。

## 仓库结构

```text
social-media-auto-publish/
  SKILL.md
  references/latest-cli.md
  skills/
  scripts/
  patches/                 # 仅旧版 sau 的兼容补丁
```

保留 [USAGE.md](USAGE.md) 作为旧版 `sau` 兼容说明；新项目请以 [最新 CLI 指南](references/latest-cli.md) 为准。
