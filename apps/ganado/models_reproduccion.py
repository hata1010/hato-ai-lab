from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from django.db.models import Q

from apps.core.models import Finca


class EventoReproductivo(models.Model):
    TIPO_EVENTO_CHOICES = [
        ("servicio_monta", "Servicio / Monta natural"),
        ("inseminacion_ia", "Inseminación artificial"),
        ("diagnostico_gestacion", "Diagnóstico de gestación"),
        ("parto", "Parto"),
        ("aborto_perdida", "Aborto / Pérdida"),
        ("destete", "Destete"),
    ]

    METODO_REPRODUCTIVO_CHOICES = [
        ("monta_natural", "Monta natural"),
        ("ia", "Inseminación artificial"),
        ("iatf", "IATF"),
    ]

    RESULTADO_GESTACION_CHOICES = [
        ("prenada", "Preñada"),
        ("vacia", "Vacía"),
        ("dudosa", "Dudosa"),
    ]

    TIPO_PARTO_CHOICES = [
        ("normal", "Normal"),
        ("distocico", "Distócico"),
        ("cesarea", "Cesárea"),
    ]

    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="eventos_reproductivos",
        db_index=True,
    )

    animal = models.ForeignKey(
        "Animal",
        on_delete=models.PROTECT,
        related_name="eventos_reproductivos",
    )

    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPO_EVENTO_CHOICES,
    )

    fecha = models.DateTimeField(
        verbose_name="Fecha y hora",
    )

    metodo_reproductivo = models.CharField(
        max_length=20,
        choices=METODO_REPRODUCTIVO_CHOICES,
        null=True,
        blank=True,
    )

    toro = models.ForeignKey(
        "Animal",
        on_delete=models.PROTECT,
        related_name="eventos_reproductivos_como_toro",
        null=True,
        blank=True,
    )

    semen_codigo = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Código de semen / pajilla",
    )

    resultado_gestacion = models.CharField(
        max_length=20,
        choices=RESULTADO_GESTACION_CHOICES,
        null=True,
        blank=True,
    )

    tipo_parto = models.CharField(
        max_length=20,
        choices=TIPO_PARTO_CHOICES,
        null=True,
        blank=True,
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_reproductivos_creados",
    )

    observaciones = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Evento reproductivo"
        verbose_name_plural = "Eventos reproductivos"
        indexes = [
            models.Index(
                fields=["finca", "animal", "-fecha"],
                name="repro_finca_animal_fecha_idx",
            ),
            models.Index(
                fields=["finca", "tipo_evento", "-fecha"],
                name="repro_finca_tipo_fecha_idx",
            ),
        ]

    def clean(self):
        errores = {}

        if self.animal_id and self.animal.sexo != "H":
            errores["animal"] = "El animal reproductivo debe ser una hembra."

        if (
            self.animal_id
            and self.finca_id
            and self.animal.finca_id != self.finca_id
        ):
            errores["animal"] = "El animal debe pertenecer a la misma finca del evento."

        if self.toro_id:
            if self.toro_id == self.animal_id:
                errores["toro"] = "El toro no puede ser el mismo animal reproductivo."
            elif self.toro.sexo != "M":
                errores["toro"] = "El animal seleccionado como toro debe ser macho."
            if self.finca_id and self.toro.finca_id != self.finca_id:
                errores["toro"] = "El toro debe pertenecer a la misma finca."
            if self.animal_id and self.toro.especie_id != self.animal.especie_id:
                errores["toro"] = "El toro debe pertenecer a la misma especie."

        if self.tipo_evento in {"servicio_monta", "inseminacion_ia"}:
            if not self.metodo_reproductivo:
                errores["metodo_reproductivo"] = "Debe indicar el método reproductivo."

            if self.metodo_reproductivo == "monta_natural":
                if not self.toro_id:
                    errores["toro"] = "La monta natural requiere identificar el toro."
                if self.semen_codigo:
                    errores["semen_codigo"] = "La monta natural no debe registrar código de semen."

            if self.metodo_reproductivo in {"ia", "iatf"}:
                if not self.semen_codigo:
                    errores["semen_codigo"] = "La inseminación requiere código de semen o pajilla."

        elif self.metodo_reproductivo or self.semen_codigo:
            errores["metodo_reproductivo"] = "El método reproductivo solo aplica a servicios o inseminaciones."

        if self.tipo_evento == "diagnostico_gestacion" and not self.resultado_gestacion:
            errores["resultado_gestacion"] = "El diagnóstico requiere un resultado."
        elif self.tipo_evento != "diagnostico_gestacion" and self.resultado_gestacion:
            errores["resultado_gestacion"] = "El resultado de gestación solo aplica a diagnósticos."

        if self.tipo_evento == "parto" and not self.tipo_parto:
            errores["tipo_parto"] = "El parto requiere indicar su tipo."
        elif self.tipo_evento != "parto" and self.tipo_parto:
            errores["tipo_parto"] = "El tipo de parto solo aplica a eventos de parto."

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.animal} - {self.get_tipo_evento_display()} - {self.fecha:%Y-%m-%d %H:%M}"


class CriaNacimiento(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="crias_nacimiento",
        db_index=True,
    )

    parto = models.ForeignKey(
        EventoReproductivo,
        on_delete=models.PROTECT,
        related_name="crias",
    )

    animal = models.OneToOneField(
        "Animal",
        on_delete=models.PROTECT,
        related_name="nacimiento_reproductivo",
        null=True,
        blank=True,
    )

    observaciones = models.TextField(blank=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crias_nacimiento_creadas",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["parto", "id"]
        verbose_name = "Cría de nacimiento"
        verbose_name_plural = "Crías de nacimiento"
        indexes = [
            models.Index(
                fields=["finca", "parto"],
                name="cria_finca_parto_idx",
            )
        ]

    def clean(self):
        errores = {}

        if self.parto_id and self.parto.tipo_evento != "parto":
            errores["parto"] = "El evento de origen debe ser un parto."

        if self.parto_id and self.finca_id != self.parto.finca_id:
            errores["finca"] = "La cría y el parto deben pertenecer a la misma finca."

        if self.animal_id:
            if self.animal.finca_id != self.finca_id:
                errores["animal"] = "La cría debe pertenecer a la misma finca."
            if self.animal.madre_id and self.animal.madre_id != self.parto.animal_id:
                errores["animal"] = "La madre del animal no coincide con la hembra del parto."
            if self.animal.padre_id and self.parto.toro_id and self.animal.padre_id != self.parto.toro_id:
                errores["animal"] = "El padre del animal no coincide con el toro registrado en el parto."

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.parto} → {self.animal or 'Cría pendiente de registrar'}"


class Lactancia(models.Model):
    ESTADO_CHOICES = [
        ("en_produccion", "En producción"),
        ("secada", "Secada"),
    ]

    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="lactancias",
        db_index=True,
    )

    animal = models.ForeignKey(
        "Animal",
        on_delete=models.PROTECT,
        related_name="lactancias",
    )

    parto_origen = models.ForeignKey(
        EventoReproductivo,
        on_delete=models.PROTECT,
        related_name="lactancias_originadas",
        null=True,
        blank=True,
    )

    numero_lactancia = models.PositiveIntegerField()
    fecha_inicio = models.DateField(verbose_name="Inicio de lactancia")
    fecha_secado = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de secado",
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="en_produccion",
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lactancias_creadas",
    )

    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Lactancia"
        verbose_name_plural = "Lactancias"
        constraints = [
            models.UniqueConstraint(
                fields=["animal", "numero_lactancia"],
                name="lactancia_unica_por_animal",
            ),
            models.CheckConstraint(
                condition=Q(numero_lactancia__gte=1),
                name="lactancia_numero_positivo",
            ),
        ]
        indexes = [
            models.Index(
                fields=["finca", "animal", "-fecha_inicio"],
                name="lact_finca_animal_inicio_idx",
            )
        ]

    def clean(self):
        errores = {}

        if self.animal_id and self.animal.sexo != "H":
            errores["animal"] = "La lactancia debe pertenecer a una hembra."

        if self.animal_id and self.finca_id and self.animal.finca_id != self.finca_id:
            errores["animal"] = "El animal debe pertenecer a la misma finca de la lactancia."

        if self.fecha_secado and self.fecha_secado < self.fecha_inicio:
            errores["fecha_secado"] = "La fecha de secado no puede ser anterior al inicio."

        if self.estado == "secada" and not self.fecha_secado:
            errores["fecha_secado"] = "Una lactancia secada debe tener fecha de secado."

        if self.parto_origen_id:
            if self.parto_origen.tipo_evento != "parto":
                errores["parto_origen"] = "El origen de la lactancia debe ser un parto."
            if self.parto_origen.finca_id != self.finca_id:
                errores["parto_origen"] = "El parto de origen debe pertenecer a la misma finca."
            if self.parto_origen.animal_id != self.animal_id:
                errores["parto_origen"] = "El parto de origen debe corresponder a la misma hembra."
            if self.parto_origen.fecha.date() != self.fecha_inicio:
                errores["fecha_inicio"] = "El inicio de lactancia debe coincidir con la fecha del parto de origen."

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.animal} - Lactancia {self.numero_lactancia}"


class ControlLeche(models.Model):
    JORNADA_CHOICES = [
        ("manana", "Mañana"),
        ("tarde", "Tarde"),
        ("unico", "Único"),
    ]

    UNIDAD_CHOICES = [
        ("kg", "Kilogramos (kg)"),
        ("l", "Litros (L)"),
    ]

    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="controles_leche",
        db_index=True,
    )

    lactancia = models.ForeignKey(
        Lactancia,
        on_delete=models.PROTECT,
        related_name="controles_leche",
    )

    fecha = models.DateTimeField(verbose_name="Fecha y hora")
    jornada = models.CharField(max_length=10, choices=JORNADA_CHOICES)
    cantidad = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name="Cantidad",
    )
    unidad = models.CharField(max_length=2, choices=UNIDAD_CHOICES)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controles_leche_creados",
    )

    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Control lechero"
        verbose_name_plural = "Controles lecheros"
        constraints = [
            models.UniqueConstraint(
                fields=["lactancia", "fecha", "jornada"],
                name="control_leche_unico_por_jornada",
            ),
            models.CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="control_leche_cantidad_positiva",
            ),
        ]
        indexes = [
            models.Index(
                fields=["finca", "lactancia", "-fecha"],
                name="leche_finca_lact_fecha_idx",
            )
        ]

    def clean(self):
        errores = {}

        if self.lactancia_id and self.finca_id != self.lactancia.finca_id:
            errores["finca"] = "El control debe pertenecer a la misma finca de la lactancia."

        if self.cantidad is not None and self.cantidad <= 0:
            errores["cantidad"] = "La cantidad de leche debe ser mayor que cero."

        if self.lactancia_id:
            fecha = self.fecha.date()
            if fecha < self.lactancia.fecha_inicio:
                errores["fecha"] = "El control no puede ser anterior al inicio de la lactancia."
            if self.lactancia.fecha_secado and fecha > self.lactancia.fecha_secado:
                errores["fecha"] = "El control no puede ser posterior al secado."

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.lactancia} - {self.fecha:%Y-%m-%d %H:%M} - {self.cantidad} {self.unidad}"
