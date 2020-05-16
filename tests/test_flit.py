import pytest

from release_often import flit


class TestVersionFilePath:

    """Tests for release_often.flit.version_file_path()."""

    def test_pyproject_does_not_exist(self, data_path):
        with pytest.raises(TypeError):
            flit.version_file_path(data_path)

    def test_pyproject_missing_data(self, poetry_example_path):
        with pytest.raises(ValueError):
            flit.version_file_path(poetry_example_path)

    @pytest.mark.parametrize(
        "example_name, expected_path",
        [
            ("src_module", "src/pkg.py"),
            ("src_pkg", "src/pkg/__init__.py"),
            ("top_module", "pkg.py"),
            ("top_pkg", "pkg/__init__.py"),
        ],
    )
    def test_found_path(self, data_path, example_name, expected_path):
        example_path = data_path / "flit" / example_name
        print(example_path)
        assert flit.version_file_path(example_path) == example_path / expected_path

    def test_version_file_not_found(self):
        pass


class TestReadVersion:

    """Tests for release_often.flit.read_version()."""

    @pytest.mark.parametrize(
        "source",
        [
            """__version__='1.2.3'""",
            """__version__=\"1.2.3\"""",
            """__version__ = \"1.2.3\"""",
            "__version__ = '1.2.3'  # A comment!",
        ],
    )
    def test_success(self, source):
        assert flit.read_version(source) == "1.2.3"


class TestChangeVersion:

    """Tests for release_often.flit.change_version()."""

    @pytest.mark.parametrize(
        "source,expect",
        [
            ("""__version__='1.2.3'""", """__version__='2.0.0'"""),
            ("""__version__=\"1.2.3\"""", """__version__=\"2.0.0\""""),
            ("""__version__ = \"1.2.3\"""", """__version__ = \"2.0.0\""""),
            (
                "__version__ = '1.2.3'  # A comment!",
                "__version__ = '2.0.0'  # A comment!",
            ),
        ],
    )
    def test_success(self, source, expect):
        assert flit.change_version(source, "1.2.3", "2.0.0") == expect
