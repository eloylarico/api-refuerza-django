# Generated by Django 3.0.10 on 2020-10-15 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0010_docente_estrellas'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='enlace_videollamada',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
