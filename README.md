
# speed_test

## 概要

`speed_test` は、インターネット回線速度を計測するためのツールです。LINUXおよびWINDOWSの両環境で動作します。distフォルダ内の実行可能ファイル（`speed_test2.exe`）を使用して、回線速度のテストを行うことができます。

## 実行方法

### LINUXの場合

1. `dist` フォルダ内にある実行ファイル `speed_test2.exe` を実行します。

   ```bash
   ./dist/speed_test2.exe
   ```

2. 実行に必要な権限がない場合、以下のコマンドで実行権限を追加します：

   ```bash
   chmod +x ./dist/speed_test2.exe
   ```

### WINDOWSの場合

1. `dist` フォルダ内にある実行ファイル `speed_test2.exe` をダブルクリックするか、コマンドラインで実行します。

   ```cmd
   ./dist/speed_test2.exe
   ```

### Python 環境のセットアップ（実行できない場合）

もし実行できない場合は、Python環境を構築し、以下の手順に従ってください。

#### WINDOWS環境での実行方法

1. `start_windows.bat` を実行して、依存関係のインストールと実行を行います。

   ```cmd
   start_windows.bat
   ```

#### LINUX環境での実行方法

1. `start_LINUX.sh` を実行して、依存関係のインストールと実行を行います。

   ```bash
   ./start_LINUX.sh
   ```

### 必要な依存関係

以下のPythonパッケージが必要です：

- `speedtest-cli`
- `ping3`
- `schedule`
- `csv_to_graph`

依存関係が不足している場合、以下のコマンドでインストールできます：

setup.pyを実行することで依存関係のインストールが可能です

## 注意点

- 実行する際は、管理者権限が必要な場合があります。権限が不足している場合、エラーが発生することがあります。
- `speed_test2.exe` は、実行する前にインターネット接続を確認してください。

## サポート

何か問題が発生した場合は、GitHubの[Issueトラッカー](https://github.com/your_repo/issues)を使用して報告してください。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)のもとで公開されています。
