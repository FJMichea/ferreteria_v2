import pandas as pd
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class DashboardStatsView(APIView):
    def get(self, request):
        total_valor = Producto.objects.aggregate(
            total=Sum(F('precio') * F('stock'))
        )['total'] or 0
        
        stock_critico = Producto.objects.filter(stock__lte=5).count()
        total_items = Producto.objects.count()
       
        top_productos = Producto.objects.order_by('-stock')[:5]
        grafico_labels = [p.nombre for p in top_productos]
        grafico_data = [p.stock for p in top_productos]

        data = {
            "valor_inventario": total_valor,
            "stock_critico": stock_critico,
            "total_items": total_items,
            "total_mermas": 0, 
            "grafico": {
                "labels": grafico_labels,
                "data": grafico_data
            }
        }
        return Response(data)

class ReporteViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = Producto.objects.all().values('categoria__nombre', 'precio', 'stock', 'nombre')
            df = pd.DataFrame(list(queryset))

            if df.empty:
                return Response({"mensaje": "No hay suficientes datos para analizar"})

            df['precio'] = df['precio'].astype(float)
            df['stock'] = df['stock'].astype(int)

            df['valor_total'] = df['precio'] * df['stock']

            analisis_categoria = df.groupby('categoria__nombre')[['valor_total', 'stock']].sum().reset_index()
            
            estadisticas = {
                "precio_promedio": round(df['precio'].mean(), 2),
                "precio_maximo": df['precio'].max(),
                "stock_total": int(df['stock'].sum()),
                "valor_inventario_total": int(df['valor_total'].sum()),
                # Usamos iloc para evitar errores de índice
                "producto_mas_caro": df.loc[df['precio'].idxmax()]['nombre'] if not df.empty else "N/A"
            }

            data = {
                "reporte": "Generado con Pandas 🐼",
                "resumen_general": estadisticas,
                "valor_por_categoria": analisis_categoria.to_dict(orient='records')
            }

            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)