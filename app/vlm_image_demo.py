#!/usr/bin/env python3
"""Run a Hugging Face image-based VLM prompt on Jetson."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration

try:
    from agent_logic import convert_vlm_response_to_action
except ImportError:
    convert_vlm_response_to_action = None


def choose_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_model(model_name: str):
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    processor = AutoProcessor.from_pretrained(model_name)
    model = LlavaForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if not torch.cuda.is_available():
        model.to("cpu")
    return processor, model


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask a VLM a question about an image.")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--prompt", default="Describe this image clearly.", help="Question for the VLM")
    parser.add_argument("--model", default="llava-hf/llava-1.5-7b-hf", help="Hugging Face model ID")
    parser.add_argument("--max-new-tokens", type=int, default=120, help="Maximum generated tokens")
    parser.add_argument("--show-action", action="store_true", help="Print simple action decision")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    device = choose_device()
    print(f"Device: {device}")
    print(f"Loading model: {args.model}")

    processor, model = load_model(args.model)
    image = Image.open(image_path).convert("RGB")

    prompt = f"USER: <image>\n{args.prompt}\nASSISTANT:"
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=False,
        )

    response = processor.decode(output[0], skip_special_tokens=True)
    answer = response.split("ASSISTANT:")[-1].strip()

    print("\n--- VLM Response ---")
    print(answer)

    if args.show_action:
        if convert_vlm_response_to_action is None:
            raise RuntimeError("Could not import app/agent_logic.py")
        print("\n--- Agent Decision ---")
        print(json.dumps(convert_vlm_response_to_action(answer), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
