# Generated by Django 4.2.2 on 2023-06-20 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_user_fft_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fft_features',
            field=models.JSONField(),
        ),
    ]
