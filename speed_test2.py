
import time
import os
import datetime
import csv
import schedule
import speedtest
from ping3 import ping
import schedule
import csv_to_graph as ctg
times = 0
test_count = 0


def calculate_jitter(ping_list):
    """PingのリストからJitterを計算"""
    if len(ping_list) < 2:
        return 0.0
    differences = [abs(ping_list[i] - ping_list[i - 1]) for i in range(1, len(ping_list))]
    return sum(differences) / len(differences)


def best_server_select(st):
    print("サーバーリストを取得中...")
    st.get_servers()
    best_server = st.get_best_server()
    best_address = best_server.get("host", "").split(":")[0]
    print(f"最適なサーバー: {best_server['host']} ({best_server['country']})")
    return best_address


def create_directory():
    directory = "result_csv"
    base_name = datetime.date.today()
    ext = ".csv"
    try:
        if not os.path.exists(directory):
            print("フォルダの作成")
            os.makedirs(directory)

        file_name = f"{base_name}{ext}"
        file_path = os.path.join(directory, file_name)
        counter = 1

        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
            counter += 1

        with open(file_path, 'w', newline='', encoding="utf-8") as file:
            fileheader = ["download_speed", "upload_speed", "PING", "JITTER","CONECT_SERVER","TIME"]
            writer = csv.DictWriter(file, fieldnames=fileheader)
            writer.writeheader()

        print(f"空のファイル '{file_path}' が作成されました。")
        return os.path.abspath(file_path)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None


def test_speed(st, file_abs, best_address):
    

    global test_count
    test_count += 1

    download_speed = st.download() / 1_000_000  # Mbpsに変換
    upload_speed = st.upload() / 1_000_000  # Mbpsに変換

    ping_values = []
    for _ in range(5):
        result = ping(best_address, timeout=1)
        if result is not None:
            ping_values.append(result * 1000)  # 秒からミリ秒に変換
        time.sleep(1)

    average_ping = sum(ping_values) / len(ping_values) if ping_values else 0
    jitter = calculate_jitter(ping_values)

    
    with open(file_abs, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([download_speed, upload_speed, average_ping, jitter,best_address,datetime.datetime.now()])
    



def main():
    print("インターネット回線速度を計測します。\n")
    try:
        
        global times

        st = speedtest.Speedtest()
        best_address = best_server_select(st)
        file_abspath = create_directory()
        while True:
            print("1 ~ 60間の整数にしてください")
            interval = int(input('計測時間の間隔を入力してください(分) : '))
            if (interval >= 1)&(interval <= 60) :
                break
        while True:
            print("1 ~ 60間の整数にしてください")
            times = int(input('計測回数を入力してください : '))
            if (times >= 1)&(times <= 60) :
                break
            print("もう一度入力して")

        test_speed(st, file_abspath, best_address)
        schedule.every(interval).minutes.do(lambda: test_speed(st, file_abspath, best_address))

        while True:
            schedule.run_pending()
            if test_count >= times:
                ctg.generate_graphs_from_csv(file_abspath)
                print("終了")
                break
            time.sleep(60)
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
