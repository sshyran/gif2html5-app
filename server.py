from flask import Flask, request, jsonify
import urllib.request
import urllib.error
import urllib.parse
import os
import json
import logging
import requests
import sys

from gif2html5.s3_manager import S3Manager
from gif2html5.config_parser import get_config
from gif2html5.video_manager import convert as convert_gif
from gif2html5.celery import make_celery


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('boto').setLevel(logging.CRITICAL)

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


@celery.task(bind=False, default_retry_delay=30)
def convert_video(gif_url, webhook):
    logging.debug('Converting video')
    parsed = urllib.parse.urlparse(webhook)
    logging.debug('Converting: {}'.format(gif_url))
    logging.debug('Parsed webhook: {}'.format(parsed))

    if parsed.query:
        queries = urllib.parse.parse_qs(parsed.query)
        if 'attachment_id' in queries:
            try:
                attachment_id = queries['attachment_id'][0]
                result = convert_gif(gif_url)

                resources = upload_resources(result)
                resources['attachment_id'] = attachment_id
                logging.debug('Responding with payload: {}'.format(resources))
                requests.post(webhook, data=resources)
                return
            except Exception as exc:
                logging.debug('Retrying: Gif:{url} and Webhook:{webhook}'.format(url=gif_url, webhook=webhook))
                convert_video.retry(exc=exc)
                return

    logging.debug('Missing attachment_id')
    requests.post(webhook, data={
        'message': 'It looks like you are missing attachment_id'})


@app.route("/convert", methods=["POST"])
def convert():
    if not request.data:
        logging.debug('Empty request data')
        return 'Error', 406

    json_request = None

    try:
        json_request = json.loads(request.data.decode('utf-8'))
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

    url = json.loads(request.data.decode('utf-8'))['url']
    logging.debug('Request for conversion: {}'.format(url))

    if 'webhook' in json_request:
        logging.debug('Delaying request via webhook')
        webhook = json.loads(request.data.decode('utf-8'))['webhook']
        result = convert_video.delay(url, webhook)
        return 'Success', 200
    else:
        result = convert_gif(url)
        resources = upload_resources(result)

        logging.debug('Responding with payload: {}'.format(resources))

        return jsonify(resources), 200

    return 'Success', 200


def upload_resources(result):
    return {k: s3Manager.upload(os.path.basename(v), v) for k, v in result.items()}


if __name__ == "__main__":
    app.run()
