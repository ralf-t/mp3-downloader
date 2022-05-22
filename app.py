# new imports
from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# new function
def download_mp3(URL):
    try:
        yt = YouTube(URL)
        print("\nDownloading...")
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()

        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        print("Success!")
        return new_file
    except Exception as e:
        print(e)
        print("Something went wrong.")
        return None

@app.route("/", methods=['GET','POST'])
def home():

    creator = "Charles Leclerc"
    downloaded_file = None # new

    if request.method == 'POST':
        URL = request.form['URL']
        downloaded_file = download_mp3(URL) # new

    return render_template('/home.html', creator=creator, downloaded_file=downloaded_file) # modified

# new route
@app.route("/download/<string:downloaded_file>")
def download(downloaded_file):
    print(downloaded_file)
    return send_file(downloaded_file, as_attachment=True)