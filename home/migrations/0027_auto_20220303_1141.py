# Generated by Django 2.2.13 on 2022-03-03 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20220303_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='informational_text',
            field=models.TextField(blank=True),
        ),
    ]
