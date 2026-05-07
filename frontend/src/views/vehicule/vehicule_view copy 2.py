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
        # Barre de recherche améliorée ---
        self.search_field = ft.TextField(
            label="Immatriculation, Marque...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            expand=True,
            on_submit=self.on_search_click,
            # On ajoute un bouton "X" à droite qui vide le champ
            suffix=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.CLEAR_ROUNDED,
                        icon_color=ft.Colors.GREY_500,
                        tooltip="Effacer la recherche",
                        on_click=self.clear_search,  # Nouvelle méthode
                        visible=False,  # Caché par défaut
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SEARCH_ROUNDED,
                        icon_color=ft.Colors.BLUE_700,
                        on_click=self.on_search_click,
                    ),
                ],
                tight=True,
            ),
            on_change=self.on_search_change,  # Pour afficher/cacher le X
        )

        # Bouton d'ajout "Action" ---
        self.add_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=self.on_add,
            tooltip="Ajouter un véhicule",
            mini=True,
        )

        # Ajout du bouton flottant à la vue
        self.floating_action_button = self.add_button

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

        # Boutons de navigation regroupés
        self.btn_navigation = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            controls=[
                self.btn_prev,
                self.page_display,
                self.btn_next,
            ],
        )

        # Disposition du Layout ---
        self.add_content(
            [
                # Header : Recherche
                ft.Container(
                    content=ft.Row([self.search_field]),
                    padding=ft.Padding(10, 5, 10, 10),
                ),
                # Corps : Liste (avec une zone plus large)
                ft.Container(
                    content=self.list_container,
                    expand=True,
                    # bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
                    padding=10,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12),
                ),
                # Footer : Navigation élégante
                ft.Container(
                    content=ft.Row(
                        [
                            self.btn_prev,
                            self.page_display,
                            self.btn_next,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=10,
                    # bgcolor=ft.Colors.GREY_50,
                ),
            ]
        )

        # Lancement asynchrone du chargement
        asyncio.create_task(self.load_data())

    @handle_api_errors  # Décorateur pour gérer les erreurs d'API
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
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.DIRECTIONS_CAR_ROUNDED, color=ft.Colors.BLUE_900
                        ),
                        title=ft.Text(vehicule.immatriculation.upper(), weight="bold"),
                        subtitle=ft.Text(f"{vehicule.marque} • {vehicule.modele}"),
                        trailing=ft.IconButton(
                            ft.Icons.DELETE_OUTLINE_ROUNDED,
                            icon_color=ft.Colors.RED_400,
                            on_click=lambda e, v=vehicule: self.delete_click(v),
                        ),
                    ),
                    margin=ft.Margin.only(bottom=5),
                    border=ft.Border.all(1, ft.Colors.GREY_800),
                    border_radius=10,
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

    async def on_search_change(self, e):
        # On affiche le bouton X uniquement s'il y a du texte
        self.search_field.suffix.controls[0].visible = True if e.data else False
        self.page.update()

    async def clear_search(self, e):
        self.search_field.value = ""
        self.search_field.suffix.controls[0].visible = False
        self.vehicule_controller.search_text = ""
        self.vehicule_controller.page_index = 1
        await self.load_data()
