import tkinter as tk
from tkinter import ttk
import speedtest
import logging
import speed_test

exclude_addresses = ["speedtest.softether.co.jp"]  # ここにつくばとかの除外したいサーバーのアドレスを入れる


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
    popup.geometry("600x600")

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
    slider.pack(pady=5)

    # 初期値を1にして
    interval_label = ttk.Label(main_tab, text="計測間隔")
    interval_label.pack(pady=10)

    options1 = ["5", "10", "15", "30", "45", "60"]
    interval = ttk.Combobox(main_tab, values=options1)
    interval.set("1")
    interval.pack(pady=5)

    # メインタブにセレクトサーバーを追加
    select_server_label = ttk.Label(main_tab, text="選択サーバー")
    select_server_label.pack(pady=10)
    st = speedtest.Speedtest()
    servers = st.get_servers()
    if not servers:
        logger.error("サーバーリストを取得できませんでした")
        raise Exception("サーバーリストの取得に失敗しました")

    selected_servers = [
        server for server_list in servers.values() for server in server_list
        if server['host'].split(':')[0] not in exclude_addresses
            if server['cc'] in "JP"
        ]
    if not selected_servers:
        logger.error("有効なサーバーが見つかりませんでした")
        raise Exception("有効なサーバーが見つかりません")
    options2 = [server['host'].split(':')[0] for server in selected_servers]
    select_server = ttk.Combobox(main_tab, values=options2)
    select_server.set("選択無し")
    select_server.pack(pady=5)

    # 開始ボタンを追加
    def start_measurement():
        out_select_server = [
            server for server_list in servers.values() for server in server_list
            if server['host'].split(':')[0] in select_server.get()
        ]
        inv = int(interval.get())
        sli = int(slider.get())
        popup.destroy()
        speed_test.speedtest_main(sli,inv,out_select_server)

    start_button = ttk.Button(main_tab, text="開始", command=start_measurement)
    start_button.pack(pady=20)

    # サブタブにラベルを追加
    sub_label = ttk.Label(sub_tab, text="詳細情報を表示予定だよ！", font=("Arial", 12))
    sub_label.pack(pady=20)

    # ウィンドウのループ
    popup.mainloop()


if __name__ == "__main__":
    create_popup()
