# Generated by Django 2.2.4 on 2019-09-06 11:03

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_coursemanagepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemanagepage',
            name='none_selected_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
