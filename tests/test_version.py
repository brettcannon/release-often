import pytest

from release_me import version


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
