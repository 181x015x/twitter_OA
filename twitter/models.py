from django.db import models

class Userinfo(models.Model):

    oauth_token = models.CharField(primary_key=True,max_length=100)
    oauth_token_secret = models.CharField(max_length=100,null=True)
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    favourites_count = models.IntegerField()
    statuses_count = models.IntegerField()
    total_point = models.IntegerField()

