# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# pythonイメージを使用
FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

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

# Setting User >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Download the latest installer
USER root
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN chmod a+x /uv-installer.sh && chown $USER_NAME:$USER_NAME /uv-installer.sh
USER $USER_NAME
# Run the installer then remove it
RUN sh /uv-installer.sh #&& rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/green/.local/bin/:$PATH"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
