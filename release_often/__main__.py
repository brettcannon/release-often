import argparse
import sys

from gidgethub import actions

from . import changelog
from . import version


def error(message):
    actions.command("error", message)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--changelog-path", dest="changelog_path")
    return parser.parse_args()


def update_version():
    build_tool, version_file = version.find_details(actions.workspace())
    if build_tool is None:
        error("build tool not detected; unable to update version")
    file_contents = version_file.read_text(encoding="utf-8")
    current_version = build_tool.read_version(file_contents)
    new_version = version.bump_by_label(actions.event(), current_version)
    new_contents = build_tool.change_version(
        file_contents, current_version, new_version
    )
    version_file.write_text(new_contents, encoding="utf-8")
    return new_version


def update_changelog(path, new_version):
    if not path.exists():
        error(f"The path to the changelog does not exist: {path!r}")
    new_entry = changelog.entry(path.suffix, new_version, actions.event())
    current_changelog = path.read_text(encoding="utf-8")
    path.write_text(new_entry + current_changelog, encoding="utf-8")


if __name__ == "__main__":
    args = parse_args()
    new_version = update_version()
    update_changelog(pathlib.Path(args.changelog_path), new_version)
    # XXX Commit the changes
    # XXX Upload to PyPI
    # XXX Create a release on GitHub
    pass
