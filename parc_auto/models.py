from django.db import models
from django.core.validators import RegexValidator


class Marque(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom


class Modele(models.Model):
    nom = models.CharField(max_length=50)
    # Relation (1,N) : Une marque a plusieurs modèles, un modèle a une seule marque
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name="modeles")

    def __str__(self):
        return f"{self.marque.nom} {self.nom}"


class Vehicule(models.Model):
    nom = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(r"^[A-Z]$", "Seulement une lettre majuscule de A à Z")
        ],
    )
    immatriculation = models.CharField(
        max_length=20,
        unique=True,
        error_messages={"unique": "Cette immatriculation est déjà utilisée."},
    )
    modele = models.ForeignKey(
        Modele, on_delete=models.PROTECT, related_name="vehicules"
    )

    kms = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nom", "modele"],
                name="unique_nom_par_modele",
                violation_error_message="Ce code lettre est déjà utilisé pour ce modèle.",
            ),
        ]

    def save(self, *args, **kwargs):
        # Force la mise en majuscule avant la sauvegarde
        if self.nom:
            self.nom = self.nom.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.modele.nom} - {self.nom} - ({self.immatriculation})"


class Entretien(models.Model):
    vehicule = models.ForeignKey(
        Vehicule, on_delete=models.PROTECT, related_name="entretiens"
    )
    date_intervention = models.DateField()
    description = models.TextField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Entretien {self.vehicule.immatriculation} du {self.date_intervention}"
