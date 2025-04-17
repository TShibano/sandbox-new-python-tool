#!/bin/zsh
devcontainer up \
  --additional-features='{"ghcr.io/duduribeiro/devcontainer-features/neovim:1": {}}' \
  --mount type=bind,source=$HOME/.config/nvim,target=/home/green/.config/nvim \
  --workspace-folder .

