# Generated by Django 4.0.3 on 2022-04-27 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apostas', '0002_aposta_dataa_aposta_valor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100)),
                ('id_indicado', models.IntegerField(default=-1)),
            ],
        ),
    ]
