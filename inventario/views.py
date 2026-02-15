"""
Módulo de vistas para la gestión de inventario.
Incluye endpoints para productos, categorías, dashboard y reportes analíticos.
"""
from datetime import timedelta
import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Producto, Categoria, MovimientoStock
from .serializers import (
    ProductoSerializer, CategoriaSerializer, MovimientoStockSerializer
)

# pylint: disable=no-member


class ProductViewSet(viewsets.ModelViewSet):
    """
    Vista para listar, crear, actualizar y eliminar productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar categorías de productos.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class DashboardStatsView(APIView):
    """
    Vista para obtener estadísticas generales del dashboard.
    """

    def get(self, _request):
        """
        Retorna KPIs principales: valor inventario, stock crítico, etc.
        """
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
    """
    Vista para generar reportes analíticos usando Pandas.
    """

    def list(self, _request):
        """
        Genera un reporte completo con análisis de rotación y stock.
        """
        try:
            qs_productos = Producto.objects.all().values(
                'id', 'sku', 'categoria__nombre', 'precio', 'stock', 'nombre')
            df_prod = pd.DataFrame(list(qs_productos))

            if df_prod.empty:  # Validación de seguridad
                return Response({"mensaje": "No hay suficientes datos para analizar"})

            df_prod['precio'] = df_prod['precio'].astype(float)
            df_prod['stock'] = df_prod['stock'].astype(int)
            df_prod['valor_total'] = df_prod['precio'] * df_prod['stock']

            hace_30_dias = timezone.now() - timedelta(days=30)
            qs_movimientos = MovimientoStock.objects.filter(
                fecha__gte=hace_30_dias).values('producto_id', 'tipo', 'cantidad')
            df_mov = pd.DataFrame(list(qs_movimientos))

            if not df_mov.empty:
                df_mov['cantidad'] = df_mov['cantidad'].astype(int)

                df_salidas = df_mov[df_mov['tipo'] == 'SALIDA'].copy()

                ventas_por_producto = df_salidas.groupby(
                    'producto_id')['cantidad'].sum().reset_index()
                ventas_por_producto.rename(
                    columns={'cantidad': 'unidades_vendidas'}, inplace=True)

                df_analisis = pd.merge(
                    df_prod, ventas_por_producto, left_on='id', right_on='producto_id', how='left')
                # Rellenar con 0 los que no tienen ventas
                df_analisis['unidades_vendidas'] = df_analisis['unidades_vendidas'].fillna(
                    0)
            else:

                df_prod['unidades_vendidas'] = 0
                df_analisis = df_prod.copy()

            df_inmovilizado = df_analisis[(df_analisis['stock'] > 0) & (
                df_analisis['unidades_vendidas'] == 0)]
            valor_inmovilizado = df_inmovilizado['valor_total'].sum()
            items_inmovilizados = len(df_inmovilizado)

            total_vendido = df_analisis['unidades_vendidas'].sum()
            stock_actual_global = df_analisis['stock'].sum()

            tasa_rotacion = round(
                total_vendido / stock_actual_global, 2) if stock_actual_global > 0 else 0

            top_vendidos = df_analisis.sort_values(
                by='unidades_vendidas', ascending=False).head(5)
            lista_top_vendidos = top_vendidos[[
                'nombre', 'unidades_vendidas']].to_dict(orient='records')

            analisis_categoria = df_analisis.groupby('categoria__nombre')[
                ['valor_total', 'stock']].sum().reset_index()

            prod_mas_caro = "N/A"
            if not df_analisis.empty:
                prod_mas_caro = df_analisis.loc[df_analisis['precio'].idxmax(
                )]['nombre']

            estadisticas = {
                "precio_promedio": round(df_analisis['precio'].mean(), 2),
                "precio_maximo": df_analisis['precio'].max(),
                "stock_total": int(df_analisis['stock'].sum()),
                "valor_inventario_total": int(df_analisis['valor_total'].sum()),
                "producto_mas_caro": prod_mas_caro,

                "tasa_rotacion_30d": float(tasa_rotacion),
                "capital_inmovilizado": int(valor_inmovilizado),
                "items_inmovilizados": int(items_inmovilizados),
                "top_vendidos_30d": lista_top_vendidos
            }

            return Response({
                "motor_analitico": "Pandas Data Science Engine 🐼",
                "resumen_general": estadisticas,
                "valor_por_categoria": analisis_categoria.to_dict(orient='records')
            })

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error en Pandas: {str(e)}")
            return Response({"error": str(e)}, status=500)


class MovimientoStockViewSet(viewsets.ModelViewSet):
    """
    Vista para listar y crear movimientos de stock (entradas/salidas).
    """
    queryset = MovimientoStock.objects.all().order_by('-fecha')
    serializer_class = MovimientoStockSerializer

    def get_queryset(self):
        """
        Permite filtrar movimientos por producto_id.
        """
        queryset = super().get_queryset()
        producto_id = self.request.query_params.get('producto_id')
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        return queryset


class CrearUsuarioView(APIView):
    """
    Vista pública para registrar nuevos usuarios.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Crea un usuario si no existe.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Faltan datos'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'El usuario ya existe'}, status=400)

        User.objects.create_user(username=username, password=password)
        return Response({'mensaje': 'Usuario creado con éxito'}, status=201)
