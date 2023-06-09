# Generated by Django 4.2 on 2023-06-08 16:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='alreadyLiked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]