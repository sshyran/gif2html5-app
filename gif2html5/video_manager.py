import urllib.request, urllib.error, urllib.parse
import os, uuid, tempfile

from os.path import basename
from moviepy.editor import *
from PIL import Image, ImageFile

from gif2html5.gfycat import convert_gif


class VideoManager:

    def convert(self, gif_url):
        codecs = ['mp4', 'ogv', 'webm']

        try:
            gif_path = self._save_to_local(gif_url)
        except Exception:
            raise Exception('This is not a gif')
        
        tempdir = tempfile.gettempdir()
        f = basename(gif_path)
        f_without_ext = os.path.splitext(f)[0]
        
        urlopener = urllib.request.URLopener()
        converted_gif = convert_gif(gif_url)
        
        list_of_files = dict([(codec, "%s/%s.%s"  % (tempdir, f_without_ext, codec))for codec in codecs])

        saving_snapshot_filename = "%s/%s.jpg" % (tempdir, f_without_ext)

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)
        
        self._compress_image(saving_snapshot_filename)
        
        for filename in list(list_of_files.values()):
            ext = filename.split(os.extsep)[1]
            if ext == 'ogv':
                video.write_videofile(filename)
            else:
                urlopener.retrieve(converted_gif[ext], filename)

        list_of_files['snapshot'] = saving_snapshot_filename
        
        return list_of_files

    def _compress_image(self, snapshot):
        with open(snapshot, 'rb') as file:
            img = Image.open(file)
            
            format = str(img.format)
            if format != 'PNG' and format != 'JPEG':
                return False
 
            # This line avoids problems that can arise saving larger JPEG files with PIL
            ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                
            # The 'quality' option is ignored for PNG files
            img.save(snapshot, quality=90, optimize=True)

    
    def _save_to_local(self, url):
        tempdir = tempfile.gettempdir()
        response = urllib.request.urlopen(url)
        content_type = response.headers['content-type']
        
        if content_type == 'image/gif':
            contents = response.read()

            gif_filepath = "%s/%s.gif" % (tempdir, uuid.uuid1())
        
            with open(gif_filepath, 'wb') as gif_file:
                gif_file.write(contents)

            return gif_filepath

        raise Exception


        
