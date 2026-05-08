from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from parc_auto.models import Entretien, Vehicule, Modele
from .serializers import ModeleSerializer, VehiculeSerializer, EntretienSerializer


# Optionnel : Définir une pagination personnalisée si tu ne veux pas de globale
class VehiculePagination(PageNumberPagination):
    page_size = 5  # Nombre d'éléments par page
    page_size_query_param = "page_size"
    max_page_size = 5


class VehiculeViewSet(viewsets.ModelViewSet):
    # queryset = Vehicule.objects.all().order_by(
    #     "-id"
    # )
    queryset = Vehicule.objects.select_related("modele__marque").all().order_by("id")
    # Ordonner pour une pagination stable
    serializer_class = VehiculeSerializer
    pagination_class = VehiculePagination

    # Configuration de la recherche
    filter_backends = [filters.SearchFilter]
    # Les champs sur lesquels la recherche s'appliquera
    search_fields = ["immatriculation", "marque", "modele"]


class EntretienViewSet(viewsets.ModelViewSet):
    queryset = Entretien.objects.all()
    serializer_class = EntretienSerializer


class ModeleViewSet(viewsets.ModelViewSet):
    queryset = Modele.objects.select_related("marque").all().order_by("-id")
    serializer_class = ModeleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nom", "marque__nom"]
