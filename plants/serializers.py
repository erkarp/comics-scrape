from rest_framework import serializers

from plants.models import Plant


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = ['name']
