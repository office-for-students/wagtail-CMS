from django.core.management.base import BaseCommand
from content.models import ContentLandingPage, Section, FlatContent
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        pages = []
        for i in Section.objects.all():
            sections = []
            for sect in i.subsections:
                sections.append(
                    dict(
                        sect_pk=sect.id,
                        sect_title=sect.value['subsection_title'],
                        sect_content=str(sect.value['subsection_content'])
                    )
                )
            # print("translated= {}".format(i.translated_page_id))
            pages.append(
                dict(
                    pk = i.pk,
                    live=i.live,
                    translation_pk=i.translated_page_id,
                    title=i.title,
                    intro=str(i.intro),
                    sections=sections
                )
            )

        with open("output.json", "w") as output:
            json.dump(pages, output)
