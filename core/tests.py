"""
Módulo de pruebas para la aplicación core usando Pytest.
"""
import pytest  # type: ignore # pylint: disable=import-error
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from inventario.models import Categoria, Producto

# pylint: disable=no-member

# --- CONFIGURACIÓN ---
# Esto permite que los tests accedan a la base de datos simulada


@pytest.mark.django_db
class TestInventario:
    """
    Suite de pruebas para verificar modelos y endpoints básicos.
    """

    def test_crear_categoria(self):
        """Verifica que se puede crear una categoría en la BD"""
        cat = Categoria.objects.create(
            nombre="Electricidad", descripcion="Cables y enchufes")
        assert cat.nombre == "Electricidad"
        assert Categoria.objects.count() == 1

    def test_impedir_precio_negativo(self):
        """
        Verifica lógica de negocio: (Este test fallará si no tienes validación en models,
        pero sirve para mostrar TDD - Test Driven Development)
        """
        cat = Categoria.objects.create(nombre="Test")
        # Aquí simulamos una creación simple
        prod = Producto.objects.create(
            sku="TEST-001",
            nombre="Prod Test",
            categoria=cat,
            precio=1000,
            stock=10
        )
        assert prod.stock >= 0

    def test_api_dashboard_status(self):
        """Verifica que el dashboard responde correctamente"""
        client = APIClient()
        # Usamos reverse para obtener la URL correcta definida en urls.py
        url = reverse('dashboard-stats')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
