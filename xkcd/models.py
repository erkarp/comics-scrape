from django.db import models


class Comic(models.Model):
    xkcd = models.PositiveIntegerField()
    date = models.DateField()
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
