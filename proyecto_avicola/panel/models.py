from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Insumo(models.Model):
    """
    Insumos principales del sistema: algas, carbonato de calcio, etc.
    """
    nombre = models.CharField(max_length=60, unique=True)
    unidad = models.CharField(max_length=20, default='kg')
    stock_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cantidad disponible actualmente"
    )
    stock_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Umbral mínimo para generar alerta de stock"
    )
    porcentaje_ocupado_bodega = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="% de capacidad de bodega usado (opcional)"
    )

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad})"


class LoteGallinas(models.Model):
    """
    Lote o grupo de gallinas usado para los cálculos de ración.
    """
    TIPO_ALIMENTO_CHOICES = [
        ('INICIO', 'Inicio'),
        ('ENGORDE', 'Engorde'),
        ('POSTURA', 'Postura'),
    ]

    nombre_lote = models.CharField(max_length=60)
    cantidad_gallinas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de gallinas del lote"
    )
    edad_semanas = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Edad promedio del lote en semanas"
    )
    tipo_alimento = models.CharField(
        max_length=10,
        choices=TIPO_ALIMENTO_CHOICES
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_lote} - {self.cantidad_gallinas} gallinas"


class Racion(models.Model):
    """
    Resultado del cálculo de raciones diarias para un lote.
    Se puede relacionar con los insumos utilizados (algas, carbonato, etc.).
    """
    lote = models.ForeignKey(
        LoteGallinas,
        on_delete=models.CASCADE,
        related_name='raciones'
    )
    fecha_calculo = models.DateField(default=timezone.now)
    cantidad_total_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cantidad total de alimento (kg) para el lote"
    )
    porcentaje_algas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="% de algas en la mezcla"
    )
    porcentaje_carbonato = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="% de carbonato de calcio en la mezcla"
    )
    observaciones = models.CharField(max_length=255, blank=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='raciones_creadas'
    )

    class Meta:
        ordering = ['-fecha_calculo']

    def __str__(self):
        return f"Ración {self.id} - {self.lote} - {self.fecha_calculo}"


class ProyeccionConsumo(models.Model):
    """
    Proyección de consumo (vista Proyecciones):
    - Días a proyectar
    - Consumo diario estimado
    - Total proyectado
    """
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='proyecciones'
    )
    dias_a_proyectar = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad de días de la proyección"
    )
    consumo_diario_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Consumo diario estimado (kg)"
    )
    total_proyectado_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Consumo total proyectado (kg)"
    )
    creado_en = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyecciones_creadas'
    )
    comentario = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"Proyección {self.id} - {self.insumo.nombre} - {self.dias_a_proyectar} días"


class AlertaStock(models.Model):
    """
    Alertas que luego puedes mostrar en el Dashboard:
    - Ej: 'Alerta: Algas - stock crítico (2 días)'
    """
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
    dias_restantes = models.IntegerField(
        null=True,
        blank=True,
        help_text="Días estimados de stock restante (opcional)"
    )
    porcentaje_restante = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="% de stock restante (opcional)"
    )
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-creada_en']

    def __str__(self):
        return f"[{self.nivel}] {self.insumo.nombre} - {self.mensaje}"


class ConfiguracionUsuario(models.Model):
    """
    Configuraciones ligadas a la vista Configuraciones:
    - Alertas de stock
    - Notificar proyecciones
    - Modo oscuro automático
    - Permitir descargas
    """
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
    """
    Tabla simple para respaldar lo que se muestra en Registros:
    ID, Usuario, Correo, Acción (eliminar).
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_acceso'
    )
    correo = models.EmailField()
    creado_en = models.DateTimeField(default=timezone.now)
    origen = models.CharField(
        max_length=60,
        blank=True,
        help_text="Ej: 'creado manual', 'importado', etc."
    )

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.usuario.username} - {self.correo}"
