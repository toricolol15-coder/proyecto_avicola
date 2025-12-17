from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models

class Insumo(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    unidad = models.CharField(max_length=20, default='kg')
    stock_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    porcentaje_ocupado_bodega = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad})"


class LoteGallinas(models.Model):
    TIPO_ALIMENTO_CHOICES = [
        ('INICIO', 'Inicio'),
        ('ENGORDE', 'Engorde'),
        ('POSTURA', 'Postura'),
    ]

    nombre_lote = models.CharField(max_length=60)
    cantidad_gallinas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    edad_semanas = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    tipo_alimento = models.CharField(max_length=10, choices=TIPO_ALIMENTO_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_lote} - {self.cantidad_gallinas} gallinas"


class Racion(models.Model):
    lote = models.ForeignKey(
        LoteGallinas,
        on_delete=models.CASCADE,
        related_name='raciones'
    )
    fecha_calculo = models.DateField(default=timezone.now)
    cantidad_total_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    porcentaje_algas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    porcentaje_carbonato = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    observaciones = models.CharField(max_length=255, blank=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-fecha_calculo']

    def __str__(self):
        return f"Ración {self.id} - {self.lote} - {self.fecha_calculo}"


class ProyeccionConsumo(models.Model):
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='proyecciones'
    )
    dias_a_proyectar = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    consumo_diario_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_proyectado_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    creado_en = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    comentario = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"Proyección {self.id} - {self.insumo.nombre}"


class AlertaStock(models.Model):
    NIVEL_CHOICES = [
        ('CRITICO', 'Crítico'),
        ('BAJO', 'Bajo'),
        ('INFO', 'Informativo'),
    ]

    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='alertas'
    )
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    mensaje = models.CharField(max_length=255)
    dias_restantes = models.IntegerField(null=True, blank=True)
    porcentaje_restante = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-creada_en']

    def __str__(self):
        return f"[{self.nivel}] {self.insumo.nombre} - {self.mensaje}"


class ConfiguracionUsuario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='configuracion_avicola'
    )
    alertas_stock = models.BooleanField(default=True)
    notificar_proyecciones = models.BooleanField(default=True)
    modo_oscuro_automatico = models.BooleanField(default=False)
    permitir_descargas = models.BooleanField(default=True)

    def __str__(self):
        return f"Configuración de {self.user.username}"


class RegistroUsuario(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_acceso'
    )
    correo = models.EmailField()
    creado_en = models.DateTimeField(default=timezone.now)
    origen = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.usuario.username} - {self.correo}"


# ------------------------------
#   🔥 TU TABLA DE REGISTROS
# ------------------------------
class RegistroRacion(models.Model):
    tipo_animal = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    granos = models.DecimalField(max_digits=6, decimal_places=2)
    algas = models.DecimalField(max_digits=6, decimal_places=2)
    dias = models.CharField(max_length=60)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_animal} - {self.peso}kg"


class ProduccionHuevos(models.Model):
    TIPO_HUEVO_CHOICES = [
        ('PEQUEÑO', 'Pequeño'),
        ('MEDIANO', 'Mediano'),
        ('GRANDE', 'Grande'),
        ('EXTRA_GRANDE', 'Extra Grande'),
    ]

    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    tipo_huevo = models.CharField(max_length=15, choices=TIPO_HUEVO_CHOICES, default='MEDIANO')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} huevos {self.tipo_huevo} ({self.fecha})"


class ProyeccionRacion(models.Model):
    racion_base = models.ForeignKey(
        RegistroRacion,
        on_delete=models.CASCADE,
        related_name='proyecciones'
    )
    cantidad_animales = models.PositiveIntegerField()
    periodo_dias = models.PositiveIntegerField()
    unidad_racion = models.CharField(max_length=2, choices=[('g', 'Gramos'), ('kg', 'Kilogramos')])
    
    # Cantidades calculadas (máximas)
    total_granos_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_algas_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_carbonato_kg = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Cantidades con ahorro del 15%
    total_granos_ahorro_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_algas_ahorro_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_carbonato_ahorro_kg = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Ahorro total en kg
    ahorro_granos_kg = models.DecimalField(max_digits=10, decimal_places=2)
    ahorro_algas_kg = models.DecimalField(max_digits=10, decimal_places=2)
    ahorro_carbonato_kg = models.DecimalField(max_digits=10, decimal_places=2)
    ahorro_total_kg = models.DecimalField(max_digits=10, decimal_places=2)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"Proyección {self.id} - {self.racion_base.tipo_animal} ({self.periodo_dias} días)"


