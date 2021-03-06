# Generated by Django 3.1.2 on 2020-10-31 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201031_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='servicios',
            field=models.ManyToManyField(through='app.HotelServicio', to='app.Servicio'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='tipo_habitaciones',
            field=models.ManyToManyField(through='app.HotelTipoHabitacion', to='app.TipoHabitacion'),
        ),
    ]
