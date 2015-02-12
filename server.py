from flask import Flask
from flask import request
from flask import render_template
from moviepy.editor import *
from src.s3_manager import S3Manager
import urllib2
import os,binascii

app = Flask(__name__)
app.debug = True

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["filedata"]
    file.save("/tmp/movie.gif")

    video = VideoFileClip("/tmp/movie.gif")

    result = CompositeVideoClip([video])
    result.write_videofile("/tmp/movie.mp4")

    return "Upload successful"

@app.route("/")
def tryme():
    return render_template("tryout.html")

@app.route("/convert", methods=["GET"])
def convert():
    aws_access = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3Manager = S3Manager(aws_access, aws_secret)

    random_filename = binascii.b2a_hex(os.urandom(15))
    url = request.args.get("url", "")
    response = urllib2.urlopen(url)
    contents = response.read()

    saving_name = "./tmp/%s.gif" % (random_filename)
    f = open(saving_name, 'wb')
    f.write(contents)
    f.close()

    video = VideoFileClip(saving_name)

    result = CompositeVideoClip([video])
    random_movie_name = "./tmp/%s.mp4" % (random_filename)
    result.write_videofile(random_movie_name)

    s3Manager.upload(random_filename, random_movie_name)

    return "https://s3.amazonaws.com/fusion-gif2html5-mp4/%s" %s (random_filename)

if __name__ == "__main__":
    app.run()
