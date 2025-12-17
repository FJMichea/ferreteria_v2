from django.urls import path, include
from inventario.views import ProductViewSet, CategoriaViewSet, DashboardStatsView # <--- Importar esto
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Nueva ruta para el dashboard:
    path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'), 
]