import argparse
import os
import pathlib
import re
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


PR_NUM = re.compile(r"\(#(?P<number>\d+)\)")


def error(message):
    gidgethub.actions.command("error", message)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--changelog-path", dest="changelog_path")
    parser.add_argument("--pypi-token", dest="pypi_token")
    parser.add_argument("--github-token", dest="github_token")
    return parser.parse_args()


async def matching_pr(gh, push_event):
    pr_number_match = PR_NUM.search(push_event["commits"][0]["message"])
    if not pr_number_match:
        return None
    pr_number = pr_number_match.group("number")
    pr_url_template = push_event["repository"]["pulls_url"]
    return await gh.getitem(pr_url_template, {"number": pr_number})


def update_version(pr_event):
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
    try:
        new_version = version.bump_by_label(pr_event, current_version)
    except ValueError as exc:
        gidgethub.actions.command("debug", str(ValueError))
        return None
    gidgethub.actions.command("debug", f"New version is {new_version}")
    try:
        new_contents = build_tool.change_version(
            file_contents, current_version, new_version
        )
    except ValueError as exc:
        # Bump label is missing.
        error(str(exc))
    version_file.write_text(new_contents, encoding="utf-8")
    return new_version


def update_changelog(path, new_version, pr_event):
    if not path.exists():
        error(f"The path to the changelog does not exist: {path}")
    gidgethub.actions.command("debug", f"Changelog file path is {path}")
    current_changelog = path.read_text(encoding="utf-8")
    new_changelog = changelog.update(
        current_changelog, path.suffix, new_version, pr_event
    )
    path.write_text(new_changelog, encoding="utf-8")
    return pr_event["title"]


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
    env = os.environ.copy()
    env.update({"TWINE_USERNAME": "__token__", "TWINE_PASSWORD": pypi_token})
    subprocess.run(
        ["twine", "upload", "--non-interactive", f"{output_dir}/*"], check=True, env=env
    )


async def create_release(gh, version, changelog_entry):
    event = gidgethub.actions.event()
    releases_url = event["repository"]["releases_url"]
    return await release.create(gh, releases_url, version, changelog_entry)


async def main():
    args = parse_args()
    async with httpx.AsyncClient() as client:
        gh = gidgethub.httpx.GitHubAPI(
            client, "brettcannon/release_often", oauth_token=args.github_token
        )

        push_event = gidgethub.actions.event()
        pr_event = await matching_pr(gh, push_event)
        if not pr_event:
            gidgethub.actions.command(
                "debug", "No pull request number found in first commit's title"
            )
            sys.exit()
        new_version = update_version(pr_event)
        if new_version is None:
            gidgethub.actions.command("debug", "No version update requested")
            sys.exit()
        changelog_entry = update_changelog(
            pathlib.Path(args.changelog_path), new_version, pr_event
        )
        output_dir = build()
        commit(new_version)
        if args.pypi_token != "-":
            upload(output_dir, args.pypi_token)
        else:
            gidgethub.actions.command(
                "debug", "PyPI uploading skipped; no API token provided"
            )
        await create_release(gh, new_version, changelog_entry)


if __name__ == "__main__":
    trio.run(main)
