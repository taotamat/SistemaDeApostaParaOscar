# Generated by Django 4.0.3 on 2022-04-12 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0011_rename_tomatoe_filme_tomatoes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filme',
            name='ava_tomatoes',
        ),
    ]