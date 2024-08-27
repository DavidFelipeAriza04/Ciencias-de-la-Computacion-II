from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MunicipiosViewSet

router = DefaultRouter()
router.register(r"", MunicipiosViewSet, basename="municipios")
urlpatterns = [
    path("", include(router.urls)),
]
