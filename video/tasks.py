import os
import subprocess
import time


def convert_video_to_720p(video_file_path):
    new_path = video_file_path.replace('.mp4', '') + '_720p.mp4'
    cmd = 'sudo ffmpeg -i {} -vf scale=1280:720 {}'.format(
        video_file_path, new_path)
    subprocess.run(cmd, capture_output=True)

def convert_video_to_480p(video_file_path):
    new_path = video_file_path.replace('.mp4', '') + '_480p.mp4'
    cmd = 'sudo ffmpeg -i {} -vf scale=960:480 {}'.format(
        video_file_path, new_path)
    subprocess.run(cmd, capture_output=True)