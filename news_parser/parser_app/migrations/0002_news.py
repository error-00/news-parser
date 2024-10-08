# Generated by Django 4.2.2 on 2023-06-13 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=250)),
                ('photo', models.CharField(blank=True, max_length=150, null=True)),
                ('published', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
    ]
