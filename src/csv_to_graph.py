import logging
from datetime import date
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .utils import gen_filename

CURDIR = Path.cwd()

# matplotlibのログを警告以上に設定
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logger = logging.getLogger("__main__").getChild(__name__)

def generate_graphs_from_csv(csv_path: Path):
    # PDFファイルのパスを取得
    pdf_path = gen_filename(date.today(), "pdf", "result_pdf")

    # CSVファイルを確認
    if not csv_path.exists():
        raise FileNotFoundError(f"指定されたCSVファイルが見つかりません: {str(csv_path)}")

    # CSVファイルを読み込む
    df = pd.read_csv(csv_path)

    # データが空の場合のチェック
    if df.empty:
        raise ValueError(f"指定されたCSVファイルにはデータがありません: {str(csv_path)}")

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

    logger.info(f"グラフが作成され、PDFに保存されました: {pdf_path}")
