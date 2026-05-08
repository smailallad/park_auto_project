import flet as ft
import asyncio
from utils.decorators import handle_api_errors
from views.base_view import BaseView


class VehiculeView(BaseView):
    def __init__(self, page: ft.Page, vehicule_controller):
        super().__init__(
            page=page,
            title="Liste des Véhicules",
            route="/vehicules",
            auth_controller=None,
        )

        self.vehicule_controller = vehicule_controller
        self.list_container = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        # --- Barre de recherche avec bouton X ---
        self.btn_clear = ft.IconButton(
            icon=ft.Icons.CLEAR_ROUNDED,
            icon_color=ft.Colors.GREY_500,
            on_click=self.clear_search,
            visible=False,
        )

        self.search_field = ft.TextField(
            label="Immatriculation, Marque...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            expand=True,
            on_submit=self.on_search_click,
            on_change=self.on_search_change,
            suffix=ft.Row(
                [
                    self.btn_clear,
                    ft.IconButton(
                        ft.Icons.SEARCH_ROUNDED,
                        icon_color=ft.Colors.BLUE_700,
                        on_click=self.on_search_click,
                    ),
                ],
                tight=True,
            ),
        )

        # --- Navigation ---
        self.page_display = ft.Container(
            content=ft.Text("1", size=16, weight="bold", color=ft.Colors.BLUE),
            bgcolor=ft.Colors.BLUE_50,
            padding=10,
            border_radius=25,
            width=50,
            alignment=ft.Alignment.CENTER,
        )

        self.btn_prev = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            style=ft.ButtonStyle(
                color={"disabled": ft.Colors.GREY_400, "": ft.Colors.BLUE_700}
            ),
            disabled=True,
            on_click=self.on_preview,
        )

        self.btn_next = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            style=ft.ButtonStyle(
                color={"disabled": ft.Colors.GREY_400, "": ft.Colors.BLUE_700}
            ),
            disabled=True,
            on_click=self.on_next,
        )

        # --- Layout ---
        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=self.on_add,
            mini=True,
            bgcolor=ft.Colors.BLUE_700,
        )

        self.add_content(
            [
                ft.Container(content=ft.Row([self.search_field]), padding=10),
                ft.Container(
                    content=self.list_container,
                    expand=True,
                    border_radius=20,
                    padding=10,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12),
                ),
                ft.Container(
                    content=ft.Row(
                        [self.btn_prev, self.page_display, self.btn_next],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=10,
                ),
            ]
        )

        asyncio.create_task(self.load_data())

    def refresh(self):
        """La méthode 'magique' qui centralise tout le rendu"""
        # 1. Liste
        self.build_list()
        # 2. Bouton X (visible seulement si texte présent)
        self.btn_clear.visible = bool(self.search_field.value)
        # 3. Pagination
        self.page_display.content.value = f"{self.vehicule_controller.page_index}"
        self.btn_next.disabled = self.vehicule_controller.next_url is None
        self.btn_prev.disabled = self.vehicule_controller.previous_url is None

        self.page.update()

    @handle_api_errors
    async def load_data(self):
        await self.vehicule_controller.get_all_vehicules()
        self.refresh()

    def build_list(self):
        self.list_container.controls.clear()
        for v in self.vehicule_controller.vehicules:
            self.list_container.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.DIRECTIONS_CAR_ROUNDED, color=ft.Colors.BLUE_900
                        ),
                        title=ft.Text(
                            f"{v.marque_nom} • {v.modele_nom} - {v.nom}",
                            weight="bold",
                            size=12,
                        ),
                        # subtitle=ft.Text(v.immatriculation),
                        # On met une Column pour avoir plusieurs "sous-titres"
                        subtitle=ft.Column(
                            spacing=2,  # Espace entre les lignes
                            controls=[
                                # Ligne 1 : Marque et Modèle
                                ft.Text(v.immatriculation, size=10),
                                # Ligne 2 : Statut avec une petite icône
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.CIRCLE,
                                            size=10,
                                            color=(
                                                ft.Colors.GREEN
                                                if v.actif
                                                else ft.Colors.RED
                                            ),
                                        ),
                                        ft.Text(
                                            "En service" if v.actif else "Hors service",
                                            size=10,
                                            italic=True,
                                        ),
                                        ft.Text(
                                            f"{v.kms} km",
                                            size=10,
                                            italic=True,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        is_three_line=True,  # Important : permet à la tuile de s'agrandir
                        trailing=ft.IconButton(
                            ft.Icons.DELETE_OUTLINE_ROUNDED,
                            icon_color=ft.Colors.RED_400,
                            data=v,
                            on_click=self.delete_click,
                        ),
                    ),
                    margin=ft.Margin.only(bottom=5),
                    border=ft.Border.all(1, ft.Colors.GREY_800),
                    border_radius=10,
                )
            )

    async def on_search_change(self, e):
        # On ne recharge pas l'API à chaque lettre (trop lourd),
        # on met juste à jour l'UI (visibilité du bouton X)
        self.btn_clear.visible = bool(e.data)
        self.page.update()

    async def clear_search(self, e):
        self.search_field.value = ""
        self.vehicule_controller.search_text = ""
        self.vehicule_controller.page_index = 1
        self.vehicule_controller.url = None  # Reset URL pour revenir au début
        await self.load_data()

    async def on_preview(self, e):
        self.vehicule_controller.url = self.vehicule_controller.previous_url
        await self.load_data()

    async def on_next(self, e):
        self.vehicule_controller.url = self.vehicule_controller.next_url
        await self.load_data()

    async def on_search_click(self, e):
        self.vehicule_controller.page_index = 1
        self.vehicule_controller.search_text = self.search_field.value
        self.vehicule_controller.url = None
        await self.load_data()

    async def on_add(self, e):
        await self.page.push_route("/vehicules/add")

    async def delete_click(self, e):
        vehicule = e.control.data

        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()

        async def confirm_delete(e):
            # Logique de suppression réelle ici
            await self.vehicule_controller.delete_vehicule(vehicule.id)
            self.page.dialog.open = False
            await self.load_data()

        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmation"),
            content=ft.Text(f"Supprimer le véhicule {vehicule.immatriculation} ?"),
            actions=[
                ft.TextButton("Annuler", on_click=close_dlg),
                ft.TextButton("Supprimer", on_click=confirm_delete),
            ],
        )
        # self.page.dialog.open = True
        self.page.show_dialog(self.page.dialog)
        self.page.update()
