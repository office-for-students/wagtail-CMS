# Generated by Django 2.1.8 on 2019-06-19 09:22

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coursefinder', '0006_coursefinderpostcode_coursefindertowncity_coursefinderuni'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefinderlandingpage',
            name='next_section',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.PageChooserBlock())], default=''),
            preserve_default=False,
        ),
    ]
