from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
import django_rq

from video.models import Video, Movie, Episode
from video.tasks import convert_video_to_720p, convert_video_to_480p


@receiver(post_save, sender=Video)
@receiver(post_save, sender=Movie)
@receiver(post_save, sender=Episode)
def save_video(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_to_720p, instance.original_video.path)
        queue.enqueue(convert_video_to_480p, instance.original_video.path)
        instance.video_720p = str(instance.original_video).replace('.mp4', '') + '_720p.mp4'
        instance.video_480p = str(instance.original_video).replace('.mp4', '') + '_480p.mp4'
        instance.save()


@receiver(post_delete, sender=Video)
@receiver(post_delete, sender=Movie)
@receiver(post_delete, sender=Episode)
def delete_video(sender, instance, **kwargs):
    print(instance.original_video)
    pathes = [instance.thumbnail.path, instance.original_video.path, instance.video_720p.path, instance.video_480p.path]

    for path in pathes:
        try:
            os.remove(path)
        except:
            pass