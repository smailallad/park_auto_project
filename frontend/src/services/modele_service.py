import httpx
from config.config import BASE_URL
from utils.headers import get_headers
from models.models import Modele
from utils.exceptions import AuthenticationError, ValidatorError


class ModeleService:
    def __init__(self):
        self.base_url = BASE_URL

    async def get_all_modeles(self, user_token: str):
        """Récupère la liste des modèles (authentifié)."""
        headers = get_headers(user_token)

        # On construit l'URL avec les paramètres de pagination et recherche
        url = f"{self.base_url}/modeles/"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print("ModeleService - get_all_modeles - data reçue:", data)  # Debug
                return data
            elif response.status_code == 401:
                raise AuthenticationError("Token expiré")  # On lève l'erreur ici

            else:
                raise Exception(f"Erreur API: {response.status_code}")
