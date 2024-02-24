from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.template.loader import render_to_string

from account.models import VideoflixUser


@receiver(post_save, sender=VideoflixUser)
def send_mail_register(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Videoflix verification",
            message="",
            from_email="videoflix@simon-esders.de",
            recipient_list=[instance.email],
            html_message=render_to_string('email.html', {
                'username': instance.username,
                'verification_code': instance.verification_code
            }),

            fail_silently=False,
        )

def send_mail_rest_password(instance, **kwargs):
    send_mail(
        subject="Videoflix reset your password",
        message="",
        from_email="videoflix@simon-esders.de",
        recipient_list=[instance.email],
        html_message=render_to_string('email_reset_password.html', {
            'username': instance.username,
            'verification_code': instance.reset_code
        }),

    )