# -*- coding: utf-8 -*-
# import os
import tempfile
import requests
import json
from django.core.management.base import BaseCommand
from django.core.files.base import File
from main.models import Tract


class Command(BaseCommand):
    help = 'Downloads and parses the files'

    def handle(self, *args, **options):
        page_format = "http://www.programme-candidats.interieur.gouv.fr/data-jsons/" \
                      "elections-{tour}-regions-{region}-candidacies.json"
        # html_dir = os.path.join(os.path.dirname(__file__), "json")
        pdf_filename = "{id}_{tour}_{region}.pdf"
        pdf_base = "http://www.programme-candidats.interieur.gouv.fr/{pdf_file}"
        for tour in Tract.TOURS:
            for region in Tract.REGIONS:
                tour_id = tour[0]
                region_id = region[0]
                url = page_format.format(tour=tour_id, region=region_id)
                self.stdout.write(self.style.SUCCESS(
                    "Downloading %s" % url
                ))
                r = requests.get(url)
                content_json = json.loads(r.content)

                for tract in content_json['lists']:
                    pdf_url = pdf_base.format(pdf_file=tract['propagande'])
                    pdf_file = self.download_file(pdf_url)
                    if not pdf_file:
                        self.stdout.write(self.style.ERROR(
                            "Error Downloading %s" % pdf_url
                        ))
                        continue
                    tract = Tract.objects.create(
                        url=pdf_url,
                        region=region_id,
                        tour=tour_id,
                        nom_de_liste=tract["name"],
                        tete_de_liste=tract["principal"]
                    )
                    tract.pdf_file.save(
                        name=pdf_filename.format(
                            id=tract.pk,
                            tour=tour_id,
                            region=region_id),
                        content=File(pdf_file))
                    pdf_file.close()

    def download_file(self, url):
        self.stdout.write(
            "Downloading %s" % url
        )
        handle = tempfile.TemporaryFile()
        response = requests.get(url)

        if not response.ok:
            return False

        handle.write(response.content)
        return handle
