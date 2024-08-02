# Ubuntuを使用
FROM ubuntu:24.04

# set up Ubuntu >>>>>>>>>>>>>>>>>>>>>>>>>>
RUN apt-get update && apt-get install -y \
    sudo \
    build-essential \
    tzdata \
    git \
    vim \
    wget \
    curl \
    llvm \
    make \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# 最後にcleanとrmでキャッシュファイルを削除することで，イメージを小さくする
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Setting User >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
# 今回のイメージでは，すでにubuntu(uid: 1000, gid: 1000が作られている)
ARG USER_NAME=green
ARG USER_UID=2000
ARG USER_GID=2000
RUN groupadd -g $USER_GID $USER_NAME \
    && useradd -u $USER_UID -g $USER_GID -m $USER_NAME -s /bin/bash
USER $USER_NAME
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Install Rye >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Rye: https://github.com/astral-sh/rye
# how to install: https://rye.astral.sh/guide/installation/
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
RUN echo 'source "$HOME/.rye/env"' >> ~/.profile
RUN echo 'source "$HOME/.rye/env"' >> ~/.bashrc
# 環境変数にパスを通しておかないとDockerfile内でRyeを実行できない
ENV PATH=/home/$USER_NAME/.rye/shims:${PATH}
# Shell Completion
RUN mkdir -p ~/.local/share/bash-completion/completions
RUN rye self completion > ~/.local/share/bash-completion/completions/rye.bash
# Update Rye
RUN rye self update
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
