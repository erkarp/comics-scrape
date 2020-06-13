from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from plants.views import PlantViewSet, water_plant
from xkcd.views import xkcds


router = routers.DefaultRouter()
router.register(r'plants/plants', PlantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('plants/watering/', water_plant, name='water-plant'),
    path('xkcd/', xkcds),
]