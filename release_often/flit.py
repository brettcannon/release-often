import re

import tomlkit


VERSION_RE = re.compile(
    r"""^__version__\s*=\s*['"](?P<version>\d+\.\d+\.\d+(\.post\d+)?)['"]"""
)


def version_file_path(directory):
    pyproject = directory / "pyproject.toml"
    if not pyproject.exists():
        raise TypeError(f"{pyproject!r} does not exist")
    data = tomlkit.loads(pyproject.read_text(encoding="utf-8"))
    try:
        module_name = data["tool"]["flit"]["metadata"]["module"]
    except KeyError as exc:
        raise ValueError(
            f"{pyproject} missing 'tool.flit.metadata' table with 'module' key"
        ) from exc
    path_possibilities = [
        directory / f"{module_name}.py",
        directory / module_name / "__init__.py",
        # I will forever blame Brian Okken for the following 'src' paths. ;)
        directory / "src" / f"{module_name}.py",
        directory / "src" / module_name / "__init__.py",
    ]
    for path in path_possibilities:
        print(path)
        if path.exists():
            return path
    else:
        raise TypeError(f"Cannot find location of '__version__' for {module_name!r}")


def read_version(file_contents):
    return VERSION_RE.search(file_contents).group("version")


def change_version(file_contents, old_version, new_version):
    return file_contents.replace(old_version, new_version)
