from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import DetalleVenta


@receiver(post_save, sender=DetalleVenta)
def al_guardar_detalle(sender, instance, created, **kwargs):
    venta = instance.venta

    if created and instance.producto:
        instance.producto.stock -= instance.cantidad
        instance.producto.save()

    nuevo_total = venta.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    venta.total = nuevo_total
    venta.save()


@receiver(post_delete, sender=DetalleVenta)
def al_borrar_detalle(sender, instance, **kwargs):
    venta = instance.venta
    nuevo_total = venta.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    venta.total = nuevo_total
    venta.save()
