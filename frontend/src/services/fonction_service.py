# services/stock_service.py
import httpx
from config.config import BASE_URL
from models.models import Fonction


class FonctionService:
    def __init__(self):
        self.base_url = BASE_URL

    async def get_all_fonctions(self, user_token: str):
        """Récupère la liste des fonctions (authentifié)."""
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/fonctions", headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    return []
                    # On convertit le JSON en une liste d'objets Product
                    return [Fonction.from_json(p) for p in data]

                elif response.status_code == 401:
                    print("Erreur: Token invalide ou expiré")
                    return None

                return []
            except Exception as e:
                print(f"Erreur Connexion API: {e}")
                return []
