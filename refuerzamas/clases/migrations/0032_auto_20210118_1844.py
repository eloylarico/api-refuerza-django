# Generated by Django 3.0.10 on 2021-01-18 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0031_auto_20210113_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='estado_foto_pago',
            field=models.CharField(choices=[('Evaluada', 'Evaluada'), ('Comprobada', 'Comprobada'), ('Observada', 'Observada')], default='Evaluada', max_length=100),
        ),
        migrations.AddField(
            model_name='reserva',
            name='texto_pago',
            field=models.TextField(blank=True, help_text='Texto dentro de la foto que sube el usuario al crear la reserva', null=True),
        ),
        migrations.AlterField(
            model_name='codigodescuento',
            name='tipo',
            field=models.CharField(choices=[('PORCENTAJE', 'Porcentaje'), ('MONTO', 'Monto')], default='PORCENTAJE', max_length=20),
        ),
    ]
