import time
import os
from datetime import datetime
import csv
import schedule
import speedtest
from ping3 import ping
import csv_to_graph as ctg
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# エラーログ用のファイルハンドラーを追加
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

test_count = 0
selected_server = None

# 最初に選択したサーバー情報を保存する変数


def calculate_jitter(ping_list):
    """PingのリストからJitterを計算"""
    if len(ping_list) < 2:
        return 0.0
    differences = [abs(ping_list[i] - ping_list[i - 1]) for i in range(1, len(ping_list))]
    return sum(differences) / len(differences)

def create_directory():
    directory = "result_csv"
    base_name = datetime.now().strftime("%Y-%m-%d")
    ext = ".csv"
    try:
        if not os.path.exists(directory):
            logger.info("フォルダの作成")
            os.makedirs(directory)

        file_name = f"{base_name}{ext}"
        file_path = os.path.join(directory, file_name)
        counter = 1

        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
            counter += 1

        with open(file_path, 'w', newline='', encoding="utf-8") as file:
            fileheader = ["download_speed", "upload_speed", "PING", "JITTER", "CONECT_SERVER", "TIME"]
            writer = csv.DictWriter(file, fieldnames=fileheader)
            writer.writeheader()

        logger.info(f"空のファイル '{file_path}' が作成されました。")
        return os.path.abspath(file_path)
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise Exception("ディレクトリ作成に失敗しました")

def test_speed(st, file_abs, selecte_server):
    
    global test_count,selected_server
    test_count += 1

    if not selected_server:
      selected_server = st.get_best_server(selecte_server)

    if selected_server:
        logger.info("ダウンロード速度計測中")
        download_speed = st.download() / 1_000_000
        if download_speed <= 0:
            logger.error("ダウンロード速度が0Mbps以下です")
            raise Exception("ダウンロード速度が異常です")

        logger.info("アップロード速度計測中")
        upload_speed = st.upload() / 1_000_000
        if upload_speed <= 0:
            logger.error("アップロード速度が0Mbps以下です")
            raise Exception("アップロード速度が異常です")

        logger.info("PING計測中")
        ping_values = []
        for _ in range(5):
            result = ping(selected_server["host"].split(':')[0], timeout=1)
            if result is not None:
                ping_values.append(result * 1000)
            time.sleep(1)

        if not ping_values:
            logger.error("PINGの計測に失敗しました")
            raise Exception("PINGの計測に失敗しました")

        average_ping = sum(ping_values) / len(ping_values) if ping_values else 0
        jitter = calculate_jitter(ping_values)

        with open(file_abs, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([download_speed, upload_speed, average_ping, jitter, selected_server["host"].split(':')[0], datetime.now().strftime("%H:%M")])
        logger.info(f"{test_count}回目の計測が終了しました")
    else:
        logger.warning("サーバーが見つかりませんでした。")
        raise Exception("サーバーが見つかりませんでした")

def speedtest_main(times,interval,select_server):

    
    st = speedtest.Speedtest()
    file_abspath = create_directory()

    test_speed(st, file_abspath,select_server)
    schedule.every(interval).minutes.do(lambda: test_speed(st, file_abspath,select_server))

    try:
        while test_count < times:
            schedule.run_pending()
            time.sleep(60)
        ctg.generate_graphs_from_csv(file_abspath)
        logger.info("終了")
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
