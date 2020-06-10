from rest_framework import viewsets

from plants.models import Plant
from plants.serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed or edited.
    """
    queryset = Plant.objects.all()  # .order_by('name')
    serializer_class = PlantSerializer
