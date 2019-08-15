# Generated by Django 2.1.8 on 2019-06-19 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('coursefinder', '0008_auto_20190619_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseFinderSummary',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('header', models.TextField(blank=True)),
                ('country_section_title', models.TextField(blank=True)),
                ('mode_of_study_section_title', models.TextField(blank=True)),
                ('subjects_section_title', models.TextField(blank=True)),
                ('narrow_by_section_title', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
