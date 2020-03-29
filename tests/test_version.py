import pytest

from release_often import version
from release_often import flit, poetry


@pytest.mark.parametrize(
    "given,level,expect",
    [
        ("1.2.3", version.BumpLevel.major, "2.0.0"),
        ("1.2.3", version.BumpLevel.minor, "1.3.0"),
        ("1.2.3", version.BumpLevel.micro, "1.2.4"),
        ("1.2.3", version.BumpLevel.post, "1.2.3.post1"),
        ("1.2.3.post1", version.BumpLevel.post, "1.2.3.post2"),
        ("1.2.3", version.BumpLevel.internal, None),
    ],
)
def test_bump(given, level, expect):
    assert version.bump(given, level) == expect


@pytest.mark.parametrize(
    "test_path,build_tool,file_path",
    [("poetry", poetry, "pyproject.toml"), ("flit/top_module", flit, "pkg.py")],
)
def test_find_details(data_path, test_path, build_tool, file_path):
    directory = data_path / test_path
    result = version.find_details(directory)
    assert result[0] == build_tool
    assert result[1] == directory / file_path


def test_bump_by_label(pr_event):
    old_version = "1.2.3"
    assert version.bump_by_label(pr_event, old_version) == "2.0.0"
