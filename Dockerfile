# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get -qy update && apt-get -qy install git && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

WORKDIR /app

RUN python -m pip --disable-pip-version-check --no-cache-dir --quiet install poetry && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
# In case GitHub Actions ever starts caching intermediate containers, install the source in a separate step.
RUN poetry install --quiet --no-interaction --no-ansi --no-dev --no-root

ADD release_often ./release_often
ENV PYTHONPATH "/app:${PYTHONPATH}"

# When GitHub executes this action, CWD is set to $GITHUB_WORKSPACE, **not** WORKDIR.
ENTRYPOINT ["python", "-m", "release_often"]
