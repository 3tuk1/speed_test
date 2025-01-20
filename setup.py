import subprocess
import sys
import os

def check_and_install_packages():
    requirements_file = "requirements.txt"

    if os.path.exists(requirements_file):
        try:
            print("必要なライブラリをインストールしています...")
            # エンコーディングを指定して requirements.txt を読み込む
            with open(requirements_file, "r", encoding="utf-8") as file:
                requirements = file.read().splitlines()
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
            print("すべてのライブラリが正常にインストールされました。")
        except subprocess.CalledProcessError as e:
            print(f"ライブラリのインストールに失敗しました: {e}")
    else:
        print(f"{requirements_file} が見つかりません。プロジェクトのディレクトリにこのファイルが存在することを確認してください。")

def check_imports():
    try:
        import speedtest
        print("speedtest モジュールがインポート可能です。")
        import ping3
        print("ping3 モジュールがインポート可能です。")
        import schedule
        print("schedule モジュールがインポート可能です。")
        import pandas
        print("pandas モジュールがインポート可能です。")
        import matplotlib
        print("matplotlib モジュールがインポート可能です。")
        print("すべてのモジュールが正常にインポートできました。")
    except ImportError as e:
        print(f"モジュールのインポートに失敗しました: {e}. 必要なライブラリが不足している可能性があります。")
        print("ライブラリをインストールしてください。")

if __name__ == "__main__":
    check_and_install_packages()
    check_imports()
