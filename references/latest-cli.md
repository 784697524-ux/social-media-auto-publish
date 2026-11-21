# 最新自媒体自动发布 CLI

本页是当前映序发布规范在独立仓库中的命令索引。下面的 `<...>` 都是占位符；用账号所有者自己的运行环境、登录身份和已获准素材替换。命令前的 `plan`、`status`、`--dry-run` 都不会投稿，只有明确带 `submit --execute` 或未带这两个保护参数的正式 `publish-batch` 才会进入发布流程。

## 运行环境

当前发布 runtime 的默认目录是：

```text
$HOME/.briefrun/publisher/runtime
```

通过 `SOCIAL_AUTO_UPLOAD_HOME` 可指定本人独立目录。映序 v0.4.21 的统一入口由本仓库的 `bin/yingxu-publish` 转交；它默认查找 `~/.codex/skills/briefrun-director`，非默认位置设置 `BRIEFRUN_DIRECTOR_HOME`，已验证的 Python 解释器设置 `BRIEFRUN_PYTHON`。本仓库不携带账号、Cookie、浏览器 Profile、视频源文件或发布状态。

旧仓库里的 `bin/sau` 和 `scripts/apply_douyin_groupbuy_patch.sh` 仅服务旧的 `social-auto-upload` runtime。它们不会把该 runtime 升级成新的 `social` 或 `publish-batch` 接口。

## 抖音 POI 与团购商品

### 国内 POI 位置

创建私有 `douyin-poi.json`。`location` 要给完整商场/门店 POI，`source_sha256` 固定最终获准的原片。`cover` 为竖封面。

```json
{
  "items": [{
    "id": "mall-video-01",
    "file": "/absolute/path/approved.mp4",
    "source_sha256": "替换为最终原片的64位SHA-256",
    "cover": "/absolute/path/cover.png",
    "title": "核准标题",
    "desc": "核准正文",
    "tags": ["本地生活", "逛吃卡"],
    "location": "合肥滨湖银泰百货",
    "exclude_aweme_ids": []
  }]
}
```

只做离线校验：

```bash
bin/yingxu-publish publish -- publish-batch \
  --manifest /absolute/path/douyin-poi.json --state-dir /absolute/path/douyin-poi-state \
  --account <本地Profile别名> --expected-account <实际抖音号> --dry-run
```

已获发布授权时，去掉 `--dry-run`，其余参数及同一 `--state-dir` 不变：

```bash
bin/yingxu-publish publish -- publish-batch \
  --manifest /absolute/path/douyin-poi.json --state-dir /absolute/path/douyin-poi-state \
  --account <本地Profile别名> --expected-account <实际抖音号>
```

流程在同一个 Chrome 会话中执行“添加标签 → 位置 → 带货模式 → 国内”，搜索并选择 POI，读回位置、封面、标题和 AI 声明；发布按钮只点击一次，随后从新作品列表取得匹配回执。`location` 只是位置标签，**不证明已挂上可购买团购券**。

### 指定团购商品

挂券时每条只填 `product`，不填 `location`：

```json
{
  "items": [{
    "id": "product-video-01",
    "file": "/absolute/path/approved.mp4",
    "source_sha256": "替换为最终原片的64位SHA-256",
    "cover": "/absolute/path/cover.png",
    "title": "核准标题",
    "desc": "核准正文",
    "tags": ["本地生活"],
    "product": {
      "id": "1234567890123456789",
      "title": "创作端选择器显示的商品全名",
      "search": "检索商品的关键词",
      "price": "16.5",
      "stores": 32,
      "promotion_title": "16.5元衣鞋普洗"
    }
  }]
}
```

使用同一条 `publish-batch` 命令。账号、完整商品名、价格和门店数会在提交前读回。找不到唯一精确商品 ID、账号不匹配或已有不明提交时，流程会在点击前停下。

已有已登录 Chrome 时，只有用户明确要求复用才追加 `--reuse-browser`；已有绑定会话时再加 `--chrome-session <session>`。`collect-results` 只导出现有状态中的已核作品链接，不打开浏览器、不重新投稿：

```bash
bin/yingxu-publish publish -- collect-results \
  --manifest /absolute/path/douyin-poi.json --state-dir /absolute/path/douyin-poi-state \
  --account <本地Profile别名> --expected-account <实际抖音号>
```

## 小红书、视频号、快手和 B 站

这四个平台使用一个作品一个私有 JSON 清单。例子：

```json
{
  "platform": "xiaohongshu",
  "account": "my_creator",
  "expected_account": "本人创作端显示名称",
  "file": "./approved.mp4",
  "sha256": "替换为最终原片的64位SHA-256",
  "title": "核准标题",
  "description": "核准正文。本视频由AI生成。",
  "tags": ["核准话题"],
  "ai_generated": true
}
```

```bash
bin/yingxu-publish social -- plan --manifest /absolute/path/job.json
bin/yingxu-publish social -- submit --manifest /absolute/path/job.json --execute
bin/yingxu-publish social -- status --manifest /absolute/path/job.json
```

- `platform` 可为 `xiaohongshu`、`tencent`（视频号）、`kuaishou` 或 `bilibili`。
- B站额外给 `category`，`expected_account` 必须是本人数字 UID，并至少给一个标签。
- 视频号与快手要求 `description` 明确包含“本视频由 AI 生成”等披露。
- 该内测入口支持 AI 单视频和默认封面；不支持定时、批量、POI、购买链接或自定义封面。未支持字段会直接停止。

同一平台、本人账号和视频 SHA-256 会复用同一个提交记录。若过程曾开始点击、回执不明或需要短信验证，先用 `status` 和平台作品列表核对；不要改账号别名、换状态目录或重新上传。

## 优兔（YouTube）

优兔目前使用 runtime 的 `sau` 单视频入口，不属于上方 `social` 清单适配器。先由账号所有者完成登录或账号检查：

```bash
bin/sau youtube login --account <youtube_account> --headed
bin/sau youtube check --account <youtube_account>
```

再提交视频：

```bash
bin/sau youtube upload-video \
  --account <youtube_account> \
  --file /absolute/path/approved.mp4 \
  --title "核准标题（100字符内）" \
  --desc "核准简介" \
  --tags "tag1,tag2" \
  --thumbnail /absolute/path/cover.png \
  --playlist "可选播放列表" \
  --visibility public \
  --headed
```

`--visibility` 可选 `public`、`unlisted` 或 `private`。优兔 runtime 命令可用不代表已经获得与 `social` 四平台同等级的本机实发证据；提交、审核和公开播放仍需分别核验。

## 旧版 sau 兼容命令

旧 runtime 继续提供小红书、快手、B站、视频号和优兔的直接命令，例如：

```bash
bin/sau xiaohongshu upload-video --account <account> --file /absolute/path/approved.mp4 --title "标题" --desc "正文" --tags "话题1,话题2" --headed
bin/sau tencent upload-video --account <account> --file /absolute/path/approved.mp4 --title "标题" --desc "正文。本视频由AI生成。" --tags "话题1" --headed
bin/sau kuaishou upload-video --account <account> --file /absolute/path/approved.mp4 --title "标题" --desc "正文。本视频由AI生成。" --tags "话题1" --headed
bin/sau bilibili upload-video --account <account> --file /absolute/path/approved.mp4 --title "标题" --desc "正文" --tid <分区ID> --tags "话题1,话题2"
```

抖音旧版位置兼容命令如下；新任务优先使用上方的 `publish-batch`：

```bash
bin/sau douyin upload-video \
  --account <account> --file /absolute/path/approved.mp4 \
  --title "标题" --desc "正文" --tags "本地生活,商场" \
  --location "合肥滨湖银泰百货" --headed
```

它会尝试选择国内 POI，但不具备现行批量入口的完整状态、账户精确核验、新作品回执和链接导出机制。
