#!/usr/bin/env python3
"""
Generates the `permissions.deny` rules for settings.json from the
single shared pattern list in sensitive_patterns.py, so you never hand-maintain
the same patterns in two places.
 
Usage:
    python generate_settings.py > settings.json
    # or merge the printed "permissions" object into an existing
    # settings.json by hand / with jq.
"""
 
import json
from sensitive_patterns import BLOCKED_PATTERNS, DENY_TOOLS
 
 
def build_deny_rules():
    rules = []
    for tool in DENY_TOOLS:
        for pattern in BLOCKED_PATTERNS:
            # Normalize to a **/pattern glob so it matches at any depth,
            # per Claude Code's gitignore-style Read/Edit/Write patterns.
            glob = pattern if pattern.startswith(("/", "**", "~")) else f"**/{pattern}"
            rules.append(f"{tool}({glob})")
    return rules
 
 
def build_settings():
    return {
        "permissions": {
            "deny": build_deny_rules(),
        },
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Read|Edit|Write|Grep|Glob|Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/block_sensitive_files.py",
                        }
                    ],
                }
            ]
        },
    }
 
 
if __name__ == "__main__":
    print(json.dumps(build_settings(), indent=2))
 