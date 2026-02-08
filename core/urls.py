from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from inventario.views import (
    ProductViewSet, 
    CategoriaViewSet, 
    DashboardStatsView, 
    ReporteViewSet 
)

def root_redirect(request):
    return redirect('/api/')

router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'reporte-bi', ReporteViewSet, basename='reporte-bi')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]