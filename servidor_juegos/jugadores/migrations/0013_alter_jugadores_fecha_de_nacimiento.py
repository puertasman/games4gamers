# Generated by Django 5.0.3 on 2024-04-01 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugadores', '0012_remove_jugadores_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugadores',
            name='fecha_de_nacimiento',
            field=models.DateField(auto_now_add=True),
        ),
    ]
