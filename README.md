# release-often
A GitHub Action for releasing a Python project to PyPI after every relevant, merged PR.

The purpose of this action is to make project maintenance as easy as possible for PyPI-hosted projects by removing the need to decide when to release. By releasing after every relevant PR is merged, not only is the question of whether to release gone, but the overhead of remembering how to even do a release and then preparing one is also gone. It also allows for releases to occur in situations where you may not have easy access to a checkout or machine setup to make a release (e.g. merging a PR from your phone). As well, contributors will be able to benefit from their hard work much faster than having to wait for the gathering of multiple changes together into a single release.

Do note that this action is not designed to work for all projects. There are legitimate reasons to want to do a release until it contains multiple changes. This action is specifically tailored towards smaller -- typically single-maintainer -- projects where PR merges are infrequent and the release process alone makes up a sizable amount of the cost of maintenance.

## Steps
1. Update the version number according to a label on the merged PR
2. Update the changelog based on the commit message
3. Commit the above updates
4. Build sdist and wheels
5. Upload to PyPI
6. Create a release on GitHub

## Caveats
Due to the fact that the action commits back to the repository you cannot have required status checks on PRs as that prevents direct commits from non-admins.

## Details
### Update version
Based on which of the following labels are applied to a PR, update the version number:

- `impact:breaking` to bump the major version
- `impact:feature` to bump the minor version
- `impact:bugfix` to bump the micro version
- `impact:post-release` to bump the `post` version
- `impact:project` to make no change

Supported build tools:
- None

#### TODO
- Make the acceptable labels configurable?
- Support the following build tools:
  1. Poetry
  1. flit
  1. setuptools via `setup.cfg`?
  1. setuptools via `setup.py`?
- Provide a way to manually specify file path and regex?

### Update the changelog
The first line of the commit message is used as the entry in the changelog for the change. The PR and the author of the change are mentioned as part of the changelog entry.

Supported changelog formats are:
- None

Automatically detected changelog file paths are:
- None

#### TODO
- Changelog file formats:
  1. `.md`
  1. `.rst`
- Changelog file paths:
  1. `CHANGELOG`
  1. `doc/CHANGELOG`
  1. `CHANGES`
  1. `doc/CHANGES`
- Allow specifying the format of the changelog entry?
- Specify the path to the changelog?
- Support a static header?
- Allow [specifying emoji](https://cjolowicz.github.io/posts/hypermodern-python-06-ci-cd/#documenting-releases-with-release-drafter) to visually signal signficance of the change?

### Commit the changes
Once the above changes are made, they are committed directly to the repository.

#### TODO
- Allow for specifying the author details?

### Upload to PyPI
With the checkout and repository in the appropriate state for release, the code can now be built and pushed to PyPI.

#### TODO
- Support the following build tools:
  1. Poetry
  1. flit
  1. setuptools via `setup.cfg`?
  1. setuptools via `setup.py`?

### Create a release on GitHub
Finally, when everything is live, create a release on GitHub to both store the artifacts uploaded to PyPI and to tag the relesae in the repository. The name of the release is the version prepended by `v` and the body of the release is the changelog entry.

#### TODO
- [Upload release artifacts](https://developer.github.com/v3/repos/releases/#upload-a-release-asset)
- Customization of the release name?
