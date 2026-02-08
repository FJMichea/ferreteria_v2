from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import DetalleVenta

# Este decorador le dice a Django: "Ejecuta esto cada vez que se guarde un DetalleVenta"
@receiver(post_save, sender=DetalleVenta)
def al_guardar_detalle(sender, instance, created, **kwargs):
    venta = instance.venta
    
    # 1. LÓGICA DE STOCK (Inventario)
    # Solo si es un registro NUEVO, descontamos el stock.
    # (Si editamos una venta antigua, sería más complejo, por ahora simplificamos).
    if created and instance.producto:
        instance.producto.stock -= instance.cantidad
        instance.producto.save()

    # 2. LÓGICA FINANCIERA (Total de Venta)
    # Recalculamos el total de la cabecera sumando todos los hijos (detalles)
    nuevo_total = venta.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    venta.total = nuevo_total
    venta.save()

# Si borramos un detalle (ej: el cliente se arrepintió), actualizamos el total.
@receiver(post_delete, sender=DetalleVenta)
def al_borrar_detalle(sender, instance, **kwargs):
    venta = instance.venta
    nuevo_total = venta.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    venta.total = nuevo_total
    venta.save()