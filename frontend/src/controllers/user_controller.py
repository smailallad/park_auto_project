class UserController:
    def __init__ (self,user_service, fonction_service,ui_service):
        self.page = None  # Sera défini dans le main.py
        self.user_service = user_service  # Sera injecté dans le main.py
        self.fonction_service = fonction_service # Sera injecté dans le main.py
        self.ui_service = ui_service # Sera injecté dans le main.py
        self.users = []
        self.pagination = {}
        self.is_loading = False

    def _get_token(self):
        """Centralise la récupération du user_token."""
        # Note : .get() est plus propre que .store.get() sur les versions récentes
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            self.ui_service.show_error("Session expirée. Veuillez vous reconnecter.")
            self.page.go("/login")
            return None
        return user_token

    async def get_all_users(self):
        user_token = self._get_token()
        if not user_token: return

        self.is_loading = True
        self.page.update()

        try:
            self.users, self.pagination = await self.user_service.get_all_users(user_token)
        except Exception as e:
            self.ui_service.show_error(f"Erreur de chargement : {str(e)}")
        finally:
            self.is_loading = False
            self.page.update()

    async def delete_user(self, user_id):
        user_token = self._get_token()
        if not user_token: return
        
        try:
            success = await self.user_service.delete_user(user_id, user_token)
            if success:
                # On rafraîchit la liste localement après suppression
                await self.get_all_users()
            return success
        except Exception as e:
            self.ui_service.show_error("Impossible de supprimer l'utilisateur.")
            return False
    
    async def get_user_by_id(self, user_id):
        """Récupère un user spécifique par ID."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            print("Pas de user_token trouvé, impossible de charger le user.")
            return None
        
        return await self.user_service.get_user_by_id(user_id, user_token)
    
    async def create_user(self, user_data):
        """Crée un nouveau user."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            print("Pas de user_token trouvé, impossible de créer le user.")
            return None
        
        return await self.user_service.create_user(user_data, user_token)
    
    async def update_user(self, user_id, user_data):
        """Met à jour un user existant."""
        user_token = self.page.session.store.get("user_token")
        if not user_token:
            print("Pas de user_token trouvé, impossible de mettre à jour le user.")
            return None
        
        return await self.user_service.update_user(user_id, user_data, user_token)
    