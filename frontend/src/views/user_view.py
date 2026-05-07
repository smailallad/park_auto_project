import flet as ft
import asyncio
from views.base_view import BaseView

class UserView(BaseView):
    def __init__(self, page: ft.Page, user_controller):
        # On appelle le constructeur de BaseView (titre, route, etc.)
        super().__init__(
            page=page, 
            title="Gestion des Utilisateurs", 
            route="/users",
            auth_controller=None # Tu peux passer ton controller ici si besoin
        )
        
        self.user_controller = user_controller

        # --- Initialisation des composants spécifiques à cette vue ---
        self.loading = ft.ProgressRing(width=30, height=30, stroke_width=3)
        
        self.loading_container = ft.Container(
            content=self.loading,
            alignment=ft.Alignment.CENTER,
            expand=True,
            visible=False
        )

        self.list_container = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.btn_navigation = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.on_preview),
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self.on_next)
            ]
        )

        # --- Montage du contenu dans le Layout Maître ---
        # On utilise la zone "content_container" définie dans BaseView
        self.add_content([
            ft.Stack(
                controls=[
                    self.list_container,
                    self.loading_container,
                ],
                expand=True
            ),
            self.btn_navigation
        ])

        # Lancer le chargement
        asyncio.create_task(self.load_data())

    # --- Logique (méthodes de classe) ---
    async def load_data(self):
        self.loading_container.visible = True
        self.list_container.disabled = True
        self.page.update()

        await self.user_controller.get_all_users()
        self.build_list()

        self.loading_container.visible = False
        self.list_container.disabled = False
        self.page.update()

    def build_list(self):
        self.list_container.controls.clear()
        for user in self.user_controller.users:
            self.list_container.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(user.nom),
                    subtitle=ft.Text(user.email),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_700,
                        on_click=lambda e, u=user: self.delete_click(u)
                    )
                )
            )

    def delete_click(self, user):
        print(f"Suppression de : {user.nom}")

    def on_preview(self, e):
        print("Page précédente")

    def on_next(self, e):
        print("Page suivante")