# apps/core/models.py

from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Finca(models.Model):
    """
    Hacienda / Fundo / Hato.

    Esta es la unidad empresarial principal.
    Todos los datos operativos deben pertenecer
    directa o indirectamente a una Finca.
    """

    nombre = models.CharField(max_length=200)

    nit = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )

    direccion = models.TextField(blank=True)

    telefono = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(blank=True)

    ubicacion = models.PointField(
        srid=4326,
        null=True,
        blank=True,
    )

    area_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fecha_fundacion = models.DateField(
        null=True,
        blank=True,
    )

    zona_horaria = models.CharField(
        max_length=50,
        default="America/Bogota",
    )

    moneda = models.CharField(
        max_length=3,
        default="COP",
    )

    is_active = models.BooleanField(
        default=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fincas_creadas",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Finca"
        verbose_name_plural = "Fincas"

    def __str__(self):
        return self.nombre


class Potrero(models.Model):
    """
    Espacio físico perteneciente exclusivamente a una Finca.
    """

    TIPO_CHOICES = [
        ("potrero", "Potrero"),
        ("corral", "Corral"),
        ("encierro", "Encierro"),
        ("embarcadero", "Embarcadero"),
        ("otro", "Otro"),
    ]

    ESTADO_CHOICES = [
        ("disponible", "Disponible"),
        ("ocupado", "Ocupado"),
        ("descanso", "En descanso"),
        ("mantenimiento", "Mantenimiento"),
    ]

    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="potreros",
    )

    nombre = models.CharField(
        max_length=100,
    )

    codigo = models.CharField(
        max_length=20,
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="potrero",
    )

    ubicacion = models.PointField(
        srid=4326,
        null=True,
        blank=True,
    )

    area_hectareas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    capacidad_animales = models.IntegerField(
        null=True,
        blank=True,
    )

    carga_actual = models.IntegerField(
        default=0,
    )

    tipo_pasto = models.CharField(
        max_length=100,
        blank=True,
    )

    calidad_pasto = models.CharField(
        max_length=20,
        choices=[
            ("excelente", "Excelente"),
            ("bueno", "Bueno"),
            ("regular", "Regular"),
            ("malo", "Malo"),
        ],
        default="bueno",
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="disponible",
    )

    dias_descanso = models.IntegerField(
        default=0,
    )

    fecha_ultimo_pastoreo = models.DateField(
        null=True,
        blank=True,
    )

    poligono = models.PolygonField(
        srid=4326,
        null=True,
        blank=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Potrero"
        verbose_name_plural = "Potreros"

        constraints = [
            models.UniqueConstraint(
                fields=["finca", "codigo"],
                name="potrero_codigo_unico_por_finca",
            )
        ]

    def save(self, *args, **kwargs):

        if self.poligono:
            area_m2 = (
                self.poligono
                .transform(3857, clone=True)
                .area
            )

            self.area_hectareas = round(
                area_m2 / 10000,
                2,
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.finca.nombre} - {self.nombre}"