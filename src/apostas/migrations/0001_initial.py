# Generated by Django 4.0.3 on 2022-04-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usuario', models.IntegerField(default=-1)),
                ('categoria', models.CharField(max_length=100)),
                ('pos1', models.IntegerField(default=-1)),
                ('pos2', models.IntegerField(default=-1)),
                ('pos3', models.IntegerField(default=-1)),
                ('pos4', models.IntegerField(default=-1)),
                ('pos5', models.IntegerField(default=-1)),
                ('pos6', models.IntegerField(default=-1)),
                ('pos7', models.IntegerField(default=-1)),
                ('pos8', models.IntegerField(default=-1)),
                ('pos9', models.IntegerField(default=-1)),
                ('pos10', models.IntegerField(default=-1)),
            ],
        ),
    ]