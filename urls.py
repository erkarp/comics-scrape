from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from plants.views import PlantViewSet
from xkcd import views


router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xkcd/', views.xkcds),
    path('', include(router.urls)),
]
