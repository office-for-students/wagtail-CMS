# Generated by Django 2.2.4 on 2019-09-10 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_search', '0002_searchlandingpage_translated_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchlandingpage',
            name='course_finder_button_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchlandingpage',
            name='search_button_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
