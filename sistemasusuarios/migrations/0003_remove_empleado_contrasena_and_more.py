# Generated by Django 5.0.4 on 2024-04-10 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistemasusuarios', '0002_empleado_contrasena_empleado_nombre_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='contrasena',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='nombre_usuario',
        ),
    ]
