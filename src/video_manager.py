from moviepy.editor import *

import os, binascii
from os.path import basename

class VideoManager:

    def convert(self, gif_path):
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]

        list_of_files = dict([(codec, "%s.%s"  % (filename_without_ext, codec))for codec in ['mp4', 'ogv', 'webm']])

        snapshot_file = "%s.png" % filename_without_ext
        saving_snapshot_filename = "./tmp/%s" % snapshot_file

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)

        [video.write_videofile("./tmp/%s" % list_of_files.get(k)) for k in list_of_files.keys()]
        list_of_files['snapshot'] = snapshot_file
        
        return list_of_files
