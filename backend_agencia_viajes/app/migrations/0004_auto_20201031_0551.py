# Generated by Django 3.1.2 on 2020-10-31 05:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201031_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destinoturistico',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='destinoturistico',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='destinoturistico',
            name='titulo',
        ),
        migrations.AddField(
            model_name='plan',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='imagen',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='titulo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
