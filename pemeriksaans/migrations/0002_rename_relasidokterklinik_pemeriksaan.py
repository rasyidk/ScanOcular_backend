# Generated by Django 4.2.4 on 2023-08-15 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relasidokterkliniks', '0002_rename_id_dokter_relasidokterklinik_dokter_and_more'),
        ('users', '0001_initial'),
        ('pemeriksaans', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Relasidokterklinik',
            new_name='Pemeriksaan',
        ),
    ]
