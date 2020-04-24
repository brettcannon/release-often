import pytest

from release_often import changelog


OLD_RST_CHANGELOG = """\
Changelog
=========

1.0.0
-------------------------------------------------
`PR #1 <...>`_: I did something! (thanks `Brett <...>`_)
"""

NEW_RST_CHANGELOG = """\
Changelog
=========

2.0.0
-------------------------------------------------
`PR #105 <https://github.com/brettcannon/gidgethub/pull/105>`_: Update the copyright year in documentation. (thanks `Mariatta <https://github.com/Mariatta>`_)

1.0.0
-------------------------------------------------
`PR #1 <...>`_: I did something! (thanks `Brett <...>`_)
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
[PR #105](https://github.com/brettcannon/gidgethub/pull/105): Update the copyright year in documentation. (thanks [Mariatta](https://github.com/Mariatta))

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
[PR #105](https://github.com/brettcannon/gidgethub/pull/105): Update the copyright year in documentation. (thanks [Mariatta](https://github.com/Mariatta))
"""


def test_no_header(pr_event):
    expect = changelog.update("", ".md", "2.0.0", pr_event)
    assert SINGLE_ENTRY == expect
