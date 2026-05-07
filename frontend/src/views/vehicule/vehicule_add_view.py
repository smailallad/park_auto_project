import asyncio

import flet as ft
from utils.decorators import handle_api_errors
from views.base_view import BaseView


class VehiculeAddView(BaseView):
    def __init__(self, page: ft.Page, vehicule_controller, modele_controller):
        # On initialise la classe parente
        super().__init__(
            page=page, title="", route="/vehicules/add", auth_controller=None
        )

        self.vehicule_controller = vehicule_controller
        self.modele_controller = modele_controller

        self.txt_immatriculation = ft.TextField(
            label="Immatriculation", border_radius=10
        )
        self.dd_modele = ft.Dropdown(
            label="Modèle",
            border_radius=10,
            options=[],
        )

        self.txt_nom = ft.TextField(
            label="Code Lettre (ex: A, B, C)",
            border_radius=10,
            max_length=1,  # On limite à 1 caractère
            hint_text="Une seule lettre",
            capitalization=ft.TextCapitalization.CHARACTERS,  # Ouvre le clavier en MAJ sur Android/iOS
            on_change=self.force_upper,  # On force la majuscule pendant la saisie
        )

        self.container = ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_900,  # Optionnel : pour le détacher du fond
            border_radius=15,
            padding=30,
            expand=True,
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        # tight=True,  # Force la colonne à ne prendre que la place de ses enfants
                        col={"xs": 12, "md": 6, "lg": 4},  # Largeur adaptative
                        offset={"md": 3, "lg": 4},  # Centre le formulaire sur PC
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=20,
                        controls=[
                            ft.Text("Nouveau Véhicule", size=20, weight="bold"),
                            self.txt_immatriculation,
                            self.dd_modele,
                            self.txt_nom,
                            ft.Button(
                                "Enregistrer",
                                icon=ft.Icons.SAVE,
                                on_click=self.on_save,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                height=40,
                            ),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Aide au centrage global
            ),
        )

        # --- Montage dans le layout (BaseView) ---
        self.add_content(
            [
                ft.Container(
                    content=self.container,  # Ton formulaire
                    alignment=ft.Alignment.CENTER,  # Centre horizontal + vertical
                    expand=True,  # Prend toute la place disponible dans BaseView
                ),
            ]
        )

        asyncio.create_task(self.load_data())

    @handle_api_errors
    async def on_save(self):
        self.txt_immatriculation.error = None

        is_valid = True

        if len(self.txt_immatriculation.value.strip()) < 3:
            self.txt_immatriculation.error = "Min 3 caractères."
            is_valid = False

        # Validation du nouveau champ Nom
        if (
            len(self.txt_nom.value.strip()) == 0
            or not self.txt_nom.value.strip()
            or not self.txt_nom.value.isalpha()
        ):
            print("Validation échouée pour le champ Nom:", self.txt_nom.value)
            self.txt_nom.error = "Lettre (A-Z)."
            is_valid = False

        if not is_valid:
            self.current_page.update()
            return

        vehicule = {
            "immatriculation": self.txt_immatriculation.value,
            "nom": self.txt_nom.value.upper(),  # On force la majuscule avant l'envoi
            "modele_id": int(self.dd_modele.value),
        }

        result = await self.vehicule_controller.create_vehicule(vehicule)
        if result:
            self.txt_immatriculation.value = ""
            self.txt_nom.value = ""
        self.current_page.update()

    # Fonction pour forcer les majuscules en temps réel
    def force_upper(self, e):
        e.control.value = e.control.value.upper()
        self.current_page.update()

    async def load_data(self):
        await self.modele_controller.get_all_modeles()
        print(
            "VehiculeAddView - load_data appelé"
        )  # Debug: Vérifie que la méthode est appelée
        print(
            self.modele_controller.modeles
        )  # Debug: Affiche les modèles chargés dans le controller
        if self.modele_controller.modeles:
            self.dd_modele.options = [
                ft.dropdown.Option(key=str(m.id), text=f"{m.marque_nom} - {m.nom}")
                for m in self.modele_controller.modeles
            ]
            self.page.update()
