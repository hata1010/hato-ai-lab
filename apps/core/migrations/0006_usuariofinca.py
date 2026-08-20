# Generated for Hato Multi-Finca V1

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_finca_options_alter_potrero_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioFinca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('propietario', 'Propietario'), ('administrador', 'Administrador'), ('operador', 'Operador'), ('veterinario', 'Veterinario'), ('auditor', 'Auditor')], default='operador', max_length=30, verbose_name='Rol en la finca')),
                ('activa', models.BooleanField(default=True, help_text='Permite revocar el acceso a una finca sin borrar el historial.', verbose_name='Membresía activa')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('finca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_autorizados', to='core.finca', verbose_name='Finca')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membresias_finca', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Membresía de Finca',
                'verbose_name_plural': 'Membresías de Fincas',
                'ordering': ['finca', 'usuario'],
            },
        ),
        migrations.AddIndex(
            model_name='usuariofinca',
            index=models.Index(fields=['usuario', 'activa'], name='core_uf_user_act_idx'),
        ),
        migrations.AddIndex(
            model_name='usuariofinca',
            index=models.Index(fields=['finca', 'activa'], name='core_uf_finca_act_idx'),
        ),
        migrations.AddConstraint(
            model_name='usuariofinca',
            constraint=models.UniqueConstraint(fields=('usuario', 'finca'), name='usuario_finca_unico'),
        ),
    ]