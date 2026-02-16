[![CI/CD Ferretería V2](https://github.com/FJMichea/ferreteria_v2/actions/workflows/main.yml/badge.svg)](https://github.com/FJMichea/ferreteria_v2/actions/workflows/main.yml)

# ⚙️ ERP Ferretería Quilpuecito - Backend API (Django REST)

¡Bienvenido al núcleo de nuestro ERP! Este repositorio contiene el Backend robusto y escalable desarrollado para el Sistema de Gestión y Control de Inventarios de la Ferretería. 

Construido sobre una arquitectura API RESTful y preparado para entornos en contenedores (Docker), este sistema permite un desacoplamiento total del Frontend, garantizando seguridad, integridad de datos y alta disponibilidad.

## 🌐 Entorno de Producción (Live Demo)
El sistema se encuentra desplegado en la nube utilizando los servidores de Render.
* **API REST base:** [https://api-ferreteria-michea.onrender.com/api/]
* **Panel de Administración Segura (PostgreSQL GUI):** [https://api-ferreteria-michea.onrender.com/admin/]

### 🔐 Credenciales de Acceso (Entorno Demo)
Para evaluar las funcionalidades del sistema o acceder al Panel de Administración, utilice las siguientes credenciales:
* **Administrador (Acceso Total):** Usuario: `admin` | Contraseña: `12345`
* **Vendedor (Acceso Restringido):** Usuario: `vendedor1` 
| Contraseña: `vendedor_ferreteria123`
> *Nota: En un entorno de producción corporativo real, las contraseñas se almacenan con hashing criptográfico (PBKDF2) en PostgreSQL.*

## 🚀 Stack Tecnológico y Arquitectura
* **Core:** Python 3.12
* **Framework Web:** Django 6.0 + Django REST Framework (DRF)
* **Inteligencia de Negocios:** Pandas (Motor analítico para KPIs)
* **Base de Datos:** PostgreSQL 15 (Modelado estricto con integridad referencial)
* **Seguridad:** Simple JWT (JSON Web Tokens para autenticación sin estado)
* **Infraestructura:** Docker, Docker Compose y GitHub Actions (CI/CD)

## 🔐 Características Destacadas (Fase 1)
* **API RESTful Completa:** Endpoints CRUD optimizados con serialización JSON.
* **Prevención de Quiebre de Stock:** Lógica transaccional a nivel de servidor que impide salidas físicas superiores al stock disponible.
* **Trazabilidad Continua:** Registro inalterable de auditoría (Kardex) para cada movimiento.
* **Dashboard BI (`/api/reporte-bi/`):** Algoritmos de análisis que procesan en tiempo real el valor del inventario, capital inmovilizado y tasa de rotación.

## 🛠️ Instalación y Entorno de Desarrollo (Local)
Para desarrollo y pruebas locales, el proyecto está dockerizado para replicación exacta del entorno:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/FJMichea/ferreteria_v2.git](https://github.com/FJMichea/ferreteria_v2.git)
   cd ferreteria_v2

Levantar los contenedores (Servidor + DB):
docker-compose up --build

Acceso local: La API estará disponible en http://localhost:8000/api/

Roadmap y Futuras Mejoras
La arquitectura micro-orientada está lista para integrar:

Machine Learning & Predicción de Demanda (Scikit-Learn).

Integración Webhooks Facturación Electrónica (SII Chile).

Soporte API para App Móvil de Bodegueros.

**Desarrollado por:** Francisco Michea
