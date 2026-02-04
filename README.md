[![CI/CD Ferretería V2](https://github.com/FJMichea/ferreteria_v2/actions/workflows/main.yml/badge.svg)](https://github.com/FJMichea/ferreteria_v2/actions/workflows/main.yml)
# Sistema de Gestión de Inventario (API REST)

Backend robusto desarrollado para la gestión de inventario de "Ferretería Quilpuecito". Este proyecto implementa una arquitectura moderna orientada a microservicios utilizando contenedores.

## 🚀 Tecnologías

* **Lenguaje:** Python 3.12
* **Framework:** Django 6.0 + Django REST Framework
* **Base de Datos:** PostgreSQL 15
* **Infraestructura:** Docker & Docker Compose

## 🛠️ Instalación y Uso

Este proyecto está dockerizado, por lo que no necesitas instalar Python ni PostgreSQL localmente.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/FJMichea/ferreteria-backend-lms.git
    cd ferreteria-backend-lms
    ```

2.  **Iniciar el proyecto:**
    ```bash
    docker-compose up --build
    ```

3.  **Acceder a la API:**
    * El servidor estará corriendo en: `http://localhost:8000`
    * Endpoint de productos: `http://localhost:8000/api/productos/`
    * Endpoint de categorías: `http://localhost:8000/api/categorias/`

## 📋 Características Técnicas

* **API RESTful:** Endpoints CRUD completos con serialización JSON.
* **Base de Datos Relacional:** Modelado estricto con integridad referencial (Foreign Keys).
* **Entorno Aislado:** Configuración completa en `docker-compose.yml` para replicación exacta en cualquier entorno de desarrollo.

---
**Desarrollado por:** Francisco Javier Michea Acuña
