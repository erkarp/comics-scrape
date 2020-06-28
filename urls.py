from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from plants.views import PlantViewSet, water_plant, current_user
from xkcd.views import xkcds


router = routers.DefaultRouter()
router.register(r'plants/plants', PlantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('plants/watering/', water_plant, name='water-plant'),
    path('token-auth/', obtain_jwt_token, name='token-auth'),
    path('user/', current_user),
    path('xkcd/', xkcds),
]
