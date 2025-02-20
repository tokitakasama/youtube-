from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        m3u8_url = request.form['m3u8_url']
        try:
            # m3u8ファイルの内容を取得
            response = requests.get(m3u8_url)
            response.raise_for_status()  # エラーが発生した場合は例外を発生させる
            m3u8_content = response.text

            # m3u8ファイルの内容を解析し、ストリームのURLを取得
            stream_url = get_stream_url(m3u8_content)

            return render_template('player.html', stream_url=stream_url)
        except requests.exceptions.RequestException as e:
            return render_template('index.html', error=f"Error: {e}")
        except ValueError as e:
            return render_template('index.html', error=f"Invalid m3u8 URL: {e}")

    return render_template('index.html')

def get_stream_url(m3u8_content):
    """m3u8ファイルの内容からストリームのURLを抽出する"""
    lines = m3u8_content.splitlines()
    for line in lines:
        if line.startswith('http'):
            return line
    raise ValueError("No stream URL found in m3u8 file")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
