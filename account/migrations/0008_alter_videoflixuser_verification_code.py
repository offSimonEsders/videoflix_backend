# Generated by Django 5.0.2 on 2024-02-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_videoflixuser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflixuser',
            name='verification_code',
            field=models.CharField(blank=True, default='XNwz3M7Xs08eSHLZ1TrXSXj12veA43', max_length=30, unique=True),
        ),
    ]
