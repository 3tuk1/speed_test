import logging

import speedtest

from src.speed_test import  speedtest_main

exclude_addresses = ["speedtest.softether.co.jp","jp-nperf.verizon.net"]  # 除外するサーバーのアドレスを指定

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# エラーログ用のファイルハンドラーを追加
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)




def no_gui_do():
    while True:
        interval = int(input("計測間隔を分単位で入力してください: "))
        measurement_count = int(input("計測回数を入力してください: "))
        from datetime import datetime, timedelta
        end_time = datetime.now() + timedelta(minutes=interval * measurement_count)
        print(f"終了想定日時: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        proceed = input("次へ進みますか？ (Y/N): ").strip().upper()
        if proceed == "Y":
            break


    from ping3 import ping
    st = speedtest.Speedtest(secure=True)
    servers = st.get_servers()
    servers = {
        sid: info for sid, info in servers.items()
        if info[0].get("host") not in exclude_addresses and info[0].get("cc") == "JP"
    }

    for i, (server_id, server_info) in enumerate(servers.items(), start=1):
        server = server_info[0]
        # ポート番号を除去
        base_host = server["host"].split(':')[0]
        latency_val = ping(base_host, timeout=1)
        server["latency"] = round(latency_val * 1000, 2) if latency_val else "接続不可"
        print(f"{i} | {server['host']} | {server.get('d', 'N/A')} | {server['latency']}")

    selected_number = int(input("サーバー番号を入力してください: "))
    if 1 <= selected_number <= len(servers):
        target_host = list(servers.items())[selected_number - 1][1][0]['host']
        selected_server = [
            srv for srv_list in servers.values() for srv in srv_list
            if srv['host'] == target_host
        ]
    else:
        print("無効な番号です。終了します。")
        return

    speedtest_main(measurement_count, interval, selected_server)