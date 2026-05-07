import functools
import flet as ft

from utils.exceptions import APIError, AuthenticationError, NetworkError

def handle_api_errors(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            # 1. On active le loading avant d'appeler la fonction
            if hasattr(self, "set_loading"):
                self.set_loading(True)

            return await func(self, *args, **kwargs)
        
        except AuthenticationError:
            print("Session expirée détectée par le décorateur")
            self.current_page.session.store.set("is_logged_in", False)
            self.current_page.session.store.remove("user_token")
            self.current_page.session.store.remove("user_refresh")
            await self.current_page.push_route("/login")
            
            self.current_page.show_dialog(ft.SnackBar(
                 ft.Text("Session expirée. Veuillez vous reconnecter."),
                bgcolor=ft.Colors.RED_700
                )
            )

        except APIError:
            print("Erreur API détectée par le décorateur")
            self.current_page.show_dialog(ft.SnackBar(
                 ft.Text("Erreur API détectée. Veuillez réessayer plus tard."),
                bgcolor=ft.Colors.RED_700
                )
            )
        
        except NetworkError:
            print("Problème de connexion internet ou serveur HS.")
            self.current_page.show_dialog(ft.SnackBar(
                 ft.Text("Problème de connexion internet ou serveur HS."),
                bgcolor=ft.Colors.RED_700
                )
            )

        except Exception as e:
            print(f"Erreur capturée : {e}")
            self.current_page.show_dialog(ft.SnackBar(
                 ft.Text(f"Une erreur est survenue : {str(e)}"),
                bgcolor=ft.Colors.RED_700
                )
            )

            self.current_page.update()
        
        finally:
            # 2. On désactive le loading quoi qu'il arrive
            if hasattr(self, "set_loading"):
                self.set_loading(False)
        
        return None
    return wrapper