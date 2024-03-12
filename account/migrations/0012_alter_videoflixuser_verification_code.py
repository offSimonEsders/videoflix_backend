# Generated by Django 5.0.2 on 2024-03-12 09:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default=uuid.UUID('e4c67e5f-721c-4899-97cc-1fa7862f1f38'), max_length=36, unique=True),
        ),
    ]
