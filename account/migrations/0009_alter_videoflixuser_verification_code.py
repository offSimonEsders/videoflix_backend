# Generated by Django 5.0.2 on 2024-02-11 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default='5OX0LJRPAEKWhnw7Jog7A5A6ioIYG5', max_length=30, unique=True),
        ),
    ]
