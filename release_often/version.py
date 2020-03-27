import enum

import packaging


@enum.unique
class BumpLevel(enum.Enum):
    major = "impact:breaking"
    minor = "impact:feature"
    micro = "impact:bugfix"
    post = "impact:post-release"
    internal = "impact:project"


def bump(version, bump_by):
    version = packaging.version.Version(version)
    major, minor, micro, post = (
        version.major,
        version.minor,
        version.micro,
        version.post,
    )
    if bump_by == BumpLevel.major:
        return f"{major + 1}.0.0"
    elif bump_by == BumpLevel.minor:
        return f"{major}.{minor + 1}.0"
    elif bump_by == BumpLevel.micro:
        return f"{major}.{minor}.{micro + 1}"
    elif bump_by == BumpLevel.post:
        post = (post or 0) + 1
        return f"{major}.{minor}.{micro}.post{post}"
    else:
        return None
