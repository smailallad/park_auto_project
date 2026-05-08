from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from parc_auto.models import Entretien, Marque, Modele, Vehicule


class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = ["id", "nom"]


class ModeleSerializer(serializers.ModelSerializer):
    marque = MarqueSerializer()  # Incorpore les détails de la marque

    class Meta:
        model = Modele
        fields = ["id", "nom", "marque"]


class VehiculeSerializer(serializers.ModelSerializer):
    modele = ModeleSerializer(read_only=True)  # Incorpore les détails du modèle
    # Pour l'ÉCRITURE (POST/PUT) : On utilise l'ID envoyé par le Dropdown
    modele_id = serializers.PrimaryKeyRelatedField(
        queryset=Modele.objects.all(),
        source="modele",  # Dit à Django d'enregistrer ça dans le champ 'modele'
        write_only=True,
    )

    class Meta:
        model = Vehicule
        # fields = "__all__"  # On expose tous les champs (id, immatriculation, etc.)
        # Liste explicitement les champs pour être sûr d'inclure modele_id
        fields = ["id", "immatriculation", "nom", "modele", "modele_id"]

    def validate_immatriculation(self, value):
        return value.upper()

    def validate(self, data):
        # Ce print va s'afficher dans ton terminal Django
        print(f"DONNÉES REÇUES : {data}")
        return data


class EntretienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entretien
        fields = "__all__"
