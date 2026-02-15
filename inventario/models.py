"""
Módulo que define los modelos de datos para el sistema de inventario.
Incluye modelos para Categoría, Producto y MovimientoStock.
"""
from __future__ import annotations

from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """
    Modelo para agrupar productos bajo una categoría específica.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.nombre)


class Producto(models.Model):
    """
    Modelo que representa un artículo o producto en el inventario.
    """
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
    """
    Modelo para registrar el historial de movimientos (entradas/salidas) de stock.
    """
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
            producto = self.producto
            if self.tipo == 'ENTRADA':
                producto.stock += self.cantidad  # pylint: disable=no-member
            elif self.tipo == 'SALIDA':
                producto.stock -= self.cantidad  # pylint: disable=no-member

            producto.save()  # pylint: disable=no-member

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        producto = self.producto
        return f"{self.tipo} de {self.cantidad} - {producto.nombre}"  # pylint: disable=no-member
