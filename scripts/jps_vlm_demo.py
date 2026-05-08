#!/usr/bin/env python3
"""Small client for NVIDIA Jetson Platform Services VLM demos."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests


DEFAULT_SYSTEM_PROMPT = (
    "You are a concise vision-language assistant running on an edge device. "
    "Answer only from the visual evidence in the stream."
)


class VlmClientError(RuntimeError):
    pass


def normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def request_json(method: str, url: str, **kwargs: Any) -> Any:
    try:
        response = requests.request(method, url, timeout=kwargs.pop("timeout", 120), **kwargs)
    except requests.RequestException as exc:
        raise VlmClientError(f"Request failed for {url}: {exc}") from exc

    if not response.ok:
        body = response.text.strip()
        raise VlmClientError(f"{method} {url} failed with {response.status_code}: {body}")

    if not response.content:
        return None

    try:
        return response.json()
    except ValueError as exc:
        raise VlmClientError(f"{method} {url} returned non-JSON response: {response.text}") from exc


def health(args: argparse.Namespace) -> None:
    payload = request_json("GET", args.health_url)
    print(json.dumps(payload, indent=2))


def add_stream(args: argparse.Namespace) -> None:
    api = normalize_base_url(args.api)
    payload = {"liveStreamUrl": args.rtsp}
    data = request_json("POST", f"{api}/api/v1/live-stream", json=payload)
    print(json.dumps(data, indent=2))


def list_streams(args: argparse.Namespace) -> None:
    api = normalize_base_url(args.api)
    data = request_json("GET", f"{api}/api/v1/live-stream")
    print(json.dumps(data, indent=2))


def delete_stream(args: argparse.Namespace) -> None:
    api = normalize_base_url(args.api)
    data = request_json("DELETE", f"{api}/api/v1/live-stream/{args.stream_id}")
    if data is not None:
        print(json.dumps(data, indent=2))
    else:
        print(f"Deleted stream {args.stream_id}")


def build_chat_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "messages": [
            {
                "role": "system",
                "content": args.system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "stream",
                        "stream": {
                            "stream_id": args.stream_id,
                        },
                    },
                    {
                        "type": "text",
                        "text": args.prompt,
                    },
                ],
            },
        ],
        "min_tokens": args.min_tokens,
        "max_tokens": args.max_tokens,
    }


def extract_answer(data: dict[str, Any]) -> str:
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise VlmClientError(f"Unexpected chat response shape: {json.dumps(data, indent=2)}") from exc


def ask_once(args: argparse.Namespace) -> str:
    api = normalize_base_url(args.api)
    payload = build_chat_payload(args)
    data = request_json("POST", f"{api}/api/v1/chat/completions", json=payload)
    answer = extract_answer(data)
    print(answer)
    run_actions(answer, args.action_rules, args.dry_run_action)
    return answer


def load_action_rules(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []

    rule_path = Path(path)
    try:
        rules = json.loads(rule_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise VlmClientError(f"Could not read action rules {rule_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise VlmClientError(f"Could not parse JSON action rules {rule_path}: {exc}") from exc

    if not isinstance(rules, list):
        raise VlmClientError("Action rules must be a JSON array")

    for rule in rules:
        if not isinstance(rule, dict) or "contains" not in rule or "command" not in rule:
            raise VlmClientError("Each action rule needs 'contains' and 'command' fields")

    return rules


def run_actions(answer: str, rules_path: str | None, dry_run: bool) -> None:
    for rule in load_action_rules(rules_path):
        needle = rule["contains"]
        if needle.lower() not in answer.lower():
            continue

        name = rule.get("name", needle)
        command = rule["command"]
        if dry_run:
            print(f"[action:dry-run] {name}: {command}", file=sys.stderr)
            continue

        print(f"[action] {name}: {command}", file=sys.stderr)
        completed = subprocess.run(command, shell=True, check=False)
        if completed.returncode != 0:
            print(f"[action:error] {name} exited with {completed.returncode}", file=sys.stderr)


def ask(args: argparse.Namespace) -> None:
    ask_once(args)


def loop(args: argparse.Namespace) -> None:
    while True:
        try:
            ask_once(args)
        except VlmClientError as exc:
            print(f"[error] {exc}", file=sys.stderr)
        time.sleep(args.interval)


def set_alerts(args: argparse.Namespace) -> None:
    api = normalize_base_url(args.api)
    payload = {
        "id": args.stream_id,
        "alerts": args.alert,
    }
    data = request_json("POST", f"{api}/api/v1/alerts", json=payload)
    print(json.dumps(data, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Client for Jetson Platform Services VLM stream demos."
    )
    subparsers = parser.add_subparsers(required=True)

    health_parser = subparsers.add_parser("health", help="Check VLM health endpoint")
    health_parser.add_argument(
        "--health-url",
        default="http://127.0.0.1:5015/v1/health",
        help="JPS VLM health URL",
    )
    health_parser.set_defaults(func=health)

    add_parser = subparsers.add_parser("add-stream", help="Register an RTSP stream")
    add_parser.add_argument("--api", default="http://127.0.0.1:5010", help="JPS VLM API base URL")
    add_parser.add_argument("--rtsp", required=True, help="RTSP stream URL")
    add_parser.set_defaults(func=add_stream)

    list_parser = subparsers.add_parser("list-streams", help="List registered streams")
    list_parser.add_argument("--api", default="http://127.0.0.1:5010", help="JPS VLM API base URL")
    list_parser.set_defaults(func=list_streams)

    delete_parser = subparsers.add_parser("delete-stream", help="Delete a registered stream")
    delete_parser.add_argument("--api", default="http://127.0.0.1:5010", help="JPS VLM API base URL")
    delete_parser.add_argument("--stream-id", required=True, help="JPS stream ID")
    delete_parser.set_defaults(func=delete_stream)

    ask_parser = subparsers.add_parser("ask", help="Ask a question about a stream")
    add_chat_args(ask_parser)
    ask_parser.set_defaults(func=ask)

    loop_parser = subparsers.add_parser("loop", help="Ask repeatedly at a fixed interval")
    add_chat_args(loop_parser)
    loop_parser.add_argument("--interval", type=float, default=5.0, help="Seconds between prompts")
    loop_parser.set_defaults(func=loop)

    alerts_parser = subparsers.add_parser("set-alerts", help="Configure native JPS alerts")
    alerts_parser.add_argument("--api", default="http://127.0.0.1:5010", help="JPS VLM API base URL")
    alerts_parser.add_argument("--stream-id", required=True, help="JPS stream ID")
    alerts_parser.add_argument(
        "--alert",
        action="append",
        required=True,
        help="Yes/no alert prompt. Repeat for multiple alerts.",
    )
    alerts_parser.set_defaults(func=set_alerts)

    return parser


def add_chat_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api", default="http://127.0.0.1:5010", help="JPS VLM API base URL")
    parser.add_argument("--stream-id", required=True, help="JPS stream ID")
    parser.add_argument("--prompt", required=True, help="Question or instruction for the VLM")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT, help="System prompt")
    parser.add_argument("--min-tokens", type=int, default=1, help="Minimum generated tokens")
    parser.add_argument("--max-tokens", type=int, default=128, help="Maximum generated tokens")
    parser.add_argument("--action-rules", help="Path to JSON action rules")
    parser.add_argument(
        "--dry-run-action",
        action="store_true",
        help="Print matching actions without executing commands",
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except VlmClientError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
