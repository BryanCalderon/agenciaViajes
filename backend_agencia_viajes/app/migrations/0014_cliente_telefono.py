# Generated by Django 3.1.2 on 2020-11-14 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20201114_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]