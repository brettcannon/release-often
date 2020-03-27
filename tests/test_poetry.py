import pathlib

import pytest
import tomlkit

from release_often import poetry


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / "data"


@pytest.fixture
def pyproject_contents(data_path):
    path = data_path / "poetry" / "pyproject.toml"
    return path.read_text(encoding="utf-8")


class TestVersionFilePath:

    """Tests for release_often.poetry.version_file_path()."""

    def test_no_pyproject(self, data_path):
        with pytest.raises(TypeError):
            poetry.version_file_path(data_path)


    def test_missing_poetry_details(self, data_path):
        flit_path = data_path / "flit" / "top_pkg"
        with pytest.raises(ValueError):
            poetry.version_file_path(flit_path)


    def test_success(self, data_path):
        poetry_path = data_path / "poetry"
        pyproject_path = poetry_path / "pyproject.toml"
        assert poetry.version_file_path(poetry_path) == pyproject_path


class TestReadVersion:

    """Tests for release_often.poetry.read_version()."""

    def test_success(self, pyproject_contents):
        assert poetry.read_version(pyproject_contents) == "1.2.3"


class TestChangeVersion:

    """Tests for release_often.poetry.change_version()."""

    def test_success(self, pyproject_contents):
        new_version = "2.0.0"
        changed = poetry.change_version(pyproject_contents, "1.2.3", new_version)
        changed_data = tomlkit.loads(changed)
        assert changed_data["tool"]["poetry"]["version"] == new_version
