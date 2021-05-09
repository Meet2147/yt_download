from flask import Flask, render_template, request, session, redirect, send_file, url_for

from pytube import YouTube

app = Flask(__name__)
app.config['SECRET_KEY'] = "meet"

def download(url):
    video = url.streams.first()
    filepath = video.download()
    return filepath

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        url = YouTube(session['link'])
        
        return render_template("see_video.html",url=url)
    return render_template("index.html")

@app.route("/see_video", methods=['GET','POST'])
def see_video():
    if request.method == 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename, as_attachment=True)
    return redirect(url_for('index'))