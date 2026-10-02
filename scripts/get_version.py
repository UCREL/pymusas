import argparse
from pathlib import Path

import tomlkit


if __name__ == "__main__":
    description = (
        "prints to stdout the version number of the given pyproject.toml file"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("toml_file_path",
                        type=Path,
                        help="File path to the pyproject.toml file")
    args = parser.parse_args()
    toml_file_path: Path = args.toml_file_path
    print(tomlkit.parse(toml_file_path.read_text(encoding="utf-8"))['project']['version'])
