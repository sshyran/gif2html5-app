from result import Result
from moviepy.editor import *

import os, binascii
from os.path import basename

class VideoManager:

    def convert(self, gif_path):
        filename = basename(gif_path)
        filename_without_ext = os.path.splitext(filename)[0]

        mp4_file = "%s.mp4" % filename_without_ext
        ogv_file = "%s.ogv" % filename_without_ext
        webm_file = "%s.webm" % filename_without_ext
        snapshot_file = "%s.png" % filename_without_ext

        saving_mp4_filename = "./tmp/%s" % (mp4_file)
        saving_ogv_filename = "./tmp/%s" % (ogv_file)
        saving_webm_filename = "./tmp/%s" % (webm_file)
        saving_snapshot_filename = "./tmp/%s" % snapshot_file

        video = VideoFileClip(gif_path)
        video.save_frame(saving_snapshot_filename)
        video.write_videofile(saving_mp4_filename)
        video.write_videofile(saving_ogv_filename)
        video.write_videofile(saving_webm_filename)

        return Result(mp4_file, ogv_file, webm_file, snapshot_file)
