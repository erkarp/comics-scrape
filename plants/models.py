import datetime

from django.db import models, IntegrityError
from django.utils import timezone


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
    spot = models.ForeignKey(Spot, related_name="spot", on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, blank=True, null=True)
    purchase_date = models.DateField(default=datetime.date.today)

    @property
    def name(self):
        return self.display_name or self.species.name

    @property
    def latest_watering_date(self):
        return self.watered.first().date

    @property
    def next_watering_min(self):
        if self.latest_watering_date:
            return self.latest_watering_date + datetime.timedelta(days=self.species.days_between_watering_min)

    @property
    def next_watering_max(self):
        if self.latest_watering_date:
            return self.latest_watering_date + datetime.timedelta(days=self.species.days_between_watering_max)

    @property
    def next_watering_avg(self):
        if self.latest_watering_date:
            avg = (self.species.days_between_watering_min + self.species.days_between_watering_max)/2
            return self.latest_watering_date + datetime.timedelta(days=avg)

    @property
    def days_till_next_watering_min(self):
        return -(datetime.date.today() - self.next_watering_min).days

    @property
    def days_till_next_watering_max(self):
        return -(datetime.date.today() - self.next_watering_max).days

    @property
    def time_till_next_watering(self):
        return -(datetime.date.today() - self.next_watering_avg).days

    def __str__(self):
        return self.name

    def record_multiple_watering(self, dates: str) -> (bool, str):
        dates = dates.split(',')
        watering_objects = []

        for d in dates:
            try:
                date = datetime.datetime.strptime(d, '%B %d %Y')
                watering = Watering(
                    plant=self,
                    date=date,
                )
                watering_objects.append(watering)

            except ValueError:
                return False, f'Bad date: {d}'

        try:
            Watering.objects.bulk_create(watering_objects)
            return True, f'Successfully watered {self} on {len(watering_objects)} dates!'

        except IntegrityError as e:
            # Error message: Duplicate entry '1-2005-06-01' for key 'plants_watering_plant_id_date_b12f1322_uniq'
            # Where "1" is the plant id. Extract the date.
            dupe_plant_date = str(e).split("'")[1]
            dupe_date_parts = dupe_plant_date.split('-')[1:]
            dupe_date = '-'.join(dupe_date_parts)
            return False, f'Already watered on {dupe_date}'


class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    src = models.ImageField(max_length=255)

    class Meta:
        ordering = ['date']


class Watering(models.Model):
    plant = models.ForeignKey(Plant, related_name='watered', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    fertilized = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['-date']
        unique_together = ['plant', 'date']
