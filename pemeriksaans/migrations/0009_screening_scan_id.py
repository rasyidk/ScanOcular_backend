# Generated by Django 4.2.4 on 2023-09-05 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pemeriksaans', '0008_rename_user_id_screening_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='screening',
            name='scan_id',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]