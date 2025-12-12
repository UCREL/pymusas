FROM ubuntu:latest


RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-dev \
    git \
    make \
    wget \
    vim \
    build-essential \
    openssh-client \
    ca-certificates \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=ubuntu

USER $USERNAME
WORKDIR /home/$USERNAME


SHELL ["/bin/bash", "-c"]
RUN set -o pipefail \
    && wget -qO- https://astral.sh/uv/install.sh \
    | sh
RUN set -o pipefail \
    && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh \
    | bash
# Required as when using a mount with write permissions in a RUN command 
# it fails because of permission reasons.
COPY --chown=ubuntu:ubuntu docs docs
RUN source .nvm/nvm.sh \
    && nvm install 24 \
    && corepack enable yarn \
    && cd docs \
    && corepack use yarn \
    && cd .. \
    && rm -rf docs

ENV PATH="/home/$USERNAME/.local/bin/:$PATH"

RUN uv python install 3.11

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --index=https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match --python=3.12 --no-install-project --no-install-workspace --all-extras