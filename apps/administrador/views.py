from collections import OrderedDict
from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from apps.core.models import Potrero
from apps.core.tenant import obtener_finca_activa, obtener_fincas_usuario
from apps.ganado.models import Animal, ComposicionGenetica, PesajeAnimal
from apps.produccion.models import Metrica


def _latest_weight(animal):
    pesaje = animal.pesajes.order_by("-fecha").first()
    return pesaje.peso_kg if pesaje else None


def dashboard(request):
    """Panel Operativo V2 con datos reales y trazabilidad visible."""
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    total_animales = 0
    total_potreros = 0
    total_hectareas = Decimal("0")
    total_metricas = 0
    hembras_pct = Decimal("0")
    peso_promedio = None
    carga_ugg_ha = None
    animales_con_peso = 0
    potreros_operativos = []
    categorias = []
    genetica = []
    registros_14_meses = []
    actividad = []
    ubicacion_finca = None

    if finca:
        animales_qs = Animal.objects.filter(finca=finca, estado="activo")
        total_animales = animales_qs.count()

        hembras = animales_qs.filter(sexo="H").count()
        if total_animales:
            hembras_pct = (Decimal(hembras) * Decimal("100") / Decimal(total_animales)).quantize(Decimal("0.1"))

        pesos = []
        for animal in animales_qs.prefetch_related("pesajes"):
            peso = _latest_weight(animal)
            if peso is not None:
                pesos.append(Decimal(peso))

        animales_con_peso = len(pesos)
        peso_total = sum(pesos, Decimal("0"))
        if pesos:
            peso_promedio = (peso_total / Decimal(len(pesos))).quantize(Decimal("0.1"))

        potreros_qs = Potrero.objects.filter(finca=finca, is_active=True).order_by("nombre")
        total_potreros = potreros_qs.count()
        total_hectareas = potreros_qs.aggregate(total=Sum("area_hectareas"))["total"] or Decimal("0")

        if total_hectareas and peso_total:
            carga_ugg_ha = (peso_total / Decimal("450") / Decimal(total_hectareas)).quantize(Decimal("0.01"))

        total_metricas = Metrica.objects.filter(
            Q(finca=finca) | Q(finca__isnull=True),
            activa=True,
        ).count()

        for potrero in potreros_qs:
            capacidad = potrero.capacidad_animales
            carga = potrero.carga_actual or 0
            utilizacion = None
            if capacidad:
                utilizacion = (Decimal(carga) * Decimal("100") / Decimal(capacidad)).quantize(Decimal("0.1"))
            potreros_operativos.append({
                "nombre": potrero.nombre,
                "codigo": potrero.codigo,
                "estado": potrero.get_estado_display(),
                "estado_codigo": potrero.estado,
                "carga": carga,
                "capacidad": capacidad,
                "utilizacion": utilizacion,
                "pasto": potrero.tipo_pasto or "No especificado",
                "area": potrero.area_hectareas,
                "descanso": potrero.dias_descanso,
                "fecha_ultimo_pastoreo": potrero.fecha_ultimo_pastoreo,
                "tiene_poligono": bool(potrero.poligono),
            })

        categorias = [
            {"nombre": item["categoria"] or "Sin categoría", "total": item["total"]}
            for item in animales_qs.values("categoria").annotate(total=Count("id")).order_by("-total")
        ]

        genetica = [
            {"nombre": item["raza__nombre"], "total": item["total"]}
            for item in ComposicionGenetica.objects.filter(animal__finca=finca)
            .values("raza__nombre")
            .annotate(total=Sum("porcentaje"))
            .order_by("-total")[:8]
        ]

        now = timezone.now()
        start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=395)).replace(day=1)
        monthly = OrderedDict()
        cursor = start
        for _ in range(14):
            monthly[cursor.strftime("%Y-%m")] = {"label": cursor.strftime("%b %y"), "total": 0}
            if cursor.month == 12:
                cursor = cursor.replace(year=cursor.year + 1, month=1)
            else:
                cursor = cursor.replace(month=cursor.month + 1)

        for created_at in Animal.objects.filter(finca=finca, created_at__gte=start).values_list("created_at", flat=True):
            key = created_at.strftime("%Y-%m")
            if key in monthly:
                monthly[key]["total"] += 1
        registros_14_meses = list(monthly.values())

        actividad = [
            {
                "tipo": "Pesaje",
                "icono": "⚖️",
                "titulo": f"{pesaje.animal.numero_arete} · {pesaje.peso_kg} kg",
                "fecha": pesaje.fecha,
                "origen": "PesajeAnimal",
            }
            for pesaje in PesajeAnimal.objects.filter(animal__finca=finca)
            .select_related("animal")
            .order_by("-fecha")[:5]
        ]

        if finca.ubicacion:
            ubicacion_finca = {"lat": float(finca.ubicacion.y), "lon": float(finca.ubicacion.x)}

    contexto = {
        "titulo": "Panel Operativo V2 — Hato AI Lab",
        "finca": finca,
        "fincas_disponibles": fincas_usuario,
        "total_animales": total_animales,
        "total_potreros": total_potreros,
        "total_hectareas": total_hectareas,
        "total_metricas": total_metricas,
        "hembras_pct": hembras_pct,
        "peso_promedio": peso_promedio,
        "carga_ugg_ha": carga_ugg_ha,
        "animales_con_peso": animales_con_peso,
        "potreros_operativos": potreros_operativos,
        "categorias": categorias,
        "genetica": genetica,
        "registros_14_meses": registros_14_meses,
        "actividad": actividad,
        "ubicacion_finca": ubicacion_finca,
    }

    return render(request, "administrador/dashboard.html", contexto)


def indicadores(request):
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    contexto = {
        "finca": finca,
        "fincas_disponibles": fincas_usuario,
    }
    return render(request, "administrador/indicadores.html", contexto)
