FROM nvidia/cuda:13.2.1-cudnn-devel-ubuntu24.04

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
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

RUN uv self update
RUN uv python install 3.14
RUN uv venv --python=3.14 --no-project \
    && uv pip install torch --index-url https://download.pytorch.org/whl/cu132

COPY --chown=ubuntu:ubuntu pymusas ./pymusas
COPY --chown=ubuntu:ubuntu tests ./tests
COPY --chown=ubuntu:ubuntu pyproject.toml pyproject.toml
RUN touch README.md LICENSE
# spaCy has no cuda13x extra and its cuda12x extra caps cupy below 13, which has
# no Python 3.13/3.14 wheels, so cupy is installed directly.
RUN uv pip install .[neural] "cupy-cuda13x>=14" --group dev

ENTRYPOINT ["./tests/docker_gpu_run_script.sh"]
