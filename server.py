from flask import Flask
from flask import request
from flask import render_template
from moviepy.editor import *

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['filedata']
    file.save('/tmp/movie.gif')

    video = VideoFileClip("/tmp/movie.gif")

    result = CompositeVideoClip([video]) # Overlay text on video
    result.write_videofile("/tmp/movie.mp4") # Many options...

    return 'Upload successful'

@app.route("/")
def tryme():
    return render_template('tryout.html')

if __name__ == "__main__":
    app.run()
