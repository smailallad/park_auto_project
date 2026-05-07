from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModeleViewSet, VehiculeViewSet, EntretienViewSet

# Le router crée les URLs comme /api/vehicules/ automatiquement
router = DefaultRouter()
router.register(r"modeles", ModeleViewSet)
router.register(r"vehicules", VehiculeViewSet)
router.register(r"entretiens", EntretienViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
