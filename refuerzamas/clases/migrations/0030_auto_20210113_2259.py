# Generated by Django 3.0.10 on 2021-01-14 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0029_auto_20210111_0401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codigodescuento',
            old_name='porcentaje_descuento',
            new_name='cantidad',
        ),
        migrations.AddField(
            model_name='codigodescuento',
            name='tipo',
            field=models.CharField(default='PORCENTAJE', max_length=20),
        ),
    ]
