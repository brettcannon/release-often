import tomlkit


def version_file_path(directory):
    """Verify pyproject.toml contains "tool.poetry"."""
    pyproject = directory / "pyproject.toml"
    if not pyproject.exists():
        raise TypeError(f"{pyproject!r} does not exist")
    data = tomlkit.loads(pyproject.read_text(encoding="utf-8"))
    try:
        data["tool"]["poetry"]["version"]
    except KeyError as exc:
        raise ValueError(
            f"{pyproject!r} missing a 'tool.poetry' table with 'version' key"
        ) from exc
    return pyproject


def read_version(file_contents):
    """Read the project setting from pyproject.toml."""
    data = tomlkit.loads(file_contents)
    details = data["tool"]["poetry"]
    return details["version"]


def change_version(file_contents, old_version, new_version):
    """Create new file contents for pyproject.toml with the new version."""
    data = tomlkit.loads(file_contents)
    details = data["tool"]["poetry"]
    details["version"] = new_version
    return tomlkit.dumps(data)
