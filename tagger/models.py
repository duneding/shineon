from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tweet(models.Model):
    text = models.CharField(max_length=200)

class Sentiment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    subjectivity = models.IntegerField(default=0)
    polarity = models.IntegerField(default=0)