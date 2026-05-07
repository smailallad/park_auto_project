import flet as ft

class AuthController:
    def __init__(self, auth_service,ui_service):
        self.auth_service = auth_service
        self.ui_service = ui_service
        self.page = None  # Sera défini dans le main.py
        self.user_data = None # Stocke les infos de l'utilisateur connecté
        self.is_loading = False

    async def login(self, username, password):
        """Tente de connecter l'utilisateur via l'API."""
        if not username or not password:
            self.ui_service.show_error("Veuillez remplir tous les champs.")
            return

        result = await self.auth_service.login_request(username, password)
        if result and result["success"] and "user_token" in result and "user_refresh" in result:
            # On stocke le token de manière persistante sur le Dell/Android
            self.page.session.store.set("user_token", result["user_token"])
            self.page.session.store.set("user_refresh", result["user_refresh"])
            self.page.session.store.set("is_logged_in", True)
            
            # Redirection vers l'accueil
            await self.page.push_route("/")
        else:
            self.ui_service.show_error("Utilisateur ou mot de passe incorrect.")

    async def logout(self, e=None):
        """Déconnecte l'utilisateur et nettoie les données."""
        self.page.session.store.remove("user_token")
        self.page.session.store.remove("user_refresh")
        self.page.session.store.set("is_logged_in", False)

        await self.page.push_route("/login")

    def check_auth(self):
        """Vérifie si l'utilisateur est déjà connecté au démarrage."""
        # return self.page.client_storage.get("is_logged_in") or False
        return self.page.session.store.get("is_logged_in") or False
