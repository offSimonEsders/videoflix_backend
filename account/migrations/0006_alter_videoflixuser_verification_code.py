# Generated by Django 5.0.2 on 2024-02-11 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default='4Z4VfgyFiG5hYLMvApVCMy3p4FDCTV', max_length=30, unique=True),
        ),
    ]
