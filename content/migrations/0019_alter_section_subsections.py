# Generated by Django 3.2.13 on 2022-07-11 12:06

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20191009_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='subsections',
            field=wagtail.core.fields.StreamField([('subsection', wagtail.core.blocks.StructBlock([('subsection_title', wagtail.core.blocks.TextBlock()), ('subsection_content', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'bold', 'underline', 'italic', 'embed', 'link', 'image', 'ol', 'ul', 'hr', 'blockquote']))]))]),
        ),
    ]
