# Generated by Django 4.2.4 on 2023-08-14 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relasidokterkliniks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relasidokterklinik',
            old_name='id_dokter',
            new_name='dokter',
        ),
        migrations.RenameField(
            model_name='relasidokterklinik',
            old_name='id_klinik',
            new_name='klinik',
        ),
    ]