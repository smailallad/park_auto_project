import functools
from utils.exceptions import APIError, AuthenticationError, NetworkError, ValidatorError

# On importe l'instance de ton container (celle qui est initialisée dans ton main.py)
from config.container import container


def handle_api_errors(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        # 1. Accès au Singleton via le provider de dependency-injector
        ui_service = container.ui_service()

        # 2. Synchronisation de la page
        if hasattr(self, "current_page"):
            ui_service.page = self.current_page

        try:
            if hasattr(self, "set_loading"):
                self.set_loading(True)

            return await func(self, *args, **kwargs)

        except AuthenticationError:
            # Nettoyage session
            self.current_page.session.store.remove("user_token")
            self.current_page.session.store.remove("user_refresh")

            ui_service.show_error("Session expirée. Veuillez vous reconnecter.")
            self.current_page.go("/login")

        except NetworkError:
            ui_service.show_error("Serveur injoignable ou problème réseau.")

        except ValidatorError as e:
            # ui_service.show_error(f"Erreur de validation : {str(e)}")
            # e est l'objet exception.
            # Les données passées lors du 'raise' sont dans e.args[0]
            error_data = e.args[0] if e.args else str(e)

            # Si c'est un dictionnaire (cas de ton erreur Django)
            if isinstance(error_data, dict):
                # On prend le premier message d'erreur trouvé
                # Ex: {'immatriculation': ['Ce véhicule est déjà répertorié.']}
                first_key = next(iter(error_data))
                message = error_data[first_key][0]
                ui_service.show_error(f"{message}")
            else:
                ui_service.show_error(f"Erreur : {error_data}")

        except Exception as e:
            print(f"Erreur non gérée : {e}")
            ui_service.show_error(f"Erreur : {str(e)}")

        except APIError:  # On attrape les autres erreurs API génériques
            ui_service.show_error("Erreur serveur (API).")

        finally:
            if hasattr(self, "set_loading"):
                self.set_loading(False)

        return None

    return wrapper
