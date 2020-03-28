import sys

from gidgethub import actions

from . import version


def update_version():
    build_tool, version_file = version.find_details(actions.workspace())
    if build_tool is None:
        actions.command("error", "build tool not detected; unable to update version")
        sys.exit(1)
    file_contents = version_file.read_text(encoding="utf-8")
    current_version = build_tool.read_version(file_contents)
    new_version = version.bump_by_label(actions.event(), current_version)
    new_contents = build_tool.change_version(
        file_contents, current_version, new_version
    )
    version_file.write_text(new_contents, encoding="utf-8")


if __name__ == "__main__":
    update_version()
    # XXX update changelog
    # XXX build the project
    # XXX Commit the changes
    # XXX Upload to PyPI
    # XXX Create a release on GitHub
    pass
