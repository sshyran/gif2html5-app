from moviepy.editor import *

import os, binascii
import urllib
import tempfile
from os.path import basename

class VideoManager:

    def convert(self, gif_path, gfycat):
        tempdir = tempfile.gettempdir()
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]
        
        urlopener = urllib.URLopener()
        converted_gif = gfycat.uploadFile(gif_path)

        list_of_files = dict([(codec, "%s/%s.%s"  % (tempdir, filename_without_ext, codec))for codec in ['mp4', 'ogv', 'webm']])

        saving_snapshot_filename = "%s/%s.png" % (tempdir, filename_without_ext)

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)

        for filename in list_of_files.values():
            ext = filename.split(os.extsep)[1]
            if ext == 'ogv':
                video.write_videofile(filename)
            else:
                urlopener.retrieve(converted_gif.get("%sUrl" % (ext)), filename)

        list_of_files['snapshot'] = saving_snapshot_filename
        
        return list_of_files
