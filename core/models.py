from wagtail.core.models import Page


class DiscoverUniBasePage(Page):

    def get_language(self):
        if '/cy/' in self.get_full_url():
            return 'cy'
        return 'en'

    class Meta:
        abstract = True
