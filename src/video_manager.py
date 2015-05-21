from moviepy.editor import *

import os, binascii
from os.path import basename

class VideoManager:

    def convert(self, gif_path):
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]

        list_of_files = dict([(codec, "./tmp/%s.%s"  % (filename_without_ext, codec))for codec in ['mp4', 'ogv', 'webm']])

        saving_snapshot_filename = "./tmp/%s.png" % filename_without_ext

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)

        for filename in list_of_files.values():
            video.write_videofile(filename)

        list_of_files['snapshot'] = saving_snapshot_filename
        
        return list_of_files
