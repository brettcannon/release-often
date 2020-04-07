# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get -qy update && apt-get -qy install git && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH "/app:${PYTHONPATH}"

COPY pyproject.toml .
COPY poetry.lock .
RUN python -m pip install --quiet poetry
RUN poetry config virtualenvs.create false
RUN poetry install --quiet --no-interaction --no-ansi --no-dev

ADD release_often .

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "-m", "release_often"]
