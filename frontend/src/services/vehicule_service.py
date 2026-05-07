# services/stock_service.py
import httpx
from config.config import BASE_URL
from utils.headers import get_headers
from models.models import Vehicule
from utils.exceptions import AuthenticationError, ValidatorError


class VehiculeService:
    def __init__(self):
        self.base_url = BASE_URL

    async def get_all_vehicules(
        self, user_token: str, page=1, search_text="", url=None
    ):
        """Récupère la liste des vehicules (authentifié)."""
        headers = get_headers(user_token)

        # On construit l'URL avec les paramètres de pagination et recherche
        if url is None:
            url = f"{self.base_url}/vehicules/?page={page}&search={search_text}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data

            elif response.status_code == 401:
                raise AuthenticationError("Token expiré")  # On lève l'erreur ici

            else:
                raise Exception(f"Erreur API: {response.status_code}")

    async def create_vehicule(self, vehicule: Vehicule, user_token: str):
        """Ajoute un véhicule (authentifié)."""
        headers = get_headers(user_token)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/vehicules/", headers=headers, json=vehicule
            )
            if response.status_code in [200, 201]:
                return True

            elif response.status_code == 401:
                raise AuthenticationError("Token expiré")  # On lève l'erreur ici

            elif response.status_code == 400:
                error_data = response.json()
                print(
                    "VehiculeService - create_vehicule - Erreur de validation:",
                    error_data,
                )  # Debug
                raise ValidatorError(error_data)

            else:
                raise Exception(f"Erreur API: {response.status_code}")

    async def delete_vehicule(self, vehicule_id: int, user_token: str):
        """Supprime un véhicule (authentifié)."""
        headers = get_headers(user_token)

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/vehicules/{vehicule_id}/", headers=headers
            )
            if response.status_code in [200, 204]:
                return True

            elif response.status_code == 401:
                raise AuthenticationError("Token expiré")  # On lève l'erreur ici

            else:
                raise Exception(f"Erreur API: {response.status_code}")
