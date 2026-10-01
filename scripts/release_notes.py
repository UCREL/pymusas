# /// script
# requires-python = ">=3.10, <3.14"
# dependencies = [
#   "pymusas"]
# ///

'''
Reference: This script has been adapted from the AllenNLP repository:
https://github.com/allenai/allennlp/blob/2cdb8742c8c8c3c38ace4bdfadbdc750a1aa2475/scripts/release_notes.py

Prepares markdown release notes for GitHub releases.
'''

import os
import subprocess

import pymusas


TAG = os.environ["TAG"]


ADDED_HEADER = "### Added 🎉"
CHANGED_HEADER = "### Changed ⚠️"
FIXED_HEADER = "### Fixed ✅"
REMOVED_HEADER = "### Removed 🗑"
DEPRECATED_HEADER = "### Deprecated 👋"
SECURITY_HEADER = "### Security 🔒"


def get_change_log_notes() -> str:
    in_current_section = False
    current_section_notes: list[str] = []
    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith("## "):
                if line.startswith("## Unreleased"):
                    continue
                if line.startswith(f"## [{TAG}]"):
                    in_current_section = True
                    continue
                break
            if in_current_section:
                if line.startswith("### Added"):
                    line = ADDED_HEADER + "\n"
                elif line.startswith("### Changed"):
                    line = CHANGED_HEADER + "\n"
                elif line.startswith("### Fixed"):
                    line = FIXED_HEADER + "\n"
                elif line.startswith("### Removed"):
                    line = REMOVED_HEADER + "\n"
                elif line.startswith("### Deprecated"):
                    line = DEPRECATED_HEADER + "\n"
                elif line.startswith("### Security"):
                    line = SECURITY_HEADER + "\n"
                current_section_notes.append(line)
    assert current_section_notes
    return "## What's new\n\n" + "".join(current_section_notes).strip() + "\n"


def get_commit_history() -> str:
    git_log = subprocess.run(
        f"git log $(git describe --always --tags --abbrev=0 {TAG}^^)..{TAG}^ --oneline",
        shell=True, stdout=subprocess.PIPE, text=True
    )
    commit_history = "## Commits\n\n" + git_log.stdout
    return commit_history


def main() -> None:
    if TAG != f"v{pymusas.__version__}":
        raise ValueError(f"The environment variable `TAG` `{TAG}` "
                         f"is not the same as `v{pymusas.__version__}` "
                         "which it should be.")
    print(get_change_log_notes())
    print(get_commit_history())


if __name__ == "__main__":
    main()
