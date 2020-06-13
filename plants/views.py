from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from plants.models import Plant
from plants.serializers import PlantSerializer, WateringSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed or edited.
    """
    queryset = Plant.objects.all()  # .order_by('name')
    serializer_class = PlantSerializer


@api_view(['POST'])
def water_plant(request):
    serializer = WateringSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
