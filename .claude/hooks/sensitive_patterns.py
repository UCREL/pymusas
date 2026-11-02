"""
Single source of truth for which files are considered sensitive.
Both the PreToolUse hook and the settings.json generator import this
list, so you only ever update patterns in one place.
"""
 
BLOCKED_PATTERNS = [
    ".env",
    ".env.*",
    "*.env",
    "*.pem",
    "*.key",
    "*credentials*",
    "*secrets*",
    ".ssh/*",
]
 
# Which tools the permission deny rules should apply to.
# (The hook script separately covers Grep/Glob/Bash too — see
# block_sensitive_files.py — but Read/Edit/Write are the ones that
# also matter for the static permissions.deny list.)
DENY_TOOLS = ["Read", "Edit", "Write"]