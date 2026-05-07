# services/stock_service.py
import httpx
from config.config import BASE_URL
from models.models import User


class UserService:
    def __init__(self):
        self.base_url = BASE_URL

    async def get_all_users(self, user_token: str):
        """Récupère la liste des users (authentifié)."""
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/users", headers=headers)
                print(response)
                if response.status_code == 200:
                    data = response.json()
                    _users = data["users"]
                    pagination = data["pagination"]

                    # On convertit le JSON en une liste d'objets User
                    users = [User.from_json(p) for p in _users]
                    return users, pagination

                elif response.status_code == 401:
                    print("Erreur: Token invalide ou expiré")
                    return None

                return []
            except Exception as e:
                print(f"Erreur Connexion API: {e}")
                return []
