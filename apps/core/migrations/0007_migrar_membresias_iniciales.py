# Generated for Hato Multi-Finca V1 Data Migration

from django.db import migrations


def crear_membresias_iniciales(apps, schema_editor):
    Finca = apps.get_model('core', 'Finca')
    UsuarioFinca = apps.get_model('core', 'UsuarioFinca')

    for finca in Finca.objects.all():
        if finca.created_by:
            UsuarioFinca.objects.get_or_create(
                usuario=finca.created_by,
                finca=finca,
                defaults={
                    'rol': 'propietario',
                    'activa': True,
                }
            )


def revertir_membresias(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_usuariofinca'),
    ]

    operations = [
        migrations.RunPython(crear_membresias_iniciales, revertir_membresias),
    ]