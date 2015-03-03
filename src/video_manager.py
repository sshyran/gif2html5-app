from result import Result
from moviepy.editor import *

import os, binascii
from os.path import basename

class VideoManager:

    def convert(self, gif_path):
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]

        mp4_file = "%s.mp4" % filename_without_ext
        snapshot_file = "%s.png" % filename_without_ext

        saving_mp4_filename = "./tmp/%s" % (mp4_file)
        saving_snapshot_filename = "./tmp/%s" % snapshot_file

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)

        result = CompositeVideoClip([video])
        result.write_videofile(saving_mp4_filename)

        return Result(mp4_file, snapshot_file)
