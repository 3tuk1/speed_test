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
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        logger.info("インターネット接続確認OK")
    except Exception as e:
        logger.error(f"ネットワーク接続エラー: {str(e)}")
        raise Exception("インターネット接続が確認できません")

    while True:
        try:
            logger.info("サーバーリスト取得中...")
            servers = st.get_servers()
            logger.info(f"サーバーリスト取得完了: {len(servers)}件")

            # まずは日本のサーバーを除外リストを適用してフィルタリング
            filtered_servers = {
                sid: info for sid, info in servers.items()
                if info[0].get("host") not in exclude_addresses and info[0].get("cc") == "JP"
            }

            logger.info(f"日本のサーバー数: {len(filtered_servers)}")

            # 日本のサーバーが見つからない場合は条件を緩和（除外リストのみ適用）
            if not filtered_servers:
                logger.warning("日本のサーバーが見つかりませんでした。除外リストのみ適用します...")
                filtered_servers = {
                    sid: info for sid, info in servers.items()
                    if info[0].get("host") not in exclude_addresses and info[0].get("cc") == "JP"
                }
                logger.info(f"除外リスト適用後のサーバー数: {len(filtered_servers)}")

            # それでもサーバーが見つからない場合は海外も含める
            if not filtered_servers:
                logger.warning("日本のサーバーが見つかりませんでした。海外のサーバーも含めます...")
                filtered_servers = {
                    sid: info for sid, info in servers.items()
                    if info[0].get("host") not in exclude_addresses
                }
                logger.info(f"海外含む緩和後のサーバー数: {len(filtered_servers)}")

            # サーバーがまだ見つからない場合はエラー
            if not filtered_servers:
                logger.error("有効なサーバーが見つかりませんでした")
                raise Exception("有効なサーバーが見つかりません")

            # PINGを計測してサーバー一覧を表示
            server_list = []
            print(f"0 | 再検索")
            print(f"1 | 終了")
            for i, (server_id, server_info) in enumerate(filtered_servers.items(), start=2):
                server = server_info[0]
                base_host = server["host"].split(':')[0]
                latency_val = ping(base_host, timeout=1)
                server["latency"] = round(latency_val * 1000, 2) if latency_val else "接続不可"
                country_code = server.get("cc", "??")
                print(f"{i} | {server['host']} | {server.get('d', 'N/A')} | {server['latency']} | 国: {country_code}")
                server_list.append((server_id, server_info))

            selected_number = int(input("サーバー番号を入力してください: "))
            if selected_number == 1:
                print("終了します。")
                return
            if 1 <= selected_number <= len(server_list):
                target_host = server_list[selected_number - 1][1][0]['host']
                selected_server = [
                    srv for srv_list in filtered_servers.values() for srv in srv_list
                    if srv['host'] == target_host
                ]
                break

            else:
                print("無効な番号です。")



        except Exception as e:
            logger.error(f"エラーが発生しました: {e}")
            print(f"エラー: {e}")
            return

    speedtest_main(measurement_count, interval, selected_server)