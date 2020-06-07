from datetime import date

from django.db import models


class Fertilizer(models.Model):
    description = models.CharField(max_length=56)

    def __str__(self):
        return self.description


class Lighting(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Species(models.Model):
    name = models.CharField(max_length=56)
    water_frequency = models.CharField(max_length=255)
    fertilize_frequency = models.CharField(max_length=255)
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.PROTECT)
    lighting = models.ForeignKey(Lighting, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'species'


class Spot(models.Model):
    name = models.CharField(max_length=255)
    lighting = models.ForeignKey(Lighting, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True)
    location = models.URLField(max_length=255, blank=True)
    closed_down = models.BooleanField

    def __str__(self):
        return self.name


class Plant(models.Model):
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=True)
    spot = models.ForeignKey(Spot, on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    purchase_date = models.DateField(default=date.today)


class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    src = models.ImageField(max_length=255)

    class Meta:
        ordering = ['date']


class Watering(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    fertilized = models.BooleanField

    class Meta:
        ordering = ['date']


