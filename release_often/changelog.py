MD_HEADER = """\
# Changelog
"""

MD_ENTRY = """\
## {version}
[PR #{pr_number}]({pr_url}): {summary} (thanks [{committer}]({committer_url}))
"""

RST_HEADER = """\
Changelog
=========
"""

RST_ENTRY = """\
{version}
-------------------------------------------------
`PR #{pr_number} <{pr_url}>`__: {summary} (thanks `{committer} <{committer_url}>`__)
"""

TEMPLATES = {".md": (MD_HEADER, MD_ENTRY), ".rst": (RST_HEADER, RST_ENTRY)}


def update(current_changelog, path_extension, version, pr_event):
    """Update the changelog based on a merged pull request."""
    header, entry_template = TEMPLATES[path_extension.lower()]
    if current_changelog.strip() and not current_changelog.startswith(header):
        raise ValueError("Changelog has a non-standard header")
    details = {
        "version": version,
        "pr_number": pr_event["number"],
        "pr_url": pr_event["html_url"],
        "summary": pr_event["title"],
        "committer": pr_event["user"]["login"],
        "committer_url": pr_event["user"]["html_url"],
    }
    entry = entry_template.format_map(details)
    changelog_no_header = current_changelog[len(header) :]
    changelog = f"{header.strip()}\n\n{entry.strip()}\n\n{changelog_no_header.strip()}"
    return f"{changelog.strip()}\n"  # Guarantee a single trailing newline.
