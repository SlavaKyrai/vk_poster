from django.db import models


class VKToken(models.Model):
    token = models.CharField(max_length=100, primary_key=True)


class Community(models.Model):
    vk_name = models.CharField(max_length=100, unique=True)
    vk_community_id = models.IntegerField(primary_key=True)
    subbredit_name = models.CharField(max_length=100, unique=True)
    token = models.ForeignKey(VKToken, on_delete=models.CASCADE)


class Post(models.Model):
    reddit_id = models.CharField(max_length=10, primary_key=True)
    vk_community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    self_text = models.TextField(blank=True)
    is_self = models.BooleanField()
    score = models.IntegerField(default=0, blank=True)
    url = models.URLField()
    is_posted = models.BooleanField(default=False)
