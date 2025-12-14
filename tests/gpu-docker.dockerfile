FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04

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

ENV PATH="/home/$USERNAME/.local/bin/:$PATH"

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --python=3.12 --no-install-project --no-install-workspace --all-extras
RUN uv pip install --python=3.12 spacy[cuda12x]
COPY --chown=ubuntu:ubuntu pymusas ./pymusas
COPY --chown=ubuntu:ubuntu tests ./tests
COPY --chown=ubuntu:ubuntu pyproject.toml pyproject.toml
COPY --chown=ubuntu:ubuntu .python-version .python-version
RUN touch README.md LICENSE
RUN uv version --bump patch

ENTRYPOINT ["./tests/docker_gpu_run_script.sh"]