import os
import subprocess
import time


def convert_video_to_720p(video_file_path):
    new_path = video_file_path.replace('.mp4', '_720p.mp4')
    cmd = [
        "ffmpeg", "-i",
        video_file_path,
        "-vf", "scale=1280:720",
        new_path
    ]
    subprocess.run(cmd, capture_output=True)


def convert_video_to_480p(video_file_path):
    new_path = video_file_path.replace('.mp4', '_720p.mp4')
    cmd = [
        "ffmpeg", "-i",
        video_file_path,
        "-vf", "scale=960:480",
        new_path
    ]
    subprocess.run(cmd, capture_output=True)
