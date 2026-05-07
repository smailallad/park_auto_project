import flet as ft

from config.config import myColors


def HomeView(page: ft.Page, auth_controller):

    async def on_logout_click(e):
        await page.push_route("/logout")

    def create_task():
        print("Call create task")

    async def handle_show_drawer():
        await page.show_drawer()

    def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
        print("Drawer dismissed!")

    async def handle_change(e: ft.Event[ft.NavigationDrawer]):
        match e.control.selected_index:
            case 0:
                print("Marque Vehicule")
                await page.push_route("/users")
            case 1:
                print("Vehicule")
                await page.push_route("/vehicules")
            case 2:
                print("Entretien")
            case 3:
                print("Quitter")
                await page.push_route("/logout")
                return
        await page.close_drawer()

    mydrawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            # ft.Container(height=8),
            ft.NavigationDrawerDestination(
                label="Marque Vehicule",
                icon=ft.Icons.CAR_REPAIR_OUTLINED,
                # selected_icon=ft.Icon(ft.Icons.CAR_REPAIR),
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.DIRECTIONS_CAR_OUTLINED),
                label="Vehicule",
                # selected_icon=ft.Icons.DIRECTIONS_CAR,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.SETTINGS_OUTLINED),
                label="Entretien",
                # selected_icon=ft.Icons.SETTINGS,
            ),
            # L'espaceur dynamique au lieu de height=500
            ft.Column([ft.Container()], expand=True),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.LOGOUT_OUTLINED),
                label="Quitter",
                # selected_icon=ft.Icons.LOGOUT,
            ),
        ],
        # Désactive visuellement l'indicateur de sélection
        indicator_color=ft.Colors.TRANSPARENT,
        tile_padding=ft.Padding(top=10, left=10, right=10, bottom=0),
    )

    menu_bar = ft.Row(
        # alignment='spaceBetween',
        controls=[
            ft.IconButton(  # On remplace le Container par un IconButton
                icon=ft.Icons.MENU,
                align=ft.Alignment.CENTER_LEFT,
                on_click=handle_show_drawer,
            ),
            ft.Text(
                "SNC RTIE - Gestion Parc Auto",
                align=ft.Alignment.CENTER,
                expand=True,
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            # ft.Row(
            #     controls=[
            #         ft.Icon(ft.Icons.SEARCH),
            #         ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED)
            #     ]
            # )
        ]
    )

    titre1 = ft.Text(value="SNC RTIE")

    titre2 = ft.Text(value="Gestion Parc Auto")

    list_cards = []

    my_cards = ft.Container(
        padding=ft.Padding.only(top=10, bottom=20), content=list_cards
    )

    page_home = ft.Container(
        padding=20,
        # width=400,
        # height=450,
        expand=True,
        # bgcolor=myColors.BG,
        # border_radius=35,
        content=ft.Column(
            controls=[
                menu_bar,
                # titre1,
                # titre2,
                my_cards,
                # ft.Text("TITRE"),
                ft.Stack(
                    height=200,
                    controls=[
                        # autres,
                        # ft.FloatingActionButton(
                        #     icon=ft.Icons.ADD,on_click=create_task
                        # )
                    ],
                ),
            ]
        ),
    )

    return ft.View(
        route="/",
        drawer=mydrawer,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=page_home,
                expand=True,
            )
        ],
    )
