import subprocess
import sys

def check_and_install_packages():
    try:
        import speedtest
        print("speedtest import")
        import ping3
        print("ping3 import")
        import schedule
        print("schedule import")
        import pandas
        print("pandas import")
        import matplotlib
        print("matplotlib import")
    except ImportError:
        print("ライブラリをインストールします...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "speedtest-cli", "ping3"])

if __name__ == "__main__":
    check_and_install_packages()