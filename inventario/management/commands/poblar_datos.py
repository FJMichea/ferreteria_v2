import random
from django.core.management.base import BaseCommand
from inventario.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Puebla la base de datos con 100 productos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando creación de datos...")

        # 1. Crear Categorías (Usamos get_or_create para que no falle si ya existen)
        categorias_data = ["Herramientas Manuales", "Electricidad", "Gasfitería", "Pinturas", "Construcción"]
        categorias_objs = []
        
        for nombre in categorias_data:
            # Asumimos que Categoria SI tiene descripción. Si fallara aquí, avísame.
            cat, created = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': f'Todo para {nombre}'})
            categorias_objs.append(cat)
            if created:
                self.stdout.write(f"Categoría creada: {nombre}")

        # 2. Listas para generar nombres aleatorios coherentes
        adjetivos = ["Profesional", "Hogar", "Industrial", "Premium", "Económico", "Reforzado"]
        
        productos_base = {
            "Herramientas Manuales": ["Martillo", "Destornillador", "Alicate", "Llave Inglesa", "Serrucho", "Cinta Métrica", "Nivel", "Formón"],
            "Electricidad": ["Cable 2.5mm", "Enchufe Doble", "Interruptor", "Ampolleta LED", "Cinta Aislante", "Automático 10A", "Extension 5m"],
            "Gasfitería": ["Llave de Paso", "Codo PVC", "Teflón", "Sifón Lavamanos", "Flexible 30cm", "Soldadura Estaño", "Pasta Soldar"],
            "Pinturas": ["Brocha 2 pulgadas", "Rodillo Felpa", "Esmalte Blanco", "Lija Madera", "Bandeja Pintura", "Aguarrás", "Látex Interior"],
            "Construcción": ["Cemento 25kg", "Yeso 1kg", "Fragüe", "Silicona Multiuso", "Clavos 2 pulgadas", "Tornillos Madera", "Adhesivo Montaje"]
        }

        # 3. Crear 100 Productos
        contador = 0
        
        # Generamos productos iterando hasta llegar a 100
        while contador < 100:
            categoria_random = random.choice(categorias_objs)
            nombre_base = random.choice(productos_base[categoria_random.nombre])
            adjetivo = random.choice(adjetivos)
            
            nombre_producto = f"{nombre_base} {adjetivo}"
            sku_generado = f"PROD-{str(contador + 1).zfill(4)}" 
            
            if not Producto.objects.filter(sku=sku_generado).exists():
                prod = Producto(
                    sku=sku_generado,
                    nombre=nombre_producto,
                    categoria=categoria_random,
                    precio=random.randint(1000, 50000), 
                    stock=random.randint(5, 200)
                    # Eliminamos la línea 'descripcion' porque el modelo no la tiene
                )
                prod.save()
                contador += 1
                
                if contador % 10 == 0:
                    self.stdout.write(f"Van {contador} productos creados...")

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se han creado {contador} productos correctamente.'))