# Generated by Django 5.0.3 on 2024-04-02 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugadores', '0016_remove_jugadores_activa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugadores',
            name='fecha_de_nacimiento',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
