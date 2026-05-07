import flet as ft

def LoginView(page: ft.Page, auth_controller):
    # Champs de saisie
    txt_user = ft.TextField(label="Utilisateur",value="smail", border_radius=10, prefix_icon=ft.Icons.PERSON)
    txt_pass = ft.TextField(label="Mot de passe",value="smail", password=True, can_reveal_password=True, border_radius=10, prefix_icon=ft.Icons.LOCK)
    
    # Indicateur de chargement (caché par défaut)
    loading_ring = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)

    async def on_login_click(e):
        # Désactiver le bouton et montrer le chargement
        btn_login.disabled = True
        loading_ring.visible = True
        page.update()

        # Appel au contrôleur
        await auth_controller.login(txt_user.value, txt_pass.value)

        # Réactiver si échec (si succès, le contrôleur aura déjà changé de page)
        btn_login.disabled = False
        loading_ring.visible = False
        page.update()

    btn_login = ft.Button(
        "Se connecter", 
        on_click=on_login_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    return ft.View(
        route="/login",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("SNC RTIE", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Gestion flotte automobile Sécurisée.", color=ft.Colors.GREY_500),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    txt_user,
                    txt_pass,
                    ft.Row([btn_login, loading_ring], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                # bgcolor=ft.Colors.GREY_500,
                border_radius=20,
                width=350
            )
        ]
    )