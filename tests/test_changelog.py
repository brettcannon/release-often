import json

import pytest

from release_often import changelog


file_extensions = pytest.mark.parametrize("file_extension", [".md", ".rst"])

@file_extensions
def test_templates(file_extension):
    template = changelog.TEMPLATES[file_extension]
    details = {
        "version": "1.2.3",
        "pr_number": "42",
        "pr_url": "https://github.com/brettcannon/release-often/pull/42",
        "summary": "A thing changed!",
        "committer": "Andrea McInnes",
        "committer_url": "https://github.com/andreamcinnes",
    }
    entry = template.format_map(details)
    for detail in details.values():
        assert detail in entry


@file_extensions
def test_entry(data_path, file_extension):
    version = "2.0.0"
    json_path = data_path / "merged_PR.json"
    event = json.loads(json_path.read_text(encoding="utf-8"))
    entry = changelog.entry(file_extension, version, event)
    assert version in entry
    assert "105" in entry
    assert "https://github.com/brettcannon/gidgethub/pull/105" in entry
    assert "Update the copyright year in documentation." in entry
    assert "Mariatta" in entry
    assert "https://github.com/Mariatta" in entry
