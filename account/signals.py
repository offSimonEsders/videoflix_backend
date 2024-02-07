from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import VideoflixUser


@receiver(post_save, sender=VideoflixUser)
def sendMail(sender, instance, created, **kwargs):
    print("test", instance.email)