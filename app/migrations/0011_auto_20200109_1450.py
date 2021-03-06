# Generated by Django 3.0.1 on 2020-01-09 17:50

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_comentarios_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestas',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to=app.models.subir_archivo),
        ),
        migrations.AlterField(
            model_name='comentarios',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to=app.models.subir_archivo_comentario),
        ),
        migrations.AlterField(
            model_name='foros',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to=app.models.subir_archivo),
        ),
    ]
