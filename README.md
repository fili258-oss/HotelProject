# Sistema de Gestión Hotelera

Sistema web monolítico desarrollado con Django para la gestión de reservas, reseñas y habitaciones de hotel.

## Características

- Gestión de habitaciones y tipos de habitación
- Sistema de reservas con fechas y precios
- Reseñas y calificaciones de huéspedes
- Autenticación de usuarios y perfiles
- Panel de administración para gestión hotelera
- Diseño responsivo con Bootstrap 5.2

## Estructura del proyecto

```
hotel_management/                  # Directorio raíz del proyecto
├── manage.py                      # Script de administración de Django
├── requirements.txt               # Dependencias del proyecto
├── .gitignore                     # Archivo gitignore
├── README.md                      # Este archivo

├── hotel_project/                 # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py                # Configuración global
│   ├── urls.py                    # URLs principales
│   ├── asgi.py                    # Configuración ASGI para despliegue
│   └── wsgi.py                    # Configuración WSGI para despliegue

├── accounts/                      # Aplicación para gestión de usuarios
│   ├── __init__.py
│   ├── admin.py                   # Configuración del admin para usuarios
│   ├── apps.py
│   ├── forms.py                   # Formularios personalizados para registro/login
│   ├── migrations/                # Migraciones de la BD
│   ├── models.py                  # Modelos extendidos de usuario
│   ├── tests.py                   # Tests para la aplicación
│   ├── urls.py                    # URLs específicas de autenticación
│   └── views.py                   # Vistas para login, registro, perfil, etc.

├── reservations/                  # Aplicación para reservas
│   ├── __init__.py
│   ├── admin.py                   # Configuración del admin para reservas
│   ├── apps.py
│   ├── forms.py                   # Formularios para reservas
│   ├── migrations/
│   ├── models.py                  # Modelos de reserva
│   ├── tests.py
│   ├── urls.py
│   └── views.py                   # Vistas CRUD para reservas

├── rooms/                         # Aplicación para habitaciones
│   ├── __init__.py
│   ├── admin.py                   # Configuración del admin para habitaciones
│   ├── apps.py
│   ├── forms.py                   # Formularios para habitaciones
│   ├── migrations/
│   ├── models.py                  # Modelos de habitaciones, tipos, características
│   ├── tests.py
│   ├── urls.py
│   └── views.py                   # Vistas CRUD para habitaciones

├── reviews/                       # Aplicación para reseñas
│   ├── __init__.py
│   ├── admin.py                   # Configuración del admin para reseñas
│   ├── apps.py
│   ├── forms.py                   # Formularios para reseñas
│   ├── migrations/
│   ├── models.py                  # Modelos de reseñas
│   ├── tests.py
│   ├── urls.py
│   └── views.py                   # Vistas CRUD para reseñas

├── core/                          # Aplicación central del hotel
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py      # Context processors para datos globales
│   ├── forms.py                   # Formularios generales
│   ├── migrations/
│   ├── models.py                  # Modelos comunes
│   ├── tests.py
│   ├── urls.py                    # URLs de páginas principales
│   └── views.py                   # Vistas principales (inicio, contacto, etc.)

├── api/                           # Opcional: para API REST
│   ├── __init__.py
│   ├── serializers.py             # Serializadores para los modelos
│   ├── urls.py                    # URLs de la API
│   └── views.py                   # Vistas de la API

├── templates/                     # Plantillas HTML (enfoque central)
│   ├── base.html                  # Plantilla base con estructura común
│   ├── partials/                  # Componentes reutilizables
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   └── messages.html          # Para notificaciones
│   ├── accounts/                  # Plantillas de usuarios
│   ├── reservations/              # Plantillas de reservas
│   ├── rooms/                     # Plantillas de habitaciones
│   ├── reviews/                   # Plantillas de reseñas
│   └── core/                      # Plantillas principales

├── static/                        # Archivos estáticos
│   ├── css/
│   │   └── custom.css             # Estilos personalizados
│   ├── js/
│   │   └── main.js                # Scripts personalizados
│   └── img/                       # Imágenes del sitio
│       └── logo.png

└── media/                         # Archivos subidos por usuarios
    ├── room_photos/               # Fotos de habitaciones
    └── user_profiles/             # Fotos de perfil de usuarios
```

## Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (opcional pero recomendado)

## Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/hotel-management.git
cd hotel-management
```

2. **Crear un entorno virtual**

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**

```bash
# Crear las migraciones iniciales
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear un superusuario para acceder al admin
python manage.py createsuperuser
```

5. **Ejecutar el servidor de desarrollo**

```bash
python manage.py runserver
```

Ahora puedes acceder a:
- Sitio web: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## Dependencias principales

El archivo `requirements.txt` incluye las siguientes dependencias:

```
Django==5.0.3
django-environ==0.11.2
Pillow==10.1.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
```

## Configuración del entorno

Para configuración local, crea un archivo `.env` en la raíz del proyecto:

```
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
```

## Despliegue en producción

Para desplegar en un servidor con Nginx:

1. Instala las dependencias de producción:

```bash
pip install gunicorn psycopg2-binary
```

2. Configura tu servidor Nginx para servir el proyecto:

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location /static/ {
        alias /ruta/a/tu/proyecto/staticfiles/;
    }

    location /media/ {
        alias /ruta/a/tu/proyecto/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Configura Gunicorn como servidor WSGI:

```bash
gunicorn hotel_project.wsgi:application --bind 127.0.0.1:8000
```

## Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añade nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
