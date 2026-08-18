# apps/ganado/models.py

from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from django.db.models import Q

from apps.core.models import Finca, Potrero


# ============================================================
# CATÁLOGOS GLOBALES
# ============================================================

class Especie(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Especie"
        verbose_name_plural = "Especies"

    def __str__(self):
        return self.nombre


class Raza(models.Model):

    nombre = models.CharField(
        max_length=100,
    )

    especie = models.ForeignKey(
        Especie,
        on_delete=models.PROTECT,
        related_name="razas",
    )

    descripcion = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["especie", "nombre"]
        verbose_name = "Raza"
        verbose_name_plural = "Razas"

        constraints = [
            models.UniqueConstraint(
                fields=["especie", "nombre"],
                name="raza_unica_por_especie",
            )
        ]

    def __str__(self):
        return f"{self.especie.nombre} - {self.nombre}"


class TipoPasto(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Tipo de Pasto"
        verbose_name_plural = "Tipos de Pasto"

    def __str__(self):
        return self.nombre


# ============================================================
# ANIMAL
# ============================================================

class Animal(models.Model):

    SEXO_CHOICES = [
        ("M", "Macho"),
        ("H", "Hembra"),
    ]

    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("vendido", "Vendido"),
        ("muerto", "Muerto"),
        ("descartado", "Descartado"),
        ("trasladado", "Trasladado"),
    ]

    numero_arete = models.CharField(
        max_length=50,
        verbose_name="Número de arete",
    )

    nombre_propio = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre",
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
    )

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
    )

    especie = models.ForeignKey(
        Especie,
        on_delete=models.PROTECT,
        related_name="animales",
    )

    raza_declarada = models.ForeignKey(
        Raza,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="animales_declarados",
        verbose_name="Raza declarada",
    )

    categoria = models.CharField(
        max_length=100,
        blank=True,
    )

    # --------------------------------------------------------
    # PERTENENCIA EMPRESARIAL / FINCA
    # --------------------------------------------------------

    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="animales",
        null=True,
        blank=True,
    )

    # --------------------------------------------------------
    # IDENTIFICACIÓN
    # --------------------------------------------------------

    microchip = models.CharField(
        max_length=100,
        blank=True,
    )

    tatuaje = models.CharField(
        max_length=100,
        blank=True,
    )

    registro_genealogico = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Registro genealógico",
    )

    # --------------------------------------------------------
    # GENEALOGÍA
    # --------------------------------------------------------

    padre = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="descendencia_paterna",
    )

    madre = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="descendencia_materna",
    )

    # --------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="activo",
    )

    observaciones = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    # --------------------------------------------------------
    # AUDITORÍA
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["numero_arete"]

        verbose_name = "Animal"
        verbose_name_plural = "Animales"

        constraints = [
            models.UniqueConstraint(
                fields=["numero_arete", "finca"],
                name="arete_unico_por_finca",
            )
        ]

    def clean(self):

        errores = {}

        # ----------------------------------------------------
        # RAZA / ESPECIE
        # ----------------------------------------------------

        if self.raza_declarada_id and self.especie_id:

            if self.raza_declarada.especie_id != self.especie_id:

                errores["raza_declarada"] = (
                    "La raza declarada debe pertenecer "
                    "a la especie seleccionada."
                )

        # ----------------------------------------------------
        # PADRE
        # ----------------------------------------------------

        if self.padre_id:

            if self.padre_id == self.pk:

                errores["padre"] = (
                    "Un animal no puede ser su propio padre."
                )

            elif self.padre.sexo != "M":

                errores["padre"] = (
                    "El animal seleccionado como padre "
                    "debe ser macho."
                )

            if (
                self.especie_id
                and self.padre.especie_id != self.especie_id
            ):

                errores["padre"] = (
                    "El padre debe pertenecer "
                    "a la misma especie."
                )

            # El padre debe pertenecer a la misma finca.
            if (
                self.finca_id
                and self.padre.finca_id != self.finca_id
            ):

                errores["padre"] = (
                    "El padre debe pertenecer "
                    "a la misma finca."
                )

        # ----------------------------------------------------
        # MADRE
        # ----------------------------------------------------

        if self.madre_id:

            if self.madre_id == self.pk:

                errores["madre"] = (
                    "Un animal no puede ser su propia madre."
                )

            elif self.madre.sexo != "H":

                errores["madre"] = (
                    "El animal seleccionado como madre "
                    "debe ser hembra."
                )

            if (
                self.especie_id
                and self.madre.especie_id != self.especie_id
            ):

                errores["madre"] = (
                    "La madre debe pertenecer "
                    "a la misma especie."
                )

            # La madre debe pertenecer a la misma finca.
            if (
                self.finca_id
                and self.madre.finca_id != self.finca_id
            ):

                errores["madre"] = (
                    "La madre debe pertenecer "
                    "a la misma finca."
                )

        # ----------------------------------------------------
        # PADRE / MADRE
        # ----------------------------------------------------

        if (
            self.padre_id
            and self.madre_id
            and self.padre_id == self.madre_id
        ):

            errores["madre"] = (
                "El padre y la madre no pueden "
                "ser el mismo animal."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):

        if self.nombre_propio:

            return (
                f"{self.numero_arete} - "
                f"{self.nombre_propio}"
            )

        return self.numero_arete


# ============================================================
# PROCEDENCIA
# ============================================================

class ProcedenciaAnimal(models.Model):

    TIPO_CHOICES = [
        ("nacimiento_granja", "Nacimiento en la granja"),
        ("compra", "Compra"),
        ("donacion", "Donación"),
        ("traslado", "Traslado"),
        ("intercambio", "Intercambio"),
        ("otro", "Otro"),
    ]

    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name="procedencia",
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
    )

    fecha = models.DateField(
        null=True,
        blank=True,
    )

    origen_nombre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Origen",
    )

    origen_identificacion = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Identificación del origen",
    )

    observaciones = models.TextField(
        blank=True,
    )

    def __str__(self):

        return (
            f"{self.animal} - "
            f"{self.get_tipo_display()}"
        )


# ============================================================
# ADQUISICIÓN
# ============================================================

class Adquisicion(models.Model):

    finca = models.ForeignKey(
        Finca,
        on_delete=models.PROTECT,
        related_name="adquisiciones",
    )

    proveedor = models.CharField(
        max_length=200,
    )

    fecha = models.DateField()

    numero_documento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Factura / Documento",
    )

    costo_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    def __str__(self):

        return (
            f"{self.numero_documento or 'Adquisición'} "
            f"- {self.proveedor}"
        )


class AdquisicionAnimal(models.Model):

    adquisicion = models.ForeignKey(
        Adquisicion,
        on_delete=models.CASCADE,
        related_name="animales",
    )

    animal = models.OneToOneField(
        Animal,
        on_delete=models.PROTECT,
        related_name="adquisicion",
    )

    precio_individual = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    def clean(self):

        errores = {}

        if (
            self.adquisicion_id
            and self.animal_id
            and self.adquisicion.finca_id
            != self.animal.finca_id
        ):

            errores["animal"] = (
                "El animal debe pertenecer "
                "a la misma finca de la adquisición."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):

        return (
            f"{self.adquisicion} → "
            f"{self.animal}"
        )


# ============================================================
# COMPOSICIÓN GENÉTICA
# ============================================================

class ComposicionGenetica(models.Model):

    METODO_CHOICES = [
        ("pedigree", "Pedigree"),
        ("registro", "Registro oficial"),
        ("adn", "ADN"),
        ("declaracion", "Declaración"),
        ("estimacion", "Estimación"),
    ]

    CONFIABILIDAD_CHOICES = [
        ("confirmada", "Confirmada"),
        ("alta", "Alta"),
        ("media", "Media"),
        ("baja", "Baja"),
        ("desconocida", "Desconocida"),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="composiciones_geneticas",
    )

    raza = models.ForeignKey(
        Raza,
        on_delete=models.PROTECT,
        related_name="composiciones",
    )

    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    metodo = models.CharField(
        max_length=30,
        choices=METODO_CHOICES,
    )

    confiabilidad = models.CharField(
        max_length=20,
        choices=CONFIABILIDAD_CHOICES,
    )

    fecha_verificacion = models.DateField(
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = [
            "animal",
            "-porcentaje",
        ]

        verbose_name = "Composición genética"
        verbose_name_plural = "Composiciones genéticas"

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(porcentaje__gte=0)
                    & Q(porcentaje__lte=100)
                ),
                name="composicion_genetica_0_100",
            )
        ]

    def clean(self):

        errores = {}

        if (
            self.porcentaje is not None
            and (
                self.porcentaje < 0
                or self.porcentaje > 100
            )
        ):

            errores["porcentaje"] = (
                "El porcentaje debe estar "
                "entre 0 y 100."
            )

        if (
            self.animal_id
            and self.raza_id
            and self.raza.especie_id
            != self.animal.especie_id
        ):

            errores["raza"] = (
                "La raza debe pertenecer "
                "a la misma especie del animal."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):

        return (
            f"{self.animal} - "
            f"{self.raza.nombre}: "
            f"{self.porcentaje}%"
        )


# ============================================================
# DOCUMENTOS
# ============================================================

class DocumentoAnimal(models.Model):

    TIPO_CHOICES = [
        ("factura", "Factura"),
        ("pedigree", "Pedigree"),
        ("registro_genealogico", "Registro genealógico"),
        ("adn", "ADN / Genotipo"),
        ("sanitario", "Certificado sanitario"),
        ("transporte", "Documento de transporte"),
        ("otro", "Otro"),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="documentos",
    )

    tipo = models.CharField(
        max_length=40,
        choices=TIPO_CHOICES,
    )

    numero_documento = models.CharField(
        max_length=150,
        blank=True,
    )

    archivo = models.FileField(
        upload_to="animales/documentos/",
        blank=True,
        null=True,
    )

    fecha_documento = models.DateField(
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    def __str__(self):

        return (
            f"{self.animal} - "
            f"{self.get_tipo_display()}"
        )


# ============================================================
# MOVIMIENTO
# ============================================================

class MovimientoAnimal(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="movimientos",
    )

    potrero = models.ForeignKey(
        Potrero,
        on_delete=models.PROTECT,
        related_name="movimientos_animales",
    )

    fecha_entrada = models.DateTimeField()

    fecha_salida = models.DateTimeField(
        null=True,
        blank=True,
    )

    activo = models.BooleanField(
        default=True,
    )

    tipo_pasto = models.ForeignKey(
        TipoPasto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = ["-fecha_entrada"]

        verbose_name = "Movimiento de Animal"
        verbose_name_plural = "Movimientos de Animales"

        constraints = [
            models.UniqueConstraint(
                fields=["animal"],
                condition=Q(activo=True),
                name="un_movimiento_activo_por_animal",
            )
        ]

    def clean(self):

        errores = {}

        # ----------------------------------------------------
        # FECHAS
        # ----------------------------------------------------

        if (
            self.fecha_entrada
            and self.fecha_salida
            and self.fecha_salida < self.fecha_entrada
        ):

            errores["fecha_salida"] = (
                "La fecha de salida no puede "
                "ser anterior a la entrada."
            )

        # ----------------------------------------------------
        # ESTADO DEL MOVIMIENTO
        # ----------------------------------------------------

        if self.activo and self.fecha_salida:

            errores["activo"] = (
                "Un movimiento activo no debe "
                "tener fecha de salida."
            )

        # ----------------------------------------------------
        # FINCA ANIMAL / POTRERO
        # ----------------------------------------------------

        if (
            self.animal_id
            and self.potrero_id
            and self.animal.finca_id
            != self.potrero.finca_id
        ):

            errores["potrero"] = (
                "El potrero debe pertenecer "
                "a la misma finca del animal."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):

        return (
            f"{self.animal} → "
            f"{self.potrero}"
        )


# ============================================================
# PESAJES
# ============================================================

class PesajeAnimal(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="pesajes",
    )

    fecha = models.DateTimeField(
        verbose_name="Fecha y hora",
    )

    peso_kg = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Peso (kg)",
    )

    observaciones = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = ["-fecha"]

        verbose_name = "Pesaje"
        verbose_name_plural = "Pesajes"

        indexes = [
            models.Index(
                fields=["animal", "-fecha"],
                name="pesaje_animal_fecha_idx",
            )
        ]

    def __str__(self):

        return (
            f"{self.animal} - "
            f"{self.fecha:%Y-%m-%d %H:%M} - "
            f"{self.peso_kg} kg"
        )


# ============================================================
# SALUD
# ============================================================

class EventoSalud(models.Model):

    TIPO_CHOICES = [
        ("vacunacion", "Vacunación"),
        ("desparasitacion", "Desparasitación"),
        ("enfermedad", "Enfermedad / Diagnóstico"),
        ("tratamiento", "Tratamiento"),
        ("lesion", "Lesión"),
        ("cirugia", "Cirugía"),
        ("examen", "Examen / Revisión"),
        ("consulta", "Consulta veterinaria"),
        ("otro", "Otro"),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="eventos_salud",
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
    )

    fecha = models.DateTimeField(
        verbose_name="Fecha y hora",
    )

    producto = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Producto / Medicamento",
    )

    dosis = models.CharField(
        max_length=50,
        blank=True,
    )

    nombre_veterinario = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Veterinario responsable",
    )

    observaciones = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = ["-fecha"]

        verbose_name = "Evento de Salud"
        verbose_name_plural = "Eventos de Salud"

        indexes = [
            models.Index(
                fields=["animal", "-fecha"],
                name="salud_animal_fecha_idx",
            )
        ]

    def __str__(self):

        return (
            f"{self.animal} - "
            f"{self.get_tipo_display()} "
            f"({self.fecha:%Y-%m-%d %H:%M})"
        )