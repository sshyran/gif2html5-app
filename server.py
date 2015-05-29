from flask import Flask, request, jsonify
from src.s3_manager import S3Manager
from src.config_parser import get_config
from src.video_manager import VideoManager
from celery import Celery
import urllib2
import os, binascii
import json
import logging
import requests
import sys
import urlparse
import tempfile
from gfycat.gfycat import gfycat

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
    CELERY_RESULT_BACKEND=config.get('REDISTOGO_URL'),
    API_KEY=config.get('GIF2HTML5_API_KEY'),
)
celery = make_celery(app)

@celery.task()
def convert_video(gif_url, webhook):
    logging.debug('Converting video')
    parsed = urlparse.urlparse(webhook)
    logging.debug('Parsed webhook: {}'.format(parsed))

    if parsed.query:
        queries = urlparse.parse_qs(parsed.query)
        if 'attachment_id' in queries:
            attachment_id = queries['attachment_id'][0]
            gif_filepath = saving_to_local(gif_url)
            result = VideoManager().convert(gif_filepath)
            
            resources = upload_resources(result)
            resources['attachment_id'] = attachment_id
            logging.debug('Responding with payload: {}'.format(resources))
            requests.post(webhook, data=resources)
            return

    logging.debug('Missing attachment_id')
    requests.post(webhook, data={
        'message' : 'It looks like you are missing attachment_id'})

@app.route("/convert", methods=["POST"])
def convert():
    if not request.data:
        logging.debug('Empty request data')
        return 'Error', 406

    json_request = None

    try:
        json_request = json.loads(request.data)
    except ValueError:
        logging.debug('Invalid JSON request')
        return 'JSON is not correct please check again', 406

    if app.config.get('API_KEY'):
        if json_request.get('api_key') != app.config.get('API_KEY'):
            logging.debug('Bad API key')
            return 'Unauthorized', 401

    if 'url' not in json_request:
        logging.debug('No URL specified')
        return 'url property is not present in the payload', 406

    url = json.loads(request.data)['url']
    logging.debug('Request for conversion: {}'.format(url))

    if 'webhook' in json_request:
        logging.debug('Delaying request via webhook')
        webhook = json.loads(request.data)['webhook']
        result = convert_video.delay(url, webhook)
        return 'Success', 200
    else:
        gif_filepath = saving_to_local(url)
        result = VideoManager().convert(gif_filepath)
        resources = upload_resources(result)
        
        logging.debug('Responding with payload: {}'.format(resources))

        return jsonify(resources), 200

    return 'Success', 200

def upload_resources(result):
    return {k: s3Manager.upload(os.path.basename(v), v) for k, v in result.iteritems()}

def saving_to_local(url):
    tempdir = tempfile.gettempdir()
    response = urllib2.urlopen(url)
    contents = response.read()

    random_filename = binascii.b2a_hex(os.urandom(15))

    gif_filepath = "%s/%s.gif" % (tempdir, random_filename)
    gif_file = open(gif_filepath, 'wb')
    gif_file.write(contents)
    gif_file.close()

    return gif_filepath

if __name__ == "__main__":
    app.run()
