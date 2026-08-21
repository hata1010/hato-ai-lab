# Generated manually from the approved reproduction/lactation design.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("ganado", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EventoReproductivo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo_evento", models.CharField(choices=[("servicio_monta", "Servicio / Monta natural"), ("inseminacion_ia", "Inseminación artificial"), ("diagnostico_gestacion", "Diagnóstico de gestación"), ("parto", "Parto"), ("aborto_perdida", "Aborto / Pérdida"), ("destete", "Destete")], max_length=30)),
                ("fecha", models.DateTimeField(verbose_name="Fecha y hora")),
                ("metodo_reproductivo", models.CharField(blank=True, choices=[("monta_natural", "Monta natural"), ("ia", "Inseminación artificial"), ("iatf", "IATF")], max_length=20, null=True)),
                ("semen_codigo", models.CharField(blank=True, max_length=150, verbose_name="Código de semen / pajilla")),
                ("resultado_gestacion", models.CharField(blank=True, choices=[("prenada", "Preñada"), ("vacia", "Vacía"), ("dudosa", "Dudosa")], max_length=20, null=True)),
                ("tipo_parto", models.CharField(blank=True, choices=[("normal", "Normal"), ("distocico", "Distócico"), ("cesarea", "Cesárea")], max_length=20, null=True)),
                ("observaciones", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("animal", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="eventos_reproductivos", to="ganado.animal")),
                ("creado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="eventos_reproductivos_creados", to=settings.AUTH_USER_MODEL)),
                ("finca", models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name="eventos_reproductivos", to="core.finca")),
                ("toro", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="eventos_reproductivos_como_toro", to="ganado.animal")),
            ],
            options={
                "verbose_name": "Evento reproductivo",
                "verbose_name_plural": "Eventos reproductivos",
                "ordering": ["-fecha"],
                "indexes": [
                    models.Index(fields=["finca", "animal", "-fecha"], name="repro_finca_animal_fecha_idx"),
                    models.Index(fields=["finca", "tipo_evento", "-fecha"], name="repro_finca_tipo_fecha_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="CriaNacimiento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("observaciones", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("animal", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="nacimiento_reproductivo", to="ganado.animal")),
                ("creado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="crias_nacimiento_creadas", to=settings.AUTH_USER_MODEL)),
                ("finca", models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name="crias_nacimiento", to="core.finca")),
                ("parto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="crias", to="ganado.eventoreproductivo")),
            ],
            options={
                "verbose_name": "Cría de nacimiento",
                "verbose_name_plural": "Crías de nacimiento",
                "ordering": ["parto", "id"],
                "indexes": [models.Index(fields=["finca", "parto"], name="cria_finca_parto_idx")],
            },
        ),
        migrations.CreateModel(
            name="Lactancia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_lactancia", models.PositiveIntegerField()),
                ("fecha_inicio", models.DateField(verbose_name="Inicio de lactancia")),
                ("fecha_secado", models.DateField(blank=True, null=True, verbose_name="Fecha de secado")),
                ("estado", models.CharField(choices=[("en_produccion", "En producción"), ("secada", "Secada")], default="en_produccion", max_length=20)),
                ("observaciones", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("animal", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lactancias", to="ganado.animal")),
                ("creado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="lactancias_creadas", to=settings.AUTH_USER_MODEL)),
                ("finca", models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name="lactancias", to="core.finca")),
                ("parto_origen", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="lactancias_originadas", to="ganado.eventoreproductivo")),
            ],
            options={
                "verbose_name": "Lactancia",
                "verbose_name_plural": "Lactancias",
                "ordering": ["-fecha_inicio"],
                "indexes": [models.Index(fields=["finca", "animal", "-fecha_inicio"], name="lact_finca_animal_inicio_idx")],
            },
        ),
        migrations.CreateModel(
            name="ControlLeche",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateTimeField(verbose_name="Fecha y hora")),
                ("jornada", models.CharField(choices=[("manana", "Mañana"), ("tarde", "Tarde"), ("unico", "Único")], max_length=10)),
                ("cantidad", models.DecimalField(decimal_places=3, max_digits=8, verbose_name="Cantidad")),
                ("unidad", models.CharField(choices=[("kg", "Kilogramos (kg)"), ("l", "Litros (L)")], max_length=2)),
                ("observaciones", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("creado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="controles_leche_creados", to=settings.AUTH_USER_MODEL)),
                ("finca", models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name="controles_leche", to="core.finca")),
                ("lactancia", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="controles_leche", to="ganado.lactancia")),
            ],
            options={
                "verbose_name": "Control lechero",
                "verbose_name_plural": "Controles lecheros",
                "ordering": ["-fecha"],
                "indexes": [models.Index(fields=["finca", "lactancia", "-fecha"], name="leche_finca_lact_fecha_idx")],
            },
        ),
        migrations.AddConstraint(
            model_name="lactancia",
            constraint=models.UniqueConstraint(fields=("animal", "numero_lactancia"), name="lactancia_unica_por_animal"),
        ),
        migrations.AddConstraint(
            model_name="lactancia",
            constraint=models.CheckConstraint(condition=Q(numero_lactancia__gte=1), name="lactancia_numero_positivo"),
        ),
        migrations.AddConstraint(
            model_name="controlleche",
            constraint=models.UniqueConstraint(fields=("lactancia", "fecha", "jornada"), name="control_leche_unico_por_jornada"),
        ),
        migrations.AddConstraint(
            model_name="controlleche",
            constraint=models.CheckConstraint(condition=Q(cantidad__gt=0), name="control_leche_cantidad_positiva"),
        ),
    ]
