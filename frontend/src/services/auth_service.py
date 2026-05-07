import httpx

from config.config import BASE_URL


class AuthService:
    def __init__(self):
        # Utiliser l'IP locale de votre PC pour les tests sur APK
        # self.base_url = "http://192.168.100.9:3001"
        self.base_url = BASE_URL

    async def login_request(self, username, password):
        """Appel direct à l'API Fastify pour obtenir un token."""
        async with httpx.AsyncClient() as client:
            try:
                # Format standard OAuth2 Password Bearer
                payload = {"username": username, "password": password}
                response = await client.post(f"{self.base_url}/login/", data=payload)
                if response.status_code == 200:
                    # data = response.json()
                    # print(f"DEBUG API DATA: {data}") # Pour voir la structure réelle
                    return {
                        "success": True,
                        "user_token": response.json().get("access"),
                        "user_refresh": response.json().get("refresh"),
                    }

                return {"success": False, "message": "Identifiants incorrects"}
            except Exception as e:
                return {"success": False, "message": f"Erreur connexion : {str(e)}"}
