# Sandbox New Python Tools

Pythonの新しいツールを試すためのDocker + devcontainerを使った環境を提供する．
Pythonの環境は[Rye](https://github.com/astral-sh/rye?tab=readme-ov-file)で設定する．

## Set up Python environment

1. Dockerをインストールする
1. VScodeをインストールし，Dev Containers(Microsoft)の拡張機能を入れる
1. リポジトリをクローンする
1. VScodeでプロジェクトのルートディレクトリを開く
1. コマンドパレット(`Ctrl+Shit+P`)を開き，"Dev Container: Rebuild Container"を選択する
1. 新しいウィンドウでVSCodeが立ち上がる．コンテナ内のユーザ名は `green` としている．
1. VSCodeの拡張機能で"Jupyter"を入れているため，マジックコマンド `# %%` を使うことで，セル実行することができる
．(https://code.visualstudio.com/docs/python/jupyter-support-py)

### Option
* コンテナ内への拡張機能は下記をインストールするようにしている．必要に応じて追加・削除すること
    * ms-python.python
    * ms-toolsai.jupyter
    * charliermarsh.ruff
    * njpwerner.autodocstring
    * mhutchie.git-graph
* コンテナ内からGitHubへアクセスしたい場合，下記を参考にすること
    * https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=mac
 

## How to Use Rey

Pythonのバージョン変更する
```
rye pin <python-version>
```

Pythonライブラリの追加
```
rye add <python-library>
rye sync
```

Pythonライブラリの削除
```
rye remove <python-library>
rye sync
```
