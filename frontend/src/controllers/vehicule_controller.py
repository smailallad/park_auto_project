from urllib.parse import urlparse, parse_qs

from models.models import Vehicule


class VehiculeController:
    def __init__(self, vehicule_service, ui_service):
        self.page = None  # Sera défini dans le main.py
        self.vehicule_service = vehicule_service  # Sera injecté dans le main.py
        self.ui_service = ui_service  # Sera injecté dans le main.py
        self.vehicules = []

        self.page_index = 1
        self.search_text = ""
        self.next_url = None
        self.previous_url = None
        self.url = None
        # self.is_loading = False

    def _get_token(self):
        """Centralise la récupération du user_token."""
        # Note : .get() est plus propre que .store.get() sur les versions récentes
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            self.ui_service.show_error("Session expirée. Veuillez vous reconnecter.")
            self.page.go("/login")
            return None
        return user_token

    async def get_all_vehicules(self):
        user_token = self._get_token()
        if not user_token:
            return

        self.vehicules = []

        results = await self.vehicule_service.get_all_vehicules(
            user_token, self.page_index, self.search_text, self.url
        )
        self.url = None
        _vehicules = results.get("results", [])
        self.vehicules = [Vehicule.from_json(p) for p in _vehicules]
        self.next_url = results.get("next")
        self.previous_url = results.get("previous")

        if self.next_url:
            parsed = urlparse(self.next_url)
            next_page = parse_qs(parsed.query).get("page", ["2"])[0]
            self.page_index = int(next_page) - 1
        elif self.previous_url:
            parsed = urlparse(self.previous_url)
            prev_page = parse_qs(parsed.query).get("page", ["0"])[0]
            self.page_index = int(prev_page) + 1

    async def delete_vehicule(self, vehicule_id):
        user_token = self._get_token()
        if not user_token:
            return
        try:
            success = await self.vehicule_service.delete_vehicule(
                vehicule_id, user_token
            )
            # if success:
            # On rafraîchit la liste localement après suppression
            # await self.get_all_vehicules()
            self.ui_service.show_success("Véhicule supprimé avec succès.")
            return success
        except Exception as e:
            self.ui_service.show_error("Impossible de supprimer l'utilisateur.")
            return False

    async def get_vehicule_by_id(self, vehicule_id):
        """Récupère un vehicule spécifique par ID."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            print("Pas de user_token trouvé, impossible de charger le vehicule.")
            return None

        return await self.vehicule_service.get_vehicule_by_id(vehicule_id, user_token)

    async def create_vehicule(self, vehicule_data):
        """Crée un nouveau vehicule."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            self.ui_service.show_error("Session expirée. Veuillez vous reconnecter.")
            self.page.go("/login")
            return None

        result = await self.vehicule_service.create_vehicule(vehicule_data, user_token)
        if result:
            self.ui_service.show_success("Véhicule créé avec succès.")
            return result

    async def update_vehicule(self, vehicule_id, vehicule_data):
        """Met à jour un vehicule existant."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            print("Pas de user_token trouvé, impossible de mettre à jour le vehicule.")
            return None

        return await self.vehicule_service.update_vehicule(
            vehicule_id, vehicule_data, user_token
        )
