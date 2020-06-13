import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from plants.models import Plant, Species, Lighting, Spot, Watering


class PlantTests(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        lighting = Lighting(description='bright')
        lighting.save()

        spot = Spot(lighting=lighting)
        spot.save()

        species = Species(
            name='jade',
            lighting=lighting,
            days_between_watering_min=3,
            days_between_watering_max=5
        )
        species.save()

        self.plant = Plant(
            species=species,
            spot=spot,
            display_name='jade'
        )
        self.plant.save()

        self.watering = Watering(plant=self.plant, date=datetime.date(2020, 6, 8))
        self.watering.save()

    def test_api_can_return_plants(self):
        response = self.client.get(reverse('plant-list'), format='json')
        self.assertEquals(response.data[0]['name'], 'jade')

    def test_api_can_return_single_plant(self):
        response = self.client.get(reverse('plant-detail', kwargs={'pk': self.plant.pk}), format='json')
        self.assertEqual(response.data['name'], 'jade')

    def test_latest_watering(self):
        self.assertEqual(self.plant.latest_watering_date, self.watering.date)

    def test_next_watering_min(self):
        self.assertEqual(self.plant.next_watering_min, 11)

    def test_next_watering_max(self):
        self.assertEqual(self.plant.next_watering_max, 13)

    def test_water_plant(self):
        data = {
            "date": datetime.date(2020, 6, 9),
            "plant": self.plant.id,
        }
        response = self.client.post(reverse('water-plant'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

