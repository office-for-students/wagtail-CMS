from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from wagtail.documents.models import Document
from wagtail.images.models import Image

from core.utils import check_for_virus

if settings.CLAMAV_ACTIVE:
    @receiver(pre_save, sender=Document)
    def pre_file_save(sender, instance, **kwargs):
        instance = check_for_virus(instance)
        instance.clean()


    @receiver(pre_save, sender=Image)
    def pre_image_save(sender, instance, **kwargs):
        instance = check_for_virus(instance)
        instance.clean()
