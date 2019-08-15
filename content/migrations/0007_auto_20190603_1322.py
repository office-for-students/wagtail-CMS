# Generated by Django 2.1.8 on 2019-06-03 13:22

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20190603_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='related_links',
            field=wagtail.core.fields.StreamField([('links', wagtail.core.blocks.PageChooserBlock())], default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='related_links_title',
            field=models.TextField(blank=True),
        ),
    ]
