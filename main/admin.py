from django.contrib import admin
from .models import Tract


class TractAdmin(admin.ModelAdmin):
    model = Tract
    list_filter = ('region', 'tour')
    list_display = ('identif', 'region', 'tour', 'nom_de_liste',
                    'tete_de_liste', 'appreciatifs', 'modalite_deontique',
                    'deictiques_personnels', 'deictiques_spatiaux', 'deictiques_temporels')

    def identif(self, obj):
        color = "#DFD" if obj.is_filled else ""
        return u"<div style='width:100%; height:100%; background-color:{};''>{}_{}_{}</div>".format(
            color,
            obj.tour,
            obj.region,
            obj.nom_de_liste[:5]
        )
    identif.allow_tags = True

admin.site.register(Tract, TractAdmin)
