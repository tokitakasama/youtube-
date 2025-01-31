from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os
import time
import schedule
import threading

app = Flask(__name__)

# 動画の保存ディレクトリ
VIDEO_DIR = "static/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

# 動画の削除までの時間（秒）
DELETE_AFTER = 3600  # 1時間

def delete_video(filepath):
    """
    指定したファイルを削除する
    """
    try:
        os.remove(filepath)
        print(f"{filepath} を削除しました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def schedule_delete(filepath):
    """
    削除タイマーを設定する
    """
    schedule.every(1).seconds.do(delete_video, filepath)  # 1秒後に実行

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# スケジューラースレッドの起動
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.default_filename
        filepath = os.path.join(VIDEO_DIR, filename)
        stream.download(output_path=VIDEO_DIR)

        # 削除タイマーを設定
        schedule_delete(filepath)

        return render_template("index.html", video_path=filename)
    except Exception as e:
        return render_template("index.html", error=str(e))

@app.route("/video/<filename>")
def video(filename):
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
