# Generated by Django 5.0.2 on 2024-02-22 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_alter_video_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
    ]