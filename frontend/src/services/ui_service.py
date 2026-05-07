import flet as ft

class UIService:
    def __init__(self):
        self.page = None # Sera injecté comme pour les contrôleurs

    def show_error(self, message: str):
        if not self.page:
            print(f"Erreur (sans page) : {message}")
            return
        
        self.page.show_dialog(ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
        ))
        self.page.update()

    def show_success(self, message: str):
        if not self.page: 
            print(f"Erreur (sans page) : {message}")
            return
        
        self.page.show_dialog(ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700,
        ))
        self.page.update()