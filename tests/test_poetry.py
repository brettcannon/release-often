import pathlib

import pytest

from release_me import poetry


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / "data"


def test_no_pyproject(data_path):
    assert poetry.version_file_path(data_path) is None


def test_missing_poetry_details(data_path):
    flit_path = data_path / "flit"
    assert poetry.version_file_path(flit_path) is None


def test_success(data_path):
    poetry_path = data_path / "poetry"
    pyproject_path = poetry_path / "pyproject.toml"
    assert poetry.version_file_path(poetry_path) == pyproject_path
