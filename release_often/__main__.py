import argparse
import os
import pathlib
import subprocess
import sys

import gidgethub.actions
import gidgethub.httpx
import httpx
import pep517.envbuild
import trio

from . import changelog
from . import release
from . import version


def error(message):
    gidgethub.actions.command("error", message)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--changelog-path", dest="changelog_path")
    parser.add_argument("--pypi-token", dest="pypi_token")
    parser.add_argument("--github-token", dest="github_token")
    return parser.parse_args()


def update_version():
    build_tool, version_file = version.find_details(gidgethub.actions.workspace())
    if build_tool is None:
        error("build tool not detected; unable to update version")
    else:
        tool_name = build_tool.__name__.rpartition(".")[-1]
        gidgethub.actions.command("debug", f"Build tool is {tool_name}")
        gidgethub.actions.command("debug", f"Version found in {version_file}")
    file_contents = version_file.read_text(encoding="utf-8")
    current_version = build_tool.read_version(file_contents)
    gidgethub.actions.command("debug", f"Current/old version is {current_version}")
    new_version = version.bump_by_label(gidgethub.actions.event(), current_version)
    gidgethub.actions.command("debug", f"New version is {new_version}")
    new_contents = build_tool.change_version(
        file_contents, current_version, new_version
    )
    version_file.write_text(new_contents, encoding="utf-8")
    return new_version


def update_changelog(path, new_version):
    if not path.exists():
        error(f"The path to the changelog does not exist: {path}")
    gidgethub.actions.command("debug", f"Changelog file path is {path}")
    new_entry = changelog.entry(path.suffix, new_version, gidgethub.actions.event())
    current_changelog = path.read_text(encoding="utf-8")
    path.write_text(new_entry + current_changelog, encoding="utf-8")
    return new_entry


def build():
    source_dir = gidgethub.actions.workspace()
    output_dir = source_dir / "dist"
    gidgethub.actions.command("debug", f"Writing build artifacts to {output_dir}")
    for builder in (pep517.envbuild.build_sdist, pep517.envbuild.build_wheel):
        builder(source_dir, output_dir)
    # https://github.com/python-poetry/poetry/issues/769
    check_result = subprocess.run(["twine", "check", f"{output_dir}/*"])
    if check_result.returncode:
        gidgethub.actions.command("warning", "`twine check` had a non-zero exit code")
    return output_dir


GIT = "/usr/bin/git"


def commit(new_version):
    os.chdir(gidgethub.actions.workspace())
    subprocess.run(
        [GIT, "config", "--local", "user.email", "action@github.com"], check=True,
    )
    subprocess.run(
        [GIT, "config", "--local", "user.name", "GitHub Action"], check=True,
    )
    subprocess.run(
        [GIT, "commit", "-a", "-m", f"Updates for v{new_version}"], check=True,
    )
    subprocess.run([GIT, "push"], check=True)


def upload(output_dir, pypi_token):
    env = {"TWINE_USERNAME": "__token__", "TWINE_PASSWORD": pypi_token}
    subprocess.run(
        ["twine", "upload", "--non-interactive", f"{output_dir}/*"], check=True, env=env
    )


async def make_release(releases_url, version, changelog_entry, oauth_token):
    async with httpx.AsyncClient() as client:
        gh = gidgethub.httpx.GitHubAPI(
            client, "brettcannon/release_often", oauth_token=oauth_token
        )
        return await release.create(gh, releases_url, version, changelog_entry)


def create_release(version, changelog_entry, oauth_token):
    event = gidgethub.actions.event()
    releases_url = event["repository"]["releases_url"]
    return trio.run(make_release, releases_url, version, changelog_entry, oauth_token)


if __name__ == "__main__":
    args = parse_args()
    new_version = update_version()
    if new_version is None:
        gidgethub.actions.command("debug", "No version update requested")
        sys.exit()
    changelog_entry = update_changelog(pathlib.Path(args.changelog_path), new_version)
    output_dir = build()
    commit(new_version)
    if args.pypi_token != "-":
        upload(output_dir, args.pypi_token)
    else:
        gidgethub.actions.command(
            "debug", "PyPI uploading skipped; no API token provided"
        )
    upload_url = create_release(new_version, changelog_entry, args.github_token)
