# Generated by Django 4.1 on 2022-10-28 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_rename_bloques_bloque_rename_cultivos_cultivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloque',
            name='dia_finalizar',
        ),
        migrations.RemoveField(
            model_name='bloque',
            name='precio',
        ),
    ]
