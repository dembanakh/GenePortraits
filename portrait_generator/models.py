from django.db import models
from django.contrib.auth.models import User


class FrequencyPortrait(models.Model):
    gene = models.TextField()
    mod = models.PositiveIntegerField(default=1)
    remainder = models.PositiveIntegerField(default=0)
    depth = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    contrast = models.BooleanField()
    frame = models.BooleanField(default=True)
    portrait = models.TextField()


class UserFrequencyPortrait(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portrait = models.ForeignKey(FrequencyPortrait, on_delete=models.CASCADE)
    generation_id = models.IntegerField(default=0)
