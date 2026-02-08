from django.urls import path, include
from django.shortcuts import redirect 
from rest_framework.routers import DefaultRouter
from inventario.views import (
    ProductViewSet, 
    CategoriaViewSet, 
    DashboardStatsView, 
    ReporteAnaliticoView
)
def root_redirect(request):
    return redirect('/api/') 

router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = [
    path('', root_redirect, name='root'),
    path('api/', include(router.urls)),
    path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('api/reporte-bi/', ReporteAnaliticoView.as_view(), name='reporte_bi') 
]