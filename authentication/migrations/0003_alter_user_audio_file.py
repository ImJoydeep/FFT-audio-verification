# Generated by Django 4.2.2 on 2023-06-13 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='audio_file',
            field=models.FileField(upload_to='audio/wav'),
        ),
    ]
