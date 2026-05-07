from urllib.parse import urlparse, parse_qs

from models.models import Modele


class ModeleController:
    def __init__(self, modele_service, ui_service):
        self.page = None  # Sera défini dans le main.py
        self.modele_service = modele_service  # Sera injecté dans le main.py
        self.ui_service = ui_service  # Sera injecté dans le main.py
        self.modeles = []

    def _get_token(self):
        """Centralise la récupération du user_token."""
        # Note : .get() est plus propre que .store.get() sur les versions récentes
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            self.ui_service.show_error("Session expirée. Veuillez vous reconnecter.")
            self.page.go("/login")
            return None
        return user_token

    async def get_all_modeles(self):
        user_token = self._get_token()
        if not user_token:
            return

        self.modeles = []
        _modeles = await self.modele_service.get_all_modeles(user_token)
        self.modeles = [Modele.from_json(p) for p in _modeles]

        # print("Modeles chargés:", self.modeles)  # Debug: Affiche les modèles chargés
