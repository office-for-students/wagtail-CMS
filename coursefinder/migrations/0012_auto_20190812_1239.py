# Generated by Django 2.2.3 on 2019-08-12 12:39

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('coursefinder', '0011_delete_coursefinderlandingpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefinderchoosecountry',
            name='helper_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
