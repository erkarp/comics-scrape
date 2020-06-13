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
            days_between_watering_min=5,
            days_between_watering_max=9
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
        water = Watering(plant=self.plant, date=(datetime.date.today() - datetime.timedelta(days=1)))
        water.save()
        self.assertEqual(self.plant.next_watering_min, (datetime.date.today() + datetime.timedelta(days=4)))

    def test_next_watering_max(self):
        water = Watering(plant=self.plant, date=(datetime.date.today() - datetime.timedelta(days=1)))
        water.save()
        self.assertEqual(self.plant.next_watering_max, (datetime.date.today() + datetime.timedelta(days=8)))

    def test_time_till_next_watering(self):
        water = Watering(plant=self.plant, date=(datetime.date.today() - datetime.timedelta(days=1)))
        water.save()
        self.assertEqual(self.plant.time_till_next_watering, 8)

    def test_water_plant(self):
        data = {
            "date": datetime.date(2020, 6, 9),
            "plant": self.plant.id,
        }
        response = self.client.post(reverse('water-plant'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_water_plant__bulk(self):
        data = {
            "dates": "June 1 2005,June 2 2006,June 3 2007",
            "plant": self.plant.id,
        }
        response = self.client.post(reverse('water-plant'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_record_multiple_watering(self):
        success, message = self.plant.record_multiple_watering("June 1 2005,June 2 2006,June 3 2007")
        self.assertTrue(success)
        self.assertEqual(Watering.objects.filter(plant=self.plant.pk).count(), 4)

    def test_record_multiple_watering__bad_date(self):
        success, message = self.plant.record_multiple_watering("June 1 2005,June 2 2006,bad date")

        self.assertFalse(success)
        self.assertEqual(message, 'Bad date: bad date')

    def test_record_multiple_watering__already_watered(self):
        self.plant.record_multiple_watering("June 1 2005")
        success, message = self.plant.record_multiple_watering("June 1 2005,June 2 2006,June 3 2007")

        self.assertFalse(success)
        self.assertEqual(message, 'Already watered on 2005-06-01')

    def test_record_multiple_watering__duplicate_input_data(self):
        success, message = self.plant.record_multiple_watering("June 1 2005,June 2 2006,June 2 2006")

        self.assertFalse(success)
        self.assertEqual(message, 'Already watered on 2006-06-02')
