# Generated by Django 4.2.4 on 2023-09-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pemeriksaans', '0003_alter_pemeriksaan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemeriksaan',
            name='diagnosa',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]