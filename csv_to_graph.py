import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_directory_and_generate_pdf(csv_file):
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
    
    return pdf_path

def generate_graphs_from_csv(csv_path):
    pdf_path=create_directory_and_generate_pdf()
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # PDF出力用のPDFファイルオブジェクトを作成
    with PdfPages(pdf_path) as pdf:
        # ダウンロード速度と時間のグラフ
        plt.figure()
        plt.plot(df['TIME'], df['download_speed'], marker='o', color='b', label='Download Speed (Mbps)')
        plt.xlabel('Time')
        plt.ylabel('Download Speed (Mbps)')
        plt.title('Download Speed over Time')
        plt.xticks(rotation=45)
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
        plt.xticks(rotation=45)
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
        plt.xticks(rotation=45)
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
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        pdf.savefig()
        plt.close()

# 使用例:
# create_directory_and_generate_pdf('your_file.csv')
