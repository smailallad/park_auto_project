import flet as ft

class BaseView(ft.View):
    def __init__(self, page: ft.Page, title: str, route: str, auth_controller):
        super().__init__(route=route)
        self.current_page = page
        self.auth_controller = auth_controller
        if title =="":
            _title="SNC RTIE - Gestion Park Auto"
        else:
            _title=title
        # Éléments communs
        self.appbar = ft.AppBar(
            title=ft.Text(_title,size=14,align=ft.Alignment.CENTER,weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.WHITE,
            # actions=[
            #     ft.IconButton(
            #         icon=ft.Icons.LOGOUT, 
            #         on_click=self.logout
            #     )
            # ]
        )
        # On crée le loading une seule fois ici
        self.loading_indicator = ft.ProgressRing(width=30, height=30, stroke_width=3)
        self.loading_container = ft.Container(
            content=self.loading_indicator,
            alignment=ft.Alignment.CENTER,
            expand=True,
            visible=False # Caché par défaut
        )
        # Zone de contenu vide (à remplir par les enfants)
        self.content_container = ft.Column(expand=True)
        self.content_container.main_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        
        # On utilise un Stack dans le layout de base pour superposer le loading
        self.controls = [
            ft.Stack(
                controls=[
                    self.content_container,      # Le contenu de la page (en dessous)
                    self.loading_container, # Le loader (au-dessus)
                ],
                expand=True
            )
        ]

    def add_content(self, controls: list):
        """Méthode utilitaire pour ajouter des widgets dans le block content"""
        self.content_container.controls.extend(controls)

    def set_loading(self, status: bool):
        """Méthode universelle pour piloter le chargement"""
        self.loading_container.visible = status
        self.content_container.disabled = status # Optionnel : grise le contenu pendant le chargement
        self.current_page.update()

    async def logout(self):
        await self.current_page.push_route("/logout")