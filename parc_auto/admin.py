from django.contrib import admin

from parc_auto.models.models import Modele, Marque, Vehicule, Entretien

# On importe depuis le package models


admin.site.register(Modele)
admin.site.register(Marque)
admin.site.register(Vehicule)
admin.site.register(Entretien)
