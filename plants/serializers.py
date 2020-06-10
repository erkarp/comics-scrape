from rest_framework import serializers

from plants.models import Plant, Species


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['days_between_watering_min', 'days_between_watering_max']


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    species = SpeciesSerializer()

    class Meta:
        model = Plant
        fields = ['species', 'name', 'latest_watering_date', 'next_watering_min', 'next_watering_max']
