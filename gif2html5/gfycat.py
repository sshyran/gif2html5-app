import requests


def convert_gif(gif_url):
    url = 'http://upload.gfycat.com/transcode?fetchUrl=%s' % gif_url
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        return None

    if not all(k in data for k in ['mp4Url', 'webmUrl']):
        return None

    mp4 = data['mp4Url']
    webm = data['webmUrl']

    return {'mp4': mp4, 'webm': webm}
