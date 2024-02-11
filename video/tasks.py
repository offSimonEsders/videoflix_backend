import os
import subprocess
import time


def convert_video_to_720p(video_file_path):
    cmd = 'ffmpeg -i "{}" -vf scale=1420:720 "{}"'.format(
        video_file_path, video_file_path.replace('.mp4', '') + '_720p.mp4')
    subprocess.run(cmd, capture_output=True)
