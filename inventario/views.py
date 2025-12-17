from rest_framework import viewsets
from rest_framework.views import APIView  # <--- Esto faltaba
from rest_framework.response import Response # <--- Esto faltaba
from django.db.models import Sum, Count, F # <--- Esto faltaba
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

# --- Vistas Antiguas (CRUD) ---

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# --- Nueva Vista (Dashboard) ---

class DashboardStatsView(APIView):
    def get(self, request):
        # 1. Calcular Valorización del Inventario (Precio * Stock)
        total_valor = Producto.objects.aggregate(
            total=Sum(F('precio') * F('stock'))
        )['total'] or 0

        # 2. Calcular Stock Crítico (ej: menos de 5 unidades)
        stock_critico = Producto.objects.filter(stock__lte=5).count()

        # 3. Total de Items
        total_items = Producto.objects.count()

        # 4. Datos para el Gráfico (Top 5 Stock)
        top_productos = Producto.objects.order_by('-stock')[:5]
        grafico_labels = [p.nombre for p in top_productos]
        grafico_data = [p.stock for p in top_productos]

        data = {
            "valor_inventario": total_valor,
            "stock_critico": stock_critico,
            "total_items": total_items,
            "total_mermas": 0, # Placeholder hasta que tengamos Mermas
            "grafico": {
                "labels": grafico_labels,
                "data": grafico_data
            }
        }
        return Response(data)