# Generated by Django 2.2.3 on 2019-08-14 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('coursefinder', '0014_auto_20190812_1313'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseFinderTownCity',
        ),
    ]
