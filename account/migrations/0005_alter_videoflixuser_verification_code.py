# Generated by Django 5.0.2 on 2024-02-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default='3pjmE49LnCr09XAJtVoG2Ah4oibqax', max_length=30, unique=True),
        ),
    ]
