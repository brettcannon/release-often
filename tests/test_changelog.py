import pytest

from release_often import changelog


OLD_RST_CHANGELOG = """\
Changelog
=========

1.0.0
-------------------------------------------------
`PR #1 <...>`__: I did something! (thanks `Brett <...>`__)
"""

NEW_RST_CHANGELOG = """\
Changelog
=========

2.0.0
-------------------------------------------------
`PR #108 <https://github.com/brettcannon/gidgethub/pull/108>`__: Adding utility functions for GitHub App (thanks `Mariatta <https://github.com/Mariatta>`__)

1.0.0
-------------------------------------------------
`PR #1 <...>`__: I did something! (thanks `Brett <...>`__)
"""

OLD_MD_CHANGELOG = """\
# Changelog

## 1.0.0
-------------------------------------------------
[PR #1]()...): I did something! (thanks [Brett](...))
"""

NEW_MD_CHANGELOG = """\
# Changelog

## 2.0.0
[PR #108](https://github.com/brettcannon/gidgethub/pull/108): Adding utility functions for GitHub App (thanks [Mariatta](https://github.com/Mariatta))

## 1.0.0
-------------------------------------------------
[PR #1]()...): I did something! (thanks [Brett](...))
"""


@pytest.mark.parametrize(
    "file_extension,old_changelog,expect",
    [
        (".rst", OLD_RST_CHANGELOG, NEW_RST_CHANGELOG),
        (".md", OLD_MD_CHANGELOG, NEW_MD_CHANGELOG),
    ],
)
def test_update(pr_event, file_extension, old_changelog, expect):
    new_changelog = changelog.update(old_changelog, file_extension, "2.0.0", pr_event)
    assert new_changelog == expect


def test_bad_header(pr_event):
    with pytest.raises(ValueError):
        changelog.update("I have no header!", ".md", "2.0.0", pr_event)


SINGLE_ENTRY = """\
# Changelog

## 2.0.0
[PR #108](https://github.com/brettcannon/gidgethub/pull/108): Adding utility functions for GitHub App (thanks [Mariatta](https://github.com/Mariatta))
"""


def test_no_header(pr_event):
    expect = changelog.update("", ".md", "2.0.0", pr_event)
    assert SINGLE_ENTRY == expect
