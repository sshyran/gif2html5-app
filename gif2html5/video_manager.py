import urllib.request, urllib.error, urllib.parse
import os, uuid, tempfile

from os.path import basename
from moviepy.editor import *
from PIL import Image, ImageFile

from gif2html5.gfycat import convert_gif
from gif2html5.exceptions.bad_content_type import BadContentType


def convert(gif_url):
    codecs = ['mp4', 'ogv', 'webm']

    gif_path = save_to_local(gif_url)
    
    tempdir = tempfile.gettempdir()
    f = basename(gif_path)
    f_without_ext = os.path.splitext(f)[0]
    
    urlopener = urllib.request.URLopener()
    converted_gif = convert_gif(gif_url)
    
    list_of_files = dict([(codec, "%s/%s.%s"  % (tempdir, f_without_ext, codec))for codec in codecs])

    saving_snapshot_filename = os.path.join(tempdir, "%s.jpg" % f_without_ext)

    video = VideoFileClip(gif_path)
    video.save_frame(saving_snapshot_filename)
    
    compress_image(saving_snapshot_filename)
    
    for filename in list(list_of_files.values()):
        ext = filename.split(os.extsep)[1]
        if ext in converted_gif:
            urlopener.retrieve(converted_gif[ext], filename)
        else:
            video.write_videofile(filename)

    list_of_files['snapshot'] = saving_snapshot_filename
    
    return list_of_files

def compress_image(snapshot):
    with open(snapshot, 'rb') as file:
        img = Image.open(file)
        
        format = str(img.format)
        if format != 'PNG' and format != 'JPEG':
            return False

        # This line avoids problems that can arise saving larger JPEG files with PIL
        ImageFile.MAXBLOCK = img.size[0] * img.size[1]
            
        # The 'quality' option is ignored for PNG files
        img.save(snapshot, quality=90, optimize=True)


def save_to_local(url):
    tempdir = tempfile.gettempdir()
    response = urllib.request.urlopen(url)
    content_type = response.headers['content-type']
    
    if content_type == 'image/gif':
        contents = response.read()

        gif_filepath = os.path.join(tempdir, "%s.gif" % uuid.uuid1())
    
        with open(gif_filepath, 'wb') as gif_file:
            gif_file.write(contents)

        return gif_filepath

    raise BadContentType('%s : is not a gif so it cannot be converted' % url)


        
