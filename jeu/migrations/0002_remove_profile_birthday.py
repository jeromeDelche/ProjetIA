# Generated by Django 2.2.5 on 2019-12-13 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birthday',
        ),
    ]
