from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(max_length=20, unique=True,
                           verbose_name="Código SKU")
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha Creación")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return f"{self.sku} - {self.nombre}"


class MovimientoStock(models.Model):
    TIPOS = (
        ('ENTRADA', 'Entrada (Compra/Devolución)'),
        ('SALIDA', 'Salida (Venta/Merma)'),
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.PositiveIntegerField()
    # Ej: "Factura 123", "Venta mostrador"
    motivo = models.CharField(max_length=200, blank=True)
    # Quién hizo el movimiento
    usuario = models.CharField(max_length=100, default='Sistema')
    fecha = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.pk:
            if self.tipo == 'ENTRADA':
                self.producto.stock += self.cantidad
            elif self.tipo == 'SALIDA':
                self.producto.stock -= self.cantidad

            self.producto.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} de {self.cantidad} - {self.producto.nombre}"
