from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os, shutil

from video.models import Video
from video.tasks import convert_video_to_720p


@receiver(post_save, sender=Video)
def save_video(sender, instance, created, **kwargs):
    if created:
        convert_video_to_720p(instance.original_video.path)


@receiver(post_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    print(instance.original_video)
    os.remove(instance.original_video.path)
