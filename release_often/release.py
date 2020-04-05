async def create(gh, releases_url, version, body):
    # https://developer.github.com/v3/repos/releases/#create-a-release
    details = {"tag_name": f"v{version}", "body": body}
    result = await gh.post(releases_url, data=details)
    return result["upload_url"]


async def add_artifact(gh, artifact_path):
    # XXX https://developer.github.com/v3/repos/releases/#upload-a-release-asset
    # XXX Requires changes to gidgethub for content-type upload
    # XXX application/gzip, application/zip
    ...
