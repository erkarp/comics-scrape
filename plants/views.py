from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from plants.models import Plant
from plants.serializers import WateringSerializer, PlantListSerializer, PlantViewSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed or edited.
    """
    queryset = Plant.objects.all()  # .order_by('name')

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantListSerializer
        else:
            return PlantViewSerializer


@api_view(['POST'])
def water_plant(request):
    if 'dates' in request.data:
        plant = Plant.objects.get(pk=request.data['plant'])
        success, message = plant.record_multiple_watering(request.data['dates'])

        if success:
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    serializer = WateringSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
