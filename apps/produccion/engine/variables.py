from apps.ganado.models import PesajeAnimal

class ErrorVariableMetrica(Exception):
    pass

def resolver_variable(variable, animal, fecha_inicio=None, fecha_fin=None):
    if not variable.activa:
        raise ErrorVariableMetrica(
            f"La variable {variable.codigo} está inactiva."
        )

    if variable.fuente != "PesajeAnimal":
        raise ErrorVariableMetrica(
            f"Fuente no soportada todavía: {variable.fuente}"
        )

    qs = PesajeAnimal.objects.filter(
        animal=animal
    ).order_by("fecha")

    if fecha_inicio:
        qs = qs.filter(fecha__gte=fecha_inicio)

    if fecha_fin:
        qs = qs.filter(fecha__lte=fecha_fin)

    if not qs.exists():
        raise ErrorVariableMetrica(
            f"No existen datos para la variable {variable.codigo}."
        )

    if not variable.campo:
        raise ErrorVariableMetrica(
            f"La variable {variable.codigo} no tiene campo definido."
        )

    if variable.regla == "primero":
        registro = qs.first()
        return getattr(registro, variable.campo)

    if variable.regla == "ultimo":
        registro = qs.last()
        return getattr(registro, variable.campo)

    if variable.regla == "promedio":
        valores = [
            getattr(registro, variable.campo)
            for registro in qs
        ]
        return sum(valores) / len(valores)

    if variable.regla == "minimo":
        valores = [
            getattr(registro, variable.campo)
            for registro in qs
        ]
        return min(valores)

    if variable.regla == "maximo":
        valores = [
            getattr(registro, variable.campo)
            for registro in qs
        ]
        return max(valores)

    if variable.regla == "suma":
        valores = [
            getattr(registro, variable.campo)
            for registro in qs
        ]
        return sum(valores)

    if variable.regla == "diferencia_fechas":
        primera = qs.first()
        ultima = qs.last()

        fecha_inicial = primera.fecha.date()
        fecha_final = ultima.fecha.date()

        diferencia = fecha_final - fecha_inicial

        return diferencia.days

    if variable.regla == "directo":
        registro = qs.last()
        return getattr(registro, variable.campo)

    raise ErrorVariableMetrica(
        f"Regla no soportada: {variable.regla}"
    )
