# Generated by Django 4.2.2 on 2023-06-13 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0002_news'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='Articles',
        ),
    ]
