#!/usr/bin/env python3
"""
Claude Code PreToolUse hook: blocks tools from reading/writing/editing
files that match a configurable "sensitive files" list (e.g. .env).

How it works
------------
Claude Code invokes this script before Read, Edit, Write, Grep, and Glob
tool calls (whichever tools you wire it to in settings.json) and pipes a
JSON payload to stdin describing the pending tool call. This script:

  1. Reads that JSON.
  2. Extracts whatever path-like field is relevant for the tool
     (file_path for Read/Edit/Write, path/pattern for Grep/Glob).
  3. Checks it against a list of blocked glob patterns.
  4. If it matches, prints a message to stderr and exits with code 2,
     which Claude Code treats as "block this tool call" and feeds the
     stderr text back to Claude as the reason.
  5. Otherwise exits 0, allowing the tool call to proceed.

Note on coverage: PreToolUse only fires for actual tool calls. If the
user references a file directly with @path/to/.env in their prompt,
Claude Code inlines its contents while building the prompt and no
PreToolUse hook fires for that. This script cannot block that path —
but the Claude Settings `permissions` can.
"""

import fnmatch
import json
import os
import sys

# Import the shared pattern list (sensitive_patterns.py must sit next
# to this script, e.g. both in .claude/hooks/) so the hook and the
# settings.json generator always agree on what's "sensitive."
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sensitive_patterns import BLOCKED_PATTERNS  # noqa: E402


def is_blocked(path: str) -> bool:
    if not path:
        return False
    norm = path.replace("\\", "/")
    base = os.path.basename(norm)
    for pattern in BLOCKED_PATTERNS:
        pat = pattern.lower()
        if fnmatch.fnmatch(base.lower(), pat) or fnmatch.fnmatch(norm.lower(), pat):
            return True
    return False


def extract_candidate_paths(tool_name: str, tool_input: dict) -> list:
    """Pull out whatever field(s) could contain a path for this tool."""
    candidates = []

    # Read / Edit / Write all use file_path
    if "file_path" in tool_input:
        candidates.append(tool_input["file_path"])

    # Grep / Glob use path (dir to search) and/or pattern
    if "path" in tool_input:
        candidates.append(tool_input["path"])
    if "pattern" in tool_input and tool_name in ("Grep", "Glob"):
        candidates.append(tool_input["pattern"])

    # Bash: best-effort scan of the command string for blocked filenames.
    # This is NOT a substitute for the Read/Edit/Write checks above —
    # it's a shallow safety net and can be bypassed (e.g. base64, cat
    # with wildcards, python -c, etc.). Treat it as defense-in-depth,
    # not a guarantee.
    if tool_name == "Bash" and "command" in tool_input:
        command = tool_input["command"]
        for pattern in BLOCKED_PATTERNS:
            token = pattern.strip("*")
            if token and token.lower() in command.lower():
                candidates.append(token)

    return [c for c in candidates if c]


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Malformed input — fail open (allow) rather than break the session.
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    for candidate in extract_candidate_paths(tool_name, tool_input):
        if is_blocked(candidate):
            print(
                f"Blocked: '{candidate}' matches a protected file pattern "
                f"and cannot be accessed by {tool_name}.",
                file=sys.stderr,
            )
            sys.exit(2)  # exit code 2 = block the tool call

    sys.exit(0)  # allow


if __name__ == "__main__":
    main()