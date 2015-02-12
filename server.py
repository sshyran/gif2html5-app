from flask import Flask, request, jsonify
from moviepy.editor import *
from src.s3_manager import S3Manager
from src.config_parser import get_config
import urllib2
import os,binascii

app = Flask(__name__)
app.debug = True

@app.route("/convert", methods=["GET"])
def convert():
    config = get_config()
    aws_access = config.get('AWS_ACCESS_KEY_ID')
    aws_secret = config.get('AWS_SECRET_ACCESS_KEY')
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
    s3_path_to_mp4 = s3Manager.upload(random_filename, random_movie_name)

    return jsonify(mp4=s3_path_to_mp4)

if __name__ == "__main__":
    app.run()
