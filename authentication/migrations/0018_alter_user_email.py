# Generated by Django 4.2.2 on 2023-06-20 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
