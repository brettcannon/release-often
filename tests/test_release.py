import json

import trio

from release_often import release
from . import data


class MockGitHubAPI:
    def __init__(self, to_return):
        self.to_return = to_return

    async def post(self, url, *, data):
        self.url = url
        self.data = data
        return self.to_return


def test_create(data_path):
    webhook_event_path = data_path / "create_release.json"
    release_payload = webhook_event_path.read_text(encoding="utf-8")
    to_return = json.loads(release_payload)
    releases_url = "https://url/to/create/release"
    mock_gh = MockGitHubAPI(to_return)
    version = "1.2.3"
    body = "body of things"
    result = trio.run(release.create, mock_gh, releases_url, version, body)
    assert (
        result
        == "https://uploads.github.com/repos/octocat/Hello-World/releases/1/assets{?name,label}"
    )
    assert mock_gh.url == releases_url
    assert mock_gh.data == {"tag_name": "v1.2.3", "body": body}
