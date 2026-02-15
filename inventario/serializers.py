from rest_framework import serializers
from .models import Producto, Categoria
from .models import MovimientoStock


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    # Esto muestra el nombre de la categoría en vez de solo el ID
    categoria_nombre = serializers.CharField(
        source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'


class MovimientoStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = MovimientoStock
        fields = '__all__'
