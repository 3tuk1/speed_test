import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging

# matplotlibのログを警告以上に設定
logging.getLogger('matplotlib').setLevel(logging.WARNING)

pdf_path = ""

def create_directory_and_generate_pdf():
    global pdf_path
    # 日付を取得
    today = datetime.date.today()
    
    # 保存先ディレクトリを指定
    directory = 'result_pdf'
    
    # ディレクトリが存在しない場合に作成
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # PDFファイル名の作成
    base_pdf_name = f"{today}.pdf"
    pdf_path = os.path.join(directory, base_pdf_name)
    
    # 同名のPDFが存在する場合、数字を追加して新しい名前にする
    counter = 1
    while os.path.exists(pdf_path):
        new_pdf_name = f"{today}_{counter}.pdf"
        pdf_path = os.path.join(directory, new_pdf_name)
        counter += 1


def generate_graphs_from_csv(csv_path):
    # PDFファイルのパスを取得
    create_directory_and_generate_pdf()

    # CSVファイルを確認
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"指定されたCSVファイルが見つかりません: {csv_path}")

    # CSVファイルを読み込む
    df = pd.read_csv(csv_path)

    # データが空の場合のチェック
    if df.empty:
        raise ValueError(f"指定されたCSVファイルにはデータがありません: {csv_path}")

    # TIMEカラムをdatetime型に変換（例: 時間データがある場合）
    if 'TIME' in df.columns:
        try:
            df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M', errors='coerce')
        except Exception as e:
            raise ValueError(f"TIMEカラムの形式が正しくありません: {e}")

    # PDF出力用のPDFファイルオブジェクトを作成
    with PdfPages(pdf_path) as pdf:
        # ダウンロード速度と時間のグラフ
        plt.figure()
        plt.plot(df['TIME'], df['download_speed'], marker='o', color='b', label='Download Speed (Mbps)')
        plt.xlabel('Time')
        plt.ylabel('Download Speed (Mbps)')
        plt.title('Download Speed over Time')
        plt.tight_layout()
        plt.legend()
        pdf.savefig()
        plt.close()

        # アップロード速度と時間のグラフ
        plt.figure()
        plt.plot(df['TIME'], df['upload_speed'], marker='o', color='g', label='Upload Speed (Mbps)')
        plt.xlabel('Time')
        plt.ylabel('Upload Speed (Mbps)')
        plt.title('Upload Speed over Time')
        plt.tight_layout()
        plt.legend()
        pdf.savefig()
        plt.close()

        # PINGと時間のグラフ
        plt.figure()
        plt.plot(df['TIME'], df['PING'], marker='o', color='r', label='Ping (ms)')
        plt.xlabel('Time')
        plt.ylabel('Ping (ms)')
        plt.title('Ping over Time')
        plt.tight_layout()
        plt.legend()
        pdf.savefig()
        plt.close()

        # JITTERと時間のグラフ
        plt.figure()
        plt.plot(df['TIME'], df['JITTER'], marker='o', color='purple', label='Jitter (ms)')
        plt.xlabel('Time')
        plt.ylabel('Jitter (ms)')
        plt.title('Jitter over Time')
        plt.tight_layout()
        plt.legend()
        pdf.savefig()
        plt.close()

    print(f"グラフが作成され、PDFに保存されました: {pdf_path}")
