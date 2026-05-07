import flet as ft
from views.home_view import HomeView
from views.login_view import LoginView
from views.user_view import UserView
from views.vehicule.vehicule_add_view import VehiculeAddView
from views.vehicule.vehicule_view import VehiculeView


class Router:
    def __init__(self, page: ft.Page, container):
        self.page = page
        self.container = container

        # Récupération des contrôleurs/services depuis le container
        self.auth_controller = container.auth_controller()
        self.auth_controller.page = page

        self.user_controller = container.user_controller()
        self.user_controller.page = page

        self.modele_controller = container.modele_controller()
        self.modele_controller.page = page

        self.vehicule_controller = container.vehicule_controller()
        self.vehicule_controller.page = page

        ui_service = container.ui_service()
        ui_service.page = page

    async def route_change(self, e=None):
        self.page.views.clear()

        # Sécurité : Vérification de la session
        is_auth = self.page.session.store.get("is_logged_in")  # Simplifié

        if not is_auth and self.page.route != "/login":
            await self.page.push_route("/login")
            return

        # Logique de routage
        match self.page.route:
            case "/":
                self.page.views.append(HomeView(self.page, self.auth_controller))
            case "/login":
                self.page.views.append(LoginView(self.page, self.auth_controller))
            case "/logout":
                await self.auth_controller.logout()
                return
            case "/users":
                self.page.views.append(HomeView(self.page, self.auth_controller))
                self.page.views.append(UserView(self.page, self.user_controller))
            case "/vehicules":
                self.page.views.append(HomeView(self.page, self.auth_controller))
                self.page.views.append(
                    VehiculeView(self.page, self.vehicule_controller)
                )
            case "/vehicules/add":
                self.page.views.append(HomeView(self.page, self.auth_controller))
                self.page.views.append(
                    VehiculeView(self.page, self.vehicule_controller)
                )
                self.page.views.append(
                    VehiculeAddView(
                        self.page, self.vehicule_controller, self.modele_controller
                    )
                )

        self.page.update()

    async def view_pop(self, e):
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            await self.page.push_route(top_view.route)
