from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Crea un superusuario automaticamente para entrar al admin'

    def handle(self, *args, **options):
        USERNAME = 'admin'
        EMAIL = 'admin@ferreteria.cl'
        PASSWORD = 'admin123_ferreteria' 

        if not User.objects.filter(username=USERNAME).exists():
            print(f"Creando superusuario: {USERNAME}...")
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            self.stdout.write(self.style.SUCCESS(f'¡LISTO! Usuario "{USERNAME}" creado. Clave: "{PASSWORD}"'))
        else:
            self.stdout.write(self.style.WARNING(f'El usuario "{USERNAME}" ya existe. No se hizo nada.'))