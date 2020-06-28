from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from plants.models import Plant, Species, Watering


class SpeciesSerializer(serializers.ModelSerializer):
    lighting = serializers.StringRelatedField()

    class Meta:
        model = Species
        fields = ['days_between_watering_min', 'days_between_watering_max', 'lighting']


class WateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watering
        fields = ['plant', 'date', 'fertilized']


class PlantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name', 'latest_watering_date',
                  'next_watering_min', 'next_watering_max',
                  'days_till_next_watering_min', 'days_till_next_watering_max',
                  'time_till_next_watering']


class PlantViewSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer()
    watered = serializers.StringRelatedField(many=True)
    spot = serializers.StringRelatedField()

    class Meta:
        model = Plant
        fields = ['id', 'species', 'watered', 'name', 'spot', 'latest_watering_date',
                  'next_watering_min', 'next_watering_max',
                  'days_till_next_watering_min', 'days_till_next_watering_max',
                  'time_till_next_watering']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('token', 'username', 'password')

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    # To add user creation, continue
    # https://medium.com/@dakota.lillie/django-react-jwt-authentication-5015ee00ef9a
