# Platform Accounts

Use these account names with `sau`.

| Platform | Command name | Account |
| --- | --- | --- |
| 小红书 | `xiaohongshu` | `<xiaohongshu_account>` |
| 抖音 | `douyin` | `<douyin_account>` |
| 快手 | `kuaishou` | `<kuaishou_account>` |
| Bilibili | `bilibili` | `<bilibili_account>` |

视频号 is not exposed by the current `sau` command. Use the direct Tencent uploader scripts in this skill bundle.

视频号 account file:

```text
$HOME/.openclaw/workspace/social-auto-upload/cookies/tencent_uploader/account.json
```

Login command:

```bash
$HOME/.openclaw/workspace/social-auto-upload/.venv/bin/python \
  /path/to/social-media-auto-publish/scripts/videohao_login.py
```
