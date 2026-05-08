#!/usr/bin/env python3
"""Simple rule mapper from VLM text to robot/IoT actions."""

from __future__ import annotations

import argparse
import json


def convert_vlm_response_to_action(vlm_text: str) -> dict[str, str]:
    text = vlm_text.lower()

    if "person" in text or "human" in text:
        return {
            "action": "slow_down_or_stop",
            "reason": "Person detected in scene",
        }

    if "box" in text or "package" in text:
        return {
            "action": "pick_or_inspect_object",
            "reason": "Box/package detected",
        }

    if "empty" in text or "nothing" in text:
        return {
            "action": "continue_patrol",
            "reason": "No major object detected",
        }

    return {
        "action": "request_human_confirmation",
        "reason": "Scene unclear",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Map VLM text into a simple action decision.")
    parser.add_argument(
        "--text",
        default="The image contains a person standing near a table with a red box.",
        help="VLM response text to classify",
    )
    args = parser.parse_args()
    print(json.dumps(convert_vlm_response_to_action(args.text), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
