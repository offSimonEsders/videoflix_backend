# Generated by Django 5.0.2 on 2024-02-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default='LqNb1UCKYz2BnVe0v7uj78NAIi0kVf', max_length=30, unique=True),
        ),
    ]