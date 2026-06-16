#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a vertical H.264 video from image cards.")
    parser.add_argument("--images", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seconds-per-slide", type=int, default=4)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=30)
    return parser.parse_args()


def read_image(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"failed to read image: {path}")
    return image


def main() -> int:
    args = parse_args()
    images = [Path(image).expanduser() for image in args.images]
    missing = [str(image) for image in images if not image.is_file()]
    if missing:
        raise SystemExit("missing images:\n" + "\n".join(missing))

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    frame_dir = output.parent / f"{output.stem}_frames"
    frame_dir.mkdir(parents=True, exist_ok=True)

    for index, path in enumerate(images, 1):
        image = read_image(path)
        image_height, image_width = image.shape[:2]
        scale = min(args.width / image_width, args.height / image_height)
        resized_width = int(image_width * scale)
        resized_height = int(image_height * scale)
        resized = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
        canvas = np.full((args.height, args.width, 3), 245, dtype=np.uint8)
        y = (args.height - resized_height) // 2
        x = (args.width - resized_width) // 2
        canvas[y : y + resized_height, x : x + resized_width] = resized
        cv2.imwrite(str(frame_dir / f"frame{index:02d}.png"), canvas)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    duration = len(images) * args.seconds_per_slide
    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        f"1/{args.seconds_per_slide}",
        "-i",
        str(frame_dir / "frame%02d.png"),
        "-t",
        str(duration),
        "-r",
        str(args.fps),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "22",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(cmd, check=True)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
