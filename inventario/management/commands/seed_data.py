import random
from django.core.management.base import BaseCommand
from inventario.models import Categoria, Producto
from django.db import transaction

class Command(BaseCommand):
    help = 'Genera datos masivos para pruebas de análisis de datos'

    def handle(self, *args, **kwargs):
        # Listas de palabras para generar nombres realistas aleatorios
        HERRAMIENTAS = ['Taladro', 'Martillo', 'Destornillador', 'Sierra', 'Llave', 'Alicate', 'Lijadora']
        MATERIALES = ['Cemento', 'Arena', 'Grava', 'Yeso', 'Pasta Muro', 'Ladrillo', 'Cerámica']
        ELECTRICIDAD = ['Cable', 'Enchufe', 'Ampolleta', 'Interruptor', 'Automático', 'Fusible']
        
        MARCAS = ['Makita', 'Bosch', 'Stanley', 'Black&Decker', 'Generico', '3M', 'Phillips']
        MEDIDAS = ['Grande', 'Pequeño', 'Industrial', 'Hogar', 'Pro', 'X200', '5kg', '20mm']

        with transaction.atomic():
            self.stdout.write("Limpiando base de datos...")
            Producto.objects.all().delete()
            Categoria.objects.all().delete()

            self.stdout.write("Creando categorías base...")
            cat_herr = Categoria.objects.create(nombre="Herramientas", descripcion="Equipamiento manual y eléctrico")
            cat_const = Categoria.objects.create(nombre="Construcción", descripcion="Materiales de obra gruesa")
            cat_elec = Categoria.objects.create(nombre="Electricidad", descripcion="Insumos eléctricos")
            
            categorias = [cat_herr, cat_const, cat_elec]

            self.stdout.write("Generando 500 productos simulados...")
            productos_a_crear = []
            
            for i in range(1, 501):
                # Elegimos categoría al azar
                cat_random = random.choice(categorias)
                
                # Generamos nombre según categoría para que tenga sentido
                if cat_random == cat_herr:
                    base = random.choice(HERRAMIENTAS)
                elif cat_random == cat_const:
                    base = random.choice(MATERIALES)
                else:
                    base = random.choice(ELECTRICIDAD)
                
                nombre_final = f"{base} {random.choice(MARCAS)} {random.choice(MEDIDAS)}"
                
                # Precio aleatorio entre 500 y 150.000
                precio_random = random.randint(5, 1500) * 100 
                
                # Stock aleatorio (algunos con 0 para probar alertas de stock crítico)
                stock_random = random.choices([0, random.randint(1, 5), random.randint(10, 200)], weights=[5, 15, 80])[0]

                producto = Producto(
                    sku=f"PROD-{i:04d}", # Genera PROD-0001, PROD-0002...
                    nombre=nombre_final,
                    categoria=cat_random,
                    precio=precio_random,
                    stock=stock_random
                )
                productos_a_crear.append(producto)

            # Usamos bulk_create para insertar 500 registros de una sola vez (Muy eficiente)
            Producto.objects.bulk_create(productos_a_crear)

            self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se crearon {len(productos_a_crear)} productos.'))