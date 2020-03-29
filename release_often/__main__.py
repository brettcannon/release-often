import argparse
import pathlib
import subprocess
import sys

from gidgethub import actions
import pep517.envbuild

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


def build():
    source_dir = actions.workspace()
    output_dir = source_dir / "dist"
    for builder in (pep517.envbuild.build_sdist, pep517.envbuild.build_wheel):
        builder(source_dir, output_dir)
    subprocess.run(["twine", "check", f"{output_dir}/*"], check=True)
    return output_dir


def commit(new_version):
    subprocess.run(
        ["git", "config", "--local", "user.email", "action@github.com"], check=True
    )
    subprocess.run(
        ["git", "config", "--local", "user.name", "GitHub Action"], check=True
    )
    subprocess.run(["git", "commit", "-a", "-m", f"Updates for v{new_version}"])


if __name__ == "__main__":
    args = parse_args()
    new_version = update_version()
    if new_version is None:
        actions.command("debug", "No version update requested")
        sys.exit()
    update_changelog(pathlib.Path(args.changelog_path), new_version)
    output_dir = build()
    commit(new_version)
    # XXX Upload to PyPI
    # XXX Create a release on GitHub
    pass
