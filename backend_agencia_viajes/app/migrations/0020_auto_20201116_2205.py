# Generated by Django 3.1.2 on 2020-11-17 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20201116_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
