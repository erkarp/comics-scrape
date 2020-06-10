import json

from django.urls import reverse
from rest_framework.test import APITestCase

from plants.models import Plant, Species, Lighting, Spot


class APITests(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        lighting = Lighting(description='bright')
        lighting.save()

        species = Species(name='jade', lighting=lighting)
        species.save()

        spot = Spot(lighting=lighting)
        spot.save()

        self.plant = Plant(
            species=species,
            spot=spot,
            name='jade'
        )
        self.plant.save()

    def test_api_can_return_plants(self):
        response = self.client.get(reverse('plant-list'), format='json')
        self.assertEquals(json.dumps(response.data), '[{"name": "jade"}]')
