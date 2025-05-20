from flask import Flask, request, send_file
import yt_dlp
import os
import glob

app = Flask(__name__)

TEMP_FOLDER = "/data/data/com.termux/files/home/downloads/"

# Make sure temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Instant Video Downloader</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 100px; background: #f4f4f4; }
            input, button {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 16px;
            }
            button {
                background: #28a745;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background: #218838;
            }
            form {
                background: white;
                padding: 20px;
                display: inline-block;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <form method="POST" action="/download">
            <input name="url" placeholder="Paste video URL" required style="width:300px;">
            <button type="submit">Download</button>
        </form>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    # Clean old files
    for f in glob.glob(TEMP_FOLDER + '*'):
        os.remove(f)

    ydl_opts = {
        'outtmpl': TEMP_FOLDER + '%(title).100s.%(ext)s',
        'format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send file directly to user
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"<h3 style='color:red;'>Error: {e}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
