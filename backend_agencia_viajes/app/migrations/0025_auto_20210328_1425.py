# Generated by Django 3.1.2 on 2021-03-28 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20210328_1421'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='calificaion',
            new_name='calificacion',
        ),
    ]