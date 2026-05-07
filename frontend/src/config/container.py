from dependency_injector import containers, providers

from controllers.user_controller import UserController
from controllers.auth_controller import AuthController
from controllers.vehicule_controller import VehiculeController
from controllers.modele_controller import ModeleController

from services.ui_service import UIService

from services.auth_service import AuthService
from services.user_service import UserService
from services.fonction_service import FonctionService
from services.vehicule_service import VehiculeService
from services.modele_service import ModeleService


class Container(containers.DeclarativeContainer):
    # Fournisseurs de configuration
    # config = providers.Configuration()

    # Services
    ui_service = providers.Singleton(UIService)

    auth_service = providers.Singleton(AuthService)
    user_service = providers.Singleton(UserService)
    fonction_service = providers.Singleton(FonctionService)
    modele_service = providers.Singleton(ModeleService)
    vehicule_service = providers.Singleton(VehiculeService)

    # Le Contrôleur devient un Singleton
    # On injecte uniquement le service. La 'page' sera injectée plus tard (Setter Injection)
    auth_controller = providers.Singleton(
        AuthController, auth_service=auth_service, ui_service=ui_service
    )

    user_controller = providers.Singleton(
        UserController,
        user_service=user_service,
        fonction_service=fonction_service,
        ui_service=ui_service,
    )
    # # Contrôleurs devient un factory en garde pas ses variable en memoire.
    # # Notez comment on "injecte" le service dans le contrôleur automatiquement
    # auth_controller = providers.Factory(
    #     AuthController,
    #     auth_service=auth_service
    # )
    vehicule_controller = providers.Singleton(
        VehiculeController, vehicule_service=vehicule_service, ui_service=ui_service
    )

    modele_controller = providers.Singleton(
        ModeleController,
        modele_service=modele_service,
        ui_service=ui_service,
    )


container = Container()
