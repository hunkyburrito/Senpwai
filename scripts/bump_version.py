from io import TextIOWrapper
import os
import subprocess
import sys
import re
from typing import cast
from .utils import (
    ROOT_DIR,
    get_current_branch_name,
    log_error as utils_log_error,
    log_info,
    log_warning,
)


PYPROJECT_FILE_PATH = ROOT_DIR.joinpath("pyproject.toml")
FILES_PATHS = [
    PYPROJECT_FILE_PATH,
    ROOT_DIR.joinpath("senpwai/utils/static.py"),
    ROOT_DIR.joinpath("scripts/setup.iss"),
    ROOT_DIR.joinpath("scripts/setup_senpcli.iss"),
]

USAGE = """
Usage: bump_version <OLD_VERSION> <NEW_VERSION>
"""
ENCOUNTERED_ERROR = False
VERSION_REGEX = re.compile(r"(\d+(\.\d+)*)")


def truncate(file: TextIOWrapper, content: str) -> None:
    file.seek(0)
    file.write(content)
    file.truncate()


def log_error(msg: str, exit=False) -> None:
    utils_log_error(msg, exit)
    global ENCOUNTERED_ERROR
    ENCOUNTERED_ERROR = True


def get_prev_version() -> str:
    prev_version = ""
    with open(PYPROJECT_FILE_PATH, "r") as f:
        opt_version = VERSION_REGEX.search(f.read())
        if opt_version is not None:
            prev_version = opt_version.group(1)
    if not prev_version:
        log_error("Failed to get previous version", True)
    return prev_version


def get_new_version() -> str:
    branch_name = get_current_branch_name()
    if branch_name == "master":
        log_error("On master branch, switch to version branch", True)
    new_version = VERSION_REGEX.search(branch_name)
    if new_version is None:
        log_error("Failed to get new version", True)
    return cast(re.Match, new_version).group(1)


def get_versions() -> tuple[str, str]:
    prev_version, new_version = get_prev_version(), get_new_version()
    return prev_version, new_version


def bump_version(prev_version: str, new_version: str, ignore_same: bool):
    for file_path in FILES_PATHS:
        if not os.path.isfile(file_path):
            log_error(f'"{file_path}" not found')
            continue
        with open(file_path, "r+") as f:
            content = f.read()
            new_content = content.replace(prev_version, new_version)
            if not ignore_same and new_content == content:
                if new_version in new_content:
                    log_warning(
                        f'Failed to find previous version in "{file_path}" but the new version is in it'
                    )
                else:
                    log_error(f'Failed to find previous version in "{file_path}"')
                continue
            truncate(f, new_content)
            log_info(f'Bumped version in "{file_path}"')


def main(ignore_same=False) -> None:
    args = sys.argv[1:]
    if len(args) == 1 and args[1] in ("--help", "-h"):
        print(USAGE)
        return
    if len(args) == 2:
        prev_version = args[0]
        new_version = args[1]
    else:
        prev_version, new_version = get_versions()
    if not ignore_same and prev_version == new_version:
        log_error(f"Previous and New version are the same: {prev_version}", True)
    log_info(f"Bumping version from {prev_version} -> {new_version}")
    bump_version(prev_version, new_version, ignore_same)
    subprocess.run("git --no-pager diff")
    if ENCOUNTERED_ERROR:
        sys.exit(1)


if __name__ == "__main__":
    main()
