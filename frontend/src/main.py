import flet as ft

from config.container import container
# from config.container import Container
from router import Router

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    
    # 1. Initialiser les dépendances
    # container = Container()

    # 2. Initialiser le routeur
    router = Router(page, container)
    
    # 3. Lier les événements au routeur
    page.on_route_change = router.route_change
    page.on_view_pop = router.view_pop
    
    # 4. Lancement initial
    await router.route_change()
     
ft.run(main)