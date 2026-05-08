#!/usr/bin/env python3
"""Capture a still image from a USB camera using OpenCV."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def save_frame(frame, output: str) -> None:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), frame):
        raise RuntimeError(f"Failed to save image to {output_path}")
    print(f"Saved image to {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture an image from a Jetson camera.")
    parser.add_argument("--camera", type=int, default=0, help="OpenCV camera index")
    parser.add_argument("--output", default="images/capture.jpg", help="Output image path")
    parser.add_argument("--width", type=int, help="Optional capture width")
    parser.add_argument("--height", type=int, help="Optional capture height")
    parser.add_argument("--warmup-frames", type=int, default=10, help="Frames to discard first")
    parser.add_argument("--no-preview", action="store_true", help="Capture one frame without GUI preview")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    if args.width:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    if args.height:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    try:
        for _ in range(max(args.warmup_frames, 0)):
            cap.read()

        if args.no_preview:
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError("Failed to read frame")
            save_frame(frame, args.output)
            return 0

        print("Press SPACE to capture, ESC to exit")
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame")
                break

            cv2.imshow("Jetson Camera", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

            if key == 32:
                save_frame(frame, args.output)
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
