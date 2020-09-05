from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from plants.models import Plant
from plants.serializers import PlantListSerializer, PlantViewSerializer


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
@permission_classes([IsAuthenticated])
def water_plant(request):
    plant = Plant.objects.get(pk=request.data['plant'])

    if 'dates' in request.data:
        success, message = plant.record_multiple_watering(request.data['dates'])

        if success:
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    plant.water()
    return Response('water tried', status=status.HTTP_201_CREATED)
