# Generated by Django 5.0.2 on 2024-02-26 22:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_alter_video_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('video_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='video.video')),
            ],
            bases=('video.video',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('video_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='video.video')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.series')),
            ],
            bases=('video.video',),
        ),
    ]
