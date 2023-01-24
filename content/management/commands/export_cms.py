from django.core.management.base import BaseCommand
from wagtail.core.models import Page

from content.models import ContentLandingPage, Section, FlatContent
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        content_landing_pages = []

        landing_pages = ContentLandingPage.objects.all()
        for landing_page in landing_pages:
            l_page = dict(
                pk=landing_page.pk,
                language=landing_page.get_language(),
                intro=landing_page.intro,
                h1=landing_page.title,
                title=landing_page.seo_title,
                translation_pk=landing_page.translated_page_id,
                slug=landing_page.slug if landing_page.slug else ""
            )
            options = []
            for option in landing_page.options:
                p = Page.objects.get(pk=option.value.pk)
                print(f"{p.pk} p.content_type: {p.content_type}")
                options.append((p.pk, p.content_type_id, str(p.content_type)))
            l_page["options"] = options
            content_landing_pages.append(l_page)
        pages = []
        for i in Section.objects.all():
            sections = []
            for sect in i.subsections:
                print(f"section id = {i.pk}")
                sections.append(
                    dict(
                        sect_pk=sect.id,
                        sect_title=sect.value['subsection_title'],
                        sect_content=str(sect.value['subsection_content'])
                    )
                )

            pages.append(
                dict(
                    pk=i.pk,
                    language=i.get_language(),
                    live=i.live,
                    translation_pk=i.translated_page_id,
                    title=i.seo_title,
                    h1=i.title,
                    intro=str(i.intro),
                    sections=sections,
                    slug=i.slug if i.slug else ""
                )
            )

        with open("output.json", "w") as output:
            json.dump(dict(pages=pages, landing_pages=content_landing_pages), output)
