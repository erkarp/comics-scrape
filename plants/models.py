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
    days_between_watering_min = models.SmallIntegerField()
    days_between_watering_max = models.SmallIntegerField()
    fertilize_frequency = models.CharField(max_length=255, blank=True)
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.PROTECT, blank=True, null=True)
    lighting = models.ForeignKey(Lighting, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
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
    closed_down = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Plant(models.Model):
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    display_name = models.CharField(max_length=255, blank=True)
    spot = models.ForeignKey(Spot, on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, blank=True, null=True)
    purchase_date = models.DateField(default=date.today)

    @property
    def name(self):
        return self.display_name or self.species.name

    @property
    def latest_watering_date(self):
        return self.watering_set.first().date

    @property
    def next_watering_min(self):
        if self.latest_watering_date:
            return self.latest_watering_date.day + self.species.days_between_watering_min

    @property
    def next_watering_max(self):
        if self.latest_watering_date:
            return self.latest_watering_date.day + self.species.days_between_watering_max

    def __str__(self):
        return self.name


class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    src = models.ImageField(max_length=255)

    class Meta:
        ordering = ['date']


class Watering(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today, unique=True)
    fertilized = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['-date']
