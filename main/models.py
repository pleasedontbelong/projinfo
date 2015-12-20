# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Tract(models.Model):
    REGIONS = (
        (44, "Alsace-Champagne-Ardenne-Lorraine"),
        (75, "Aquitaine-Limousin-Poitou-Charentes"),
        (84, "Auvergne-Rhône-Alpes"),
        (27, "Bourgogne-Franche-Comté"),
        (53, "Bretagne"),
        (24, "Centre-Val de Loire"),
        (94, "Corse"),
        (11, "Île-de-France"),
        (76, "Languedoc-Roussillon-Midi-Pyrénées"),
        (32, "Nord-Pas-de-Calais-Picardie"),
        (28, "Normandie"),
        (52, "Pays de la Loire"),
        (93, "Provence-Alpes-Côte d'Azur")
    )
    TOURS = ((1, "1er Tour"), (2, "2eme Tour"))
    url = models.URLField(null=True, blank=True)
    pdf_file = models.FileField(upload_to="pdfs", null=True, blank=True)
    region = models.PositiveSmallIntegerField(null=True, blank=True, choices=REGIONS)
    tour = models.PositiveSmallIntegerField(null=True, blank=True, choices=TOURS)
    nom_de_liste = models.TextField(null=True, blank=True)
    tete_de_liste = models.CharField(max_length=255, null=True, blank=True)
    appreciatifs = models.IntegerField(null=True, blank=True)
    modalite_deontique = models.BooleanField(default=False)
    phrase_deontique = models.TextField(null=True, blank=True)
    deictiques_personnels = models.TextField(null=True, blank=True)
    deictiques_spatiaux = models.TextField(null=True, blank=True)
    deictiques_temporels = models.TextField(null=True, blank=True)

    @property
    def is_filled(self):
        return bool(self.appreciatifs or self.modalite_deontique or self.phrase_deontique or
                    self.deictiques_temporels or self.deictiques_personnels or self.deictiques_spatiaux)
