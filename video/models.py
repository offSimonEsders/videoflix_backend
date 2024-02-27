from django.db import models
import os

def get_upload_path(instance, filename):
    title_without_spaces = instance.title.replace(" ", "")
    return os.path.join('videos', title_without_spaces, filename)

class Video(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    thumbnail = models.FileField(upload_to='thumbnails')
    original_video = models.FileField(upload_to=get_upload_path)
    video_720p = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    video_480p = models.FileField(upload_to=get_upload_path, blank=True, null=True)


class Movie(Video):
    pass

class Serie(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    thumbnail = models.FileField(upload_to='thumbnails')

    def __str__(self):
        return self.title

class Episode(Video):
    series = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='episodes')