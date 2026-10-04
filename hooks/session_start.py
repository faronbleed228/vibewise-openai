#!/usr/bin/env python3
"""Read-only context restoration for OpenAI SessionStart hooks."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "vibewise" / "scripts"))
from state import context  # noqa: E402


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict) or not isinstance(event.get("cwd"), str):
            raise ValueError("Expected a hook event with a string cwd.")
        restored = context(event["cwd"])
        if restored:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "SessionStart", "additionalContext": restored,
            }}))
    except (OSError, ValueError) as exc:
        print(json.dumps({"systemMessage": f"VibeWise could not restore notes: {exc}"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
