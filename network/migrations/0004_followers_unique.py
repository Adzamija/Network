# Generated by Django 4.2 on 2023-06-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_following_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='unique',
            field=models.IntegerField(default=0),
        ),
    ]
