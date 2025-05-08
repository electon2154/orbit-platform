# Django B2B E-commerce Platform

Una plataforma de comercio electrónico B2B desarrollada con Django para conectar compañías y tiendas minoristas.

## Características

- Sistema de autenticación con diferentes tipos de usuario (Compañías y Tiendas)
- Catálogo de productos
- Carrito de compras
- Sistema de pedidos
- Panel de control para compañías y tiendas
- Mapas de localización
- Sistema de cambio de contraseña
- Tema Materio Admin

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Django-B2BProject
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar las migraciones:
```bash
python manage.py migrate
```

5. Crear un superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor:
```bash
python manage.py runserver
```

## Tema Materio

El proyecto ahora incluye el tema de administración Materio que ofrece un diseño moderno y responsivo. Para activar completamente el tema:

1. Asegúrese de que los archivos estáticos estén correctamente configurados:
```bash
python manage.py collectstatic
```

2. Activar el tema Materio en settings.py:
```python
TEMPLATES = [
    {
        # ...
        'DIRS': [BASE_DIR / 'templates'],
        # ...
    }
]
```

3. Los nuevos templates están disponibles con el sufijo '_materio' y pueden utilizarse en las vistas:
   - base_materio.html
   - home_materio.html
   - customer_dashboard_materio.html
   - company_dashboard_materio.html
   - login_materio.html

4. Para cambiar entre el tema original y Materio, puede modificar las vistas correspondientes para usar los templates deseados.

## Estructura del Proyecto

- **core/**: Configuración principal del proyecto
- **user_accounts/**: Gestión de usuarios y perfiles
- **product_catalog/**: Catálogo de productos
- **company_profiles/**: Perfiles de compañías
- **order_management/**: Gestión de pedidos
- **shopping_cart/**: Carrito de compras
- **templates/**: Plantillas HTML
- **static/**: Archivos estáticos (CSS, JS, imágenes)

## Contribuir

1. Haga un fork del repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios y haga commit (`git commit -m 'Añadir nueva funcionalidad'`)
4. Haga push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abra un Pull Request 