import argparse
from pathlib import Path
import random
import time
from typing import cast

import tomlkit


def get_unique_number() -> int:
    """
    Generates a unique number that is suitable to be used as part of a
    python package version.

    We would normally use UUID4 but the number for the Python version has to
    be less than `18446744073709551615`

    # Returns

    `int`
    """
    unique_number = int(time.time() * 1000)
    additional_random_number = random.randint(0, 9999)
    larger_unique_number = int(f"{unique_number}{additional_random_number}")
    return larger_unique_number


if __name__ == "__main__":
    description = (
        "Copies the original pyproject.toml (`toml_file_path`) file to a temporary "
        "location specified by `store_original_toml_file_path`. The original pyproject.toml "
        "is then modified to have a unique version number. This script is useful when you want "
        "to create a unique version of the project that when built is not cached by UV "
        "when it is installed. This is very useful for functional testing."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("toml_file_path",
                        type=Path,
                        help="File path to the original pyproject.toml file")
    parser.add_argument("store_original_toml_file_path",
                        type=Path,
                        help="File path to store a copy of the original pyproject.toml file")
    args = parser.parse_args()
    toml_file_path = cast(Path, args.toml_file_path)
    copy_toml_file_path = cast(Path, args.store_original_toml_file_path)

    # The original file is copied byte for byte and the version is edited with
    # tomlkit, so that comments and formatting are preserved in both files.
    original_toml_text = toml_file_path.read_text(encoding="utf-8")
    copy_toml_file_path.write_text(original_toml_text, encoding="utf-8")

    pyproject = tomlkit.parse(original_toml_text)
    current_project_version = str(pyproject["project"]["version"])
    x, y, z = current_project_version.split('.')
    pyproject["project"]["version"] = f"{x}.{y}.{z}.{get_unique_number()}"
    toml_file_path.write_text(tomlkit.dumps(pyproject), encoding="utf-8")
