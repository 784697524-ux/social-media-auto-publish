# 视频号 Notes

The current `sau` CLI does not expose a 视频号 command. The runtime repo does include `uploader.tencent_uploader`.

Use these scripts:

- `scripts/videohao_login.py`: login and save cookie.
- `scripts/make_card_video.py`: turn image cards into a vertical H.264 mp4.
- `scripts/publish_videohao.py`: publish the mp4 to 视频号.

Important behavior:

- Use `headless=False` for 视频号 login and publish.
- If the QR code appears, display the generated local QR image directly.
- If image-card content needs to be sent as 视频号 content, turn it into a short vertical video first.
- The runtime source has been patched to confirm the "编辑封面" / "编辑个人主页卡片" dialog before publishing, because the dialog can block the "发表" button.

Verified publish result from this setup:

```text
2026-06-16 10:42:54 视频发布成功
```
