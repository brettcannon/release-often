import json
import pathlib

import pytest


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / "data"


@pytest.fixture
def poetry_example_path(data_path):
    return data_path / "poetry"


@pytest.fixture
def pr_event(data_path):
    path = data_path / "PR.json"
    return json.loads(path.read_text(encoding="utf-8"))
