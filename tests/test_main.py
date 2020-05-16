import json
from unittest import mock

import gidgethub.abc
import pytest

from release_often import __main__ as main


class TestMatchingPR:
    @pytest.mark.asyncio
    async def test_pr_found(self, data_path):
        """Test when a PR number is specified in the initial commit's message."""
        gh_mock = mock.AsyncMock(gidgethub.abc.GitHubAPI)
        push_data = data_path / "push.json"
        push_event = json.loads(push_data.read_text(encoding="utf-8"))
        pr_data = data_path / "PR.json"
        pr_event = json.loads(pr_data.read_text(encoding="utf-8"))
        gh_mock.getitem.return_value = pr_event

        result = await main.matching_pr(gh_mock, push_event)
        assert result == pr_event
        gh_mock.getitem.assert_called_with(
            push_event["repository"]["pulls_url"], {"number": "108"}
        )

    @pytest.mark.asyncio
    async def test_no_pr_number(self, data_path):
        """Test when no PR number is specified in the initial commit message."""
        gh_mock = mock.AsyncMock(gidgethub.abc.GitHubAPI)
        push_data = data_path / "push.json"
        push_event = json.loads(push_data.read_text(encoding="utf-8"))
        push_event["commits"][0]["message"] = "No PR to see here!"

        result = await main.matching_pr(gh_mock, push_event)
        assert not result
