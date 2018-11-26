from django.db import models


class Comic(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    published = models.DateField()
    display_name = models.CharField(max_length=100)
    img_filename = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scraped = models.DateTimeField(auto_now=True)
