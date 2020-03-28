# release-often
A GitHub Action for releasing a Python project to PyPI after every relevant, merged PR.

The purpose of this action is to make project maintenance as easy as possible for PyPI-hosted projects by removing the need to decide when to release. By releasing after every relevant PR is merged, not only is the question of whether to release gone, but the overhead of remembering how to even do a release and then preparing one is also gone. It also allows for releases to occur in situations where you may not have easy access to a checkout or machine setup to make a release (e.g. merging a PR from your phone). As well, contributors will be able to benefit from their hard work much faster than having to wait for the gathering of multiple changes together into a single release.

Do note that this action is not designed to work for all projects. There are legitimate reasons to bundle multiple changes in a release. This action is specifically tailored towards smaller -- typically single-maintainer -- projects where PR merges are infrequent and the release process alone makes up a sizable amount of the cost of maintenance.

## Outline
1. Update the version number according to a label on the merged PR
2. Update the changelog based on the commit message
3. Commit the above updates
4. Build sdist and wheels
5. Upload to PyPI
6. Create a release on GitHub

## Caveats
Due to the fact that the action commits back to the repository you cannot have required status checks on PRs as that prevents direct commits from non-admins.

## Action instructions
### Suggested configuration
```YAML
release:
  needs: [test, lint]
  if: github.event_name == 'pull_request' && github.ref == 'refs/heads/master' && github.event.action == 'closed' && github.event.pull_request.merged

  runs-on: ubuntu-latest

  steps:
  - uses: actions/checkout@v2
  - uses: brettcannon/release-often@v1
    with:
      changelog-path: doc/CHANGELOG.rst
      github-token: ${{ secret.GITHUB_TOKEN }}
      pypi-token: ${{ secrets.PYPI_TOKEN }}
```

### Inputs

#### `changelog-path`
**Required**: The path to the changelog file. Paths must end in one of the following extensions to denote the file format:
- `.md`
- `.rst`

Leaving this input out will disable automatic changelog updating.

#### `github-token`
**Required**: The GitHub access token (i.e. `${{ secrets.GITHUB_TOKEN }}`). This allows for committing changes back to the repository.

Leaving this input out will disable committing any changes made and creating a release.

#### `pypi-token`
The [PyPI API token](https://pypi.org/help/#apitoken) for this project. It is **strongly** suggested that you create a token scoped to _just_ this project.

Leaving this input out will disable uploading to PyPI.


## Details
### Update version
Based on which of the following labels are applied to a PR, update the version number:

- `impact:breaking` to bump the major version
- `impact:feature` to bump the minor version
- `impact:bugfix` to bump the micro version
- `impact:post-release` to bump the `post` version
- `impact:project` to make no change

Input:
- build tool

Supported build tools:
- poetry
- flit

### Update the changelog
The first line of the commit message is used as the entry in the changelog for the change. The PR and the author of the change are mentioned as part of the changelog entry.

Input:
- Path to changelog file

Supported changelog formats are:
- `.md`
- `.rst`


### Build project

Build the project's release artifacts.

#### TODO
- Build sdist and wheel via [pep517](https://pypi.org/project/pep517/)

### Commit the changes
Once the above changes are made and the build artifacts can be successfully built, commit the changes that were made.

#### TODO
- Allow for specifying the author details?

### Upload to PyPI
With the checkout and repository in the appropriate state for release, the code can now be built and pushed to PyPI.

Input:
- PyPI token

#### TODO
- Upload via twine

### Create a release on GitHub
Finally, when everything is live, create a release on GitHub to both tag the release in the repository and store the artifacts uploaded to PyPI. The name of the release is the version prepended by `v` and the body of the release is the changelog entry.

#### TODO
- [Upload release artifacts](https://developer.github.com/v3/repos/releases/#upload-a-release-asset)
- Customization of the release name?
