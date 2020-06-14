from rest_framework import serializers

from plants.models import Plant, Species, Watering


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['days_between_watering_min', 'days_between_watering_max']


class WateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watering
        fields = ['plant', 'date', 'fertilized']


class PlantSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer()
    watered = serializers.StringRelatedField(many=True)

    class Meta:
        model = Plant
        fields = ['species', 'watered', 'name', 'latest_watering_date',
                  'next_watering_min', 'next_watering_max',
                  'days_till_next_watering_min', 'days_till_next_watering_max',
                  'time_till_next_watering']
