from flask import Flask, request, jsonify
from moviepy.editor import *
from src.s3_manager import S3Manager
from src.config_parser import get_config
from src.video_manager import VideoManager
from celery import Celery
import urllib2
import os,binascii
import json
import requests
import urlparse

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

config = get_config()
s3Manager = S3Manager(config)
app = Flask(__name__)

# app.debug = True
app.config.update(
    CELERY_BROKER_URL=config.get('REDISTOGO_URL'),
    CELERY_RESULT_BACKEND=config.get('REDISTOGO_URL')
)
celery = make_celery(app)

@celery.task()
def convert_video(gif_url, webhook):
    parsed = urlparse.urlparse(webhook)
    attachment_id = urlparse.parse_qs(parsed.query)['attachment_id'][0]

    gif_filepath = saving_to_local(gif_url)
    result = VideoManager().convert(gif_filepath)

    s3_path_to_mp4 = s3Manager.upload(result.mp4, "./tmp/%s" % result.mp4)
    s3_path_to_png = s3Manager.upload(result.snapshot, "./tmp/%s" % result.snapshot)

    payload = {'mp4': s3_path_to_mp4, 'snapshot': s3_path_to_png, 'attachment_id': attachment_id}
    requests.post(webhook, data=payload)

@app.route("/convert", methods=["POST"])
def convert():
    if not request.data:
        return 'Error', 406

    json_request = None

    try:
        json_request = json.loads(request.data)
    except ValueError, e:
        return 'JSON is not correct please check again', 406

    if 'url' not in json_request:
        return 'url property is not present in the payload', 406

    url = json.loads(request.data)['url']

    if 'webhook' in json_request:
        webhook = json.loads(request.data)['webhook']
        result = convert_video.delay(url, webhook)
        return 'Success', 200
    else:
        gif_filepath = saving_to_local(url)
        result = VideoManager().convert(gif_filepath)
        s3_path_to_mp4 = s3Manager.upload(result.mp4, "./tmp/%s" % result.mp4)
        s3_path_to_png = s3Manager.upload(result.snapshot, "./tmp/%s" % result.snapshot)
        return jsonify(mp4=s3_path_to_mp4, snapshot=s3_path_to_png), 200

    return 'Success', 200

def saving_to_local(url):
    response = urllib2.urlopen(url)
    contents = response.read()

    random_filename = binascii.b2a_hex(os.urandom(15))

    gif_filepath = "./tmp/%s.gif" % (random_filename)
    f = open(gif_filepath, 'wb')
    f.write(contents)
    f.close()

    return gif_filepath

if __name__ == "__main__":
    app.run()
