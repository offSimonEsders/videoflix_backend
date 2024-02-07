from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from account.models import VideoflixUser


@receiver(post_save, sender=VideoflixUser)
def sendMail(sender, instance, created, **kwargs):
    print("test", instance.email)
    send_mail(
        "Videoflix verification",
        "Doppel peace",
        "videoflix@simon-esders.de",
        [instance.email],
        fail_silently=False,
    )