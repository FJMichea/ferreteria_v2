from django.db import models

# Modelo para Categorías (Ej: Herramientas, Pinturas, Electricidad)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo para el Producto (El inventario real)
class Producto(models.Model):
    sku = models.CharField(max_length=20, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=150)
    # Relación ForeignKey: Un producto pertenece a una categoría
    # on_delete=models.PROTECT evita borrar una categoría si tiene productos asignados (Integridad Referencial)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    # Fechas automáticas (Auditoría básica)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return f"{self.sku} - {self.nombre}"