MD = """# {version}
[PR #{pr_number}]({pr_url}): {summary} (thanks [{committer}]({committer_url}))

"""

RST = """{version}
=====================================================================
`PR #{pr_number} <{pr_url}>`_: {summary} (thanks `{committer} <{committer_url}>`_)

"""

TEMPLATES = {".md": MD, ".rst": RST}


def entry(path_extension, version, pr_event):
    """Create a changelog entry based on the log's file extension and PR webhook event."""
    template = TEMPLATES[path_extension.lower()]
    pull_request = pr_event["pull_request"]
    details = {
        "version": version,
        "pr_number": pull_request["number"],
        "pr_url": pull_request["html_url"],
        "summary": pull_request["title"],
        "committer": pull_request["user"]["login"],
        "committer_url": pull_request["user"]["html_url"],
    }
    return template.format_map(details)
