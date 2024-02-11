from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os

from video.models import Video
from video.tasks import convert_video_to_720p, convert_video_to_480p


@receiver(post_save, sender=Video)
def save_video(sender, instance, created, **kwargs):
    if created:
        convert_video_to_720p(instance.original_video.path)
        convert_video_to_480p(instance.original_video.path)
        instance.video_720p = str(instance.original_video).replace('.mp4', '') + '_720p.mp4'
        instance.video_480p = str(instance.original_video).replace('.mp4', '') + '_480p.mp4'
        instance.save()


@receiver(post_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    print(instance.original_video)
    os.remove(instance.original_video.path)
    os.remove(instance.video_720p.path)
    os.remove(instance.video_480p.path)
