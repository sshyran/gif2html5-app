from moviepy.editor import *
from PIL import Image, ImageFile

import os, binascii
import urllib.request, urllib.parse, urllib.error
import tempfile
from os.path import basename

from gif2html5.gfycat import convert_gif

class VideoManager:

    def convert(self, gif_path):
        tempdir = tempfile.gettempdir()
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]
        
        urlopener = urllib.request.URLopener()
        converted_gif = convert_gif(gif_path)

        list_of_files = dict([(codec, "%s/%s.%s"  % (tempdir, filename_without_ext, codec))for codec in ['mp4', 'ogv', 'webm']])

        saving_snapshot_filename = "%s/%s.jpg" % (tempdir, filename_without_ext)

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)
        
        self._compress_image(saving_snapshot_filename)
        
        for filename in list(list_of_files.values()):
            ext = filename.split(os.extsep)[1]
            if ext == 'ogv':
                video.write_videofile(filename)
            else:
                print(converted_gif) 
                urlopener.retrieve(converted_gif.get(ext), filename)

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
        
