FROM python:3.12.0-slim-bullseye AS builder

ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

RUN pip install --no-cache-dir poetry==1.7.1

WORKDIR /build

COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev


FROM python:3.12.0-slim-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN DEBIAN_FRONTEND=noninteractive \
	apt-get update && \
	apt-get -y upgrade && \
    apt-get install tini && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG USERNAME="bot"
ARG UID=1500

# switch to non-root user
RUN useradd \
    --create-home \
    --no-log-init \
    --shell /bin/bash \
    --system \
    --user-group ${USERNAME} \
    --uid ${UID} && \
    chown --recursive ${USERNAME}:${USERNAME} /app

# use UID instead of USERNAME to allow Kubernetes recognising it as non-root user
USER ${UID}

ENV HOME=/app \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder /build/.venv ${VIRTUAL_ENV}
COPY bot.py .

ENTRYPOINT [ "tini", "./bot.py" ]
