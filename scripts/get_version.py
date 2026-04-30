import argparse
import io
import sys


if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


if __name__ == "__main__":
    description = (
        "prints to stdout the version number of the given pyproject.toml file"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("toml_file_path",
                        type=argparse.FileType(mode="r", encoding="utf-8"),
                        help="File path to the pyproject.toml file")
    args = parser.parse_args()
    toml_file_io = args.toml_file_path
    assert isinstance(toml_file_io, io.TextIOWrapper)
    print(tomllib.loads(toml_file_io.read())['project']['version'])
