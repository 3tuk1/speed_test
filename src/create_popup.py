import tkinter as tk
from tkinter import ttk
import speedtest
import logging
from ping3 import ping  # ping3をインポート
from src.speed_test import speedtest_main
from src.utils import get_fqdn

exclude_addresses = ["speedtest.softether.co.jp","jp-nperf.verizon.net"]  # 除外するサーバーのアドレスを指定
shcedule_id = None

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# エラーログ用のファイルハンドラーを追加
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

def create_popup():
    # ポップアップウィンドウの作成
    popup = tk.Tk()
    popup.title("ポップアップウィンドウ")
    popup.geometry("900x600")

    # タブコントロールの作成
    tab_control = ttk.Notebook(popup)

    # メインタブ
    main_tab = ttk.Frame(tab_control)
    tab_control.add(main_tab, text="設定")

    # サブタブ
    sub_tab = ttk.Frame(tab_control)
    tab_control.add(sub_tab, text="詳細")

    tab_control.pack(expand=1, fill="both")

    # メインタブにスライダーを追加
    slider_label = ttk.Label(main_tab, text="計測回数")
    slider_label.pack(pady=10)

    # スライダー値を表示するラベル
    slider_value_label = ttk.Label(main_tab, text="スライダーの値: 1")
    slider_value_label.pack(pady=5)

    # スライダーの作成
    def update_slider_value(event):
        slider_value_label.config(text=f"スライダーの値: {int(slider.get())}")

    slider = ttk.Scale(main_tab, from_=1, to=100, orient="horizontal", command=update_slider_value)
    slider.set(1)
    slider.pack(pady=5)

    # 計測間隔設定
    interval_label = ttk.Label(main_tab, text="計測間隔")
    interval_label.pack(pady=10)

    options1 = [1, 5, 10, 15, 30, 45, 60]
    interval = ttk.Combobox(main_tab, values=options1)
    interval.set(1)
    interval.pack(pady=5)

    try:
        st = speedtest.Speedtest(secure=True)

        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            logger.info("インターネット接続確認OK")
        except Exception as e:
            logger.error(f"ネットワーク接続エラー: {str(e)}")
            raise Exception("インターネット接続が確認できません")

        logger.info("サーバーリスト取得中...")
        servers = st.get_servers()
        logger.info(f"サーバーリスト取得完了: {len(servers)}件")

        # ステップ1: 日本のサーバーを除外リスト適用でフィルタリング
        filtered_servers = {
            sid: info for sid, info in servers.items()
            if info[0].get("host") not in exclude_addresses and info[0].get("cc") == "JP"
        }
        logger.info(f"日本のサーバー数（除外リスト適用）: {len(filtered_servers)}")

        selected_servers = []
        for server_list in filtered_servers.values():
            for server in server_list:
                host = get_fqdn(server)
                selected_servers.append({
                    "host": host,
                    "latency": "未計測",
                    "average_latency": "未計測",
                    "distance": server.get('d', "不明"),
                    "ping_count": 0
                })

        # ステップ2: 日本のサーバーが見つからない場合は除外リストを無視
        if not selected_servers:
            logger.warning("日本のサーバーが見つかりませんでした。除外リストを無視します...")
            filtered_servers = {
                sid: info for sid, info in servers.items()
                if info[0].get("cc") == "JP"  # 除外リストを適用しない
            }
            logger.info(f"日本のサーバー数（除外リストなし）: {len(filtered_servers)}")

            for server_list in filtered_servers.values():
                for server in server_list:
                    host = get_fqdn(server)
                    selected_servers.append({
                        "host": host,
                        "latency": "未計測",
                        "average_latency": "未計測",
                        "distance": server.get('d', "不明"),
                        "ping_count": 0
                    })

        # ステップ3: それでもサーバーが見つからない場合は海外も含める
        if not selected_servers:
            logger.warning("日本のサーバーが見つかりませんでした。海外のサーバーも含めます...")
            filtered_servers = {
                sid: info for sid, info in servers.items()
                if info[0].get("host") not in exclude_addresses  # 除外リスト適用・国コード無視
            }
            logger.info(f"海外含む緩和後のサーバー数: {len(filtered_servers)}")

            for server_list in filtered_servers.values():
                for server in server_list:
                    host = get_fqdn(server)
                    selected_servers.append({
                        "host": host,
                        "latency": "未計測",
                        "average_latency": "未計測",
                        "distance": server.get('d', "不明"),
                        "ping_count": 0
                    })

    except Exception as e:
        logger.error(f"サーバーリスト取得中にエラー発生: {str(e)}")
        raise Exception(f"サーバーリスト取得エラー: {str(e)}")

    # 最終確認
    if not selected_servers:
        logger.error("有効なサーバーが見つかりませんでした")
        raise Exception("有効なサーバーが見つかりません")


    # サーバー選択用のコンボボックス
    options2 = [server['host'] for server in selected_servers]
    options2.insert(0, "選択無し")
    select_server_label = ttk.Label(main_tab, text="選択サーバー")
    select_server_label.pack(pady=10)

    select_server = ttk.Combobox(main_tab, values=options2)
    select_server.set("選択無し")
    select_server.pack(pady=5)

    # サブタブにTreeviewを追加してサーバー情報を表示
    tree = ttk.Treeview(sub_tab, columns=("host", "ping", "average_ping", "distance"), show="headings", height=15)
    tree.heading("host", text="ホスト名")
    tree.heading("ping", text="PING値 (ms)")
    tree.heading("average_ping", text="平均PING (ms)")
    tree.heading("distance", text="距離 (km)")

    for server in selected_servers:
        tree.insert("", "end", values=(server["host"], server["latency"], server["average_latency"], server["distance"]))

    tree.pack(pady=10, fill="both", expand=True)

    # PINGを1秒ごとに更新する関数
    def update_ping():
            for i, server in enumerate(selected_servers):
                host = server["host"]
                latency = ping(host, timeout=1)  # ping3でPING値を計測
                if latency:
                    latency_ms = round(latency * 1000, 2)
                    server["ping_count"] += 1  # 計測回数を増加

                    # 平均PING値を計算
                    if server["ping_count"] == 1:
                        server["average_latency"] = latency_ms
                    else:
                        server["average_latency"] = round(
                            (server["average_latency"] * (server["ping_count"] - 1) + latency_ms) / server["ping_count"], 2
                        )

                    server["latency"] = latency_ms
                else:
                    server["latency"] = "接続不可"

            # Treeviewの内容を更新
            for item, server in zip(tree.get_children(), selected_servers):
                tree.item(item, values=(server["host"], server["latency"], server["average_latency"], server["distance"]))

            # 1秒後に再度実行
            global shcedule_id
            shcedule_id = popup.after(5000, update_ping)

    # 開始ボタンを追加
    def start_measurement():
        global shcedule_id
        selected_server = [
            server for server_list in servers.values() for server in server_list
            if get_fqdn(server) in select_server.get()
        ]
        inv = int(interval.get())
        sli = int(slider.get())
        popup.after_cancel(shcedule_id)
        popup.destroy()
        speedtest_main(sli, inv, selected_server)

    start_button = ttk.Button(main_tab, text="開始", command=start_measurement)
    start_button.pack(pady=20)

    # PINGの更新を開始
    update_ping()

    # ウィンドウのループ
    popup.mainloop()
