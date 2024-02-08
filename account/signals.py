from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.template.loader import render_to_string

from account.models import VideoflixUser


@receiver(post_save, sender=VideoflixUser)
def sendMail(sender, instance, created, **kwargs):
    print("test", instance.verification_code)
    send_mail(
        subject="Videoflix verification",
        message="",
        from_email="videoflix@simon-esders.de",
        recipient_list=[instance.email],
        html_message=render_to_string('email.html', {
            'username': instance.username,
        }),

        fail_silently=False,
    )