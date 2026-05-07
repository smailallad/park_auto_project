from dataclasses import dataclass


@dataclass
class Fonction:
    id: str
    nom: str

    @classmethod
    def from_json(cls, json_data: dict):
        """Crée un objet Fonction à partir d'un dictionnaire JSON."""
        return cls(
            id=int(json_data.get("id", 0)),
            nom=str(json_data.get("nom", "")),
        )


@dataclass
class User:
    id: str
    nom: str
    email: str
    actif: bool

    @classmethod
    def from_json(cls, json_data: dict):
        """Crée un objet User à partir d'un dictionnaire JSON."""
        return cls(
            id=int(json_data.get("id", 0)),
            nom=str(json_data.get("nom", "")),
            email=str(json_data.get("email", "")),
            actif=bool(json_data.get("actif", False)),
        )


@dataclass
class Modele:
    id: int
    nom: str
    marque_nom: str

    @classmethod
    def from_json(cls, json_data: dict):
        # Récupération sécurisée des données imbriquées
        marque_obj = json_data.get("marque", {})

        return cls(
            id=int(json_data.get("id", 0)),
            nom=str(json_data.get("nom", "")),
            marque_nom=str(marque_obj.get("nom", "Inconnue")),
        )


@dataclass
class Vehicule:
    id: int
    nom: str  # Ta lettre unique (A, B, C...)
    immatriculation: str
    actif: bool  # Par défaut, un véhicule est actif
    kms: int
    marque_nom: str  # On extrait le nom de la marque pour simplifier l'UI
    modele_nom: str  # On extrait le nom du modèle pour simplifier l'UI

    @classmethod
    def from_json(cls, json_data: dict):
        """Crée un objet Vehicule en gérant les dictionnaires imbriqués de l'API."""

        # Récupération sécurisée des données imbriquées
        modele_obj = json_data.get("modele", {})
        marque_obj = modele_obj.get("marque", {})

        return cls(
            id=int(json_data.get("id", 0)),
            # nom=str(json_data.get("nom", "")),
            nom=str(json_data.get("nom", "")).upper(),
            immatriculation=str(json_data.get("immatriculation", "")),
            actif=bool(json_data.get("actif", True)),
            kms=int(json_data.get("kms", 0)),
            # On va chercher le nom dans le dictionnaire 'marque' qui est dans 'modele'
            marque_nom=str(marque_obj.get("nom", "Inconnue")),
            # On va chercher le nom dans le dictionnaire 'modele'
            modele_nom=str(modele_obj.get("nom", "Inconnu")),
        )
