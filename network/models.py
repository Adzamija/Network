from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    body = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)


class Followers(models.Model):
    # User ce biti osoba koja ce biti pracena to znaci da to nije trenutni logovani user 
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed_user")
    unique = models.IntegerField(default=0)
    # Follower_id je id od osobe koja je trenutni user tj logovani
    follower_id = models.IntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked_post_user")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="liked_post")
