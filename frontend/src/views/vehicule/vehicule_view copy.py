import flet as ft
import asyncio
from utils.decorators import handle_api_errors
from views.base_view import BaseView

class VehiculeView(BaseView):
    def __init__(self, page: ft.Page, vehicule_controller):
        # On initialise la classe parente
        super().__init__(
            page=page,
            title="Liste des Véhicules",
            route="/vehicules",
            auth_controller=None,
        )

        self.vehicule_controller = vehicule_controller

        self.search_field = ft.TextField(
            # key="search_field",
            label="Rechercher par immatriculation",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=15,
            expand=True,
            on_submit=self.on_search_click,  # Permet aussi de valider avec la touche 'Entrée'
            suffix=ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD_ROUNDED,  # Ou ft.Icons.SEARCH
                icon_color=ft.Colors.BLUE,
                on_click=self.on_search_click,  # Déclenche la recherche
            ),
        )
        self.list_container = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # --- Dans __init__ ---

        self.page_display = ft.Container(
            content=ft.Text(
                f"{self.vehicule_controller.page_index}",
                size=16,
                weight="bold",
                color=ft.Colors.BLUE,
            ),
            bgcolor=ft.Colors.BLUE_50,
            padding=ft.Padding.all(10),
            border_radius=ft.BorderRadius.all(25),
            width=50,
            alignment=ft.Alignment.CENTER,
        )

        # Bouton Précédent
        self.btn_prev = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            # icon_color=ft.Colors.BLUE_700,
            # On définit un style spécifique pour l'état désactivé
            style=ft.ButtonStyle(
                color={
                    "disabled": ft.Colors.GREY_400,
                    "": ft.Colors.BLUE_700,  # "" correspond à l'état par défaut
                },
            ),
            tooltip="Page précédente",
            disabled=True,  # Désactivé par défaut
            on_click=self.on_preview,
        )

        # Bouton Suivant
        self.btn_next = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            # icon_color=ft.Colors.BLUE_700,
            # On définit un style spécifique pour l'état désactivé
            style=ft.ButtonStyle(
                color={
                    "disabled": ft.Colors.GREY_400,
                    "": ft.Colors.BLUE_700,  # "" correspond à l'état par défaut
                },
            ),
            tooltip="Page suivante",
            disabled=True,  # Désactivé par défaut
            on_click=self.on_next,
        )
        self.btn_navigation = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            controls=[
                self.btn_prev,
                self.page_display,
                self.btn_next,
            ],
        )

        self.add_button = ft.IconButton(
            icon=ft.Icons.ADD_OUTLINED,
            icon_color=ft.Colors.BLUE_700,
            bgcolor=ft.Colors.BLUE_50,
            hover_color=ft.Colors.BLUE_100,
            on_click=self.on_add,
        )

        self.add_content(
            [
                # Barre de recherche avec un peu de marge
                ft.Container(
                    ft.Row(
                        controls=[
                            self.search_field,
                            self.add_button,
                        ],
                    ),
                    # margin=ft.Margin.only(bottom=10),
                ),
                # Liste avec bordure subtile
                ft.Container(
                    content=self.list_container,
                    expand=True,
                    border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=15,
                    padding=5,
                    # bgcolor=ft.Colors.SURFACE_VARIANT if page.dark_theme else ft.Colors.WHITE,
                ),
                # Espace
                # ft.Container(height=20),
                # Barre d'action avec Add et Navigation sur la même ligne ou empilés
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # self.add_button,
                        # ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        self.btn_navigation,
                    ],
                ),
            ]
        )
        # Lancement asynchrone du chargement
        asyncio.create_task(self.load_data())

    @handle_api_errors  # self.list_container.update()\
    async def load_data(self):
        await self.vehicule_controller.get_all_vehicules()
        self.build_list()

        self.page_display.content.value = f"{self.vehicule_controller.page_index}"
        # 2. On active ou désactive les boutons selon la présence d'un lien
        self.btn_next.disabled = (
            True if self.vehicule_controller.next_url is None else False
        )
        self.btn_prev.disabled = (
            True if self.vehicule_controller.previous_url is None else False
        )

        self.page.update()

    def build_list(self):
        self.list_container.controls.clear()

        for vehicule in self.vehicule_controller.vehicules:
            self.list_container.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DIRECTIONS_CAR),
                    title=ft.Text(vehicule.immatriculation),
                    subtitle=ft.Text(f"{vehicule.marque} {vehicule.modele}"),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_700,
                        hover_color=ft.Colors.BLUE_GREY_700,
                        on_click=lambda e, v=vehicule: self.delete_click(v),
                    ),
                )
            )

    def delete_click(self, vehicule):
        print(f"Suppression demandée pour : {vehicule.immatriculation}")

    async def on_preview(self, e):
        self.vehicule_controller.url = self.vehicule_controller.previous_url
        await self.load_data()

    async def on_next(self, e):
        self.vehicule_controller.url = self.vehicule_controller.next_url
        await self.load_data()

    async def on_add(self, e):
        await self.page.push_route("/vehicules/add")

    async def on_search_click(self, e):
        self.vehicule_controller.page_index = 1
        self.vehicule_controller.search_text = self.search_field.value
        await self.load_data()
