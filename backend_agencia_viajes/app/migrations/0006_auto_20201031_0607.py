# Generated by Django 3.1.2 on 2020-10-31 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_plan_destinos'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinoturistico',
            name='nombre',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
