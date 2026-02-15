from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from inventario.views.MovimientoStockViewSet import MovimientoStockViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView:
    TokenRefreshView:
)
from inventario.views import (
    ProductViewSet,
    CategoriaViewSet,
    DashboardStatsView,
    ReporteViewSet,
    CrearUsuarioView,
)


def root_redirect(request):
    return redirect('/api/')


router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'reporte-bi', ReporteViewSet, basename='reporte-bi')
router.register(r'movimientos', MovimientoStockViewSet)
urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/crear-usuario/', CrearUsuarioView.as_view(), name='crear-usuario'),

    path('api/dashboard-stats/', DashboardStatsView.as_view(),
         name='dashboard-stats'),
]
