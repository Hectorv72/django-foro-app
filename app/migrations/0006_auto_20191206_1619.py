# Generated by Django 2.2.4 on 2019-12-06 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20191206_1614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tipos_usuarios',
            old_name='nom_tipo_usuario',
            new_name='nom_tipo',
        ),
    ]