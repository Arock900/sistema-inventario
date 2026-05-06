# 📦 Sistema de Gestión de Inventario

API REST desarrollada con Django y Django REST Framework para gestionar el inventario de una tienda. Permite controlar productos, categorías y movimientos de stock con autenticación por token.

## 🚀 Tecnologías

- Python 3.13
- Django 6.0
- Django REST Framework 3.17
- SQLite
- Token Authentication

## ⚙️ Instalación

1. Clona el repositorio
\```bash
git clone https://github.com/Arock900/sistema-inventario.git
cd sistema-inventario
\```

2. Crea y activa el entorno virtual
\```bash
python -m venv .venv
.venv\Scripts\activate
\```

3. Instala las dependencias
\```bash
pip install django djangorestframework
\```

4. Corre las migraciones
\```bash
python manage.py migrate
\```

5. Crea un superusuario
\```bash
python manage.py createsuperuser
\```

6. Corre el servidor
\```bash
python manage.py runserver
\```

## 🔐 Autenticación

Registra un usuario y usa el token en el header de cada request:
\```
Authorization: Token tu_token_aqui
\```

## 📡 Endpoints

### Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/registro/ | Registrar usuario |
| POST | /api/login/ | Iniciar sesión |

### Categorías
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/categorias/ | Listar categorías |
| POST | /api/categorias/crear/ | Crear categoría 🔐 |

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/productos/ | Listar productos |
| GET | /api/productos/{id}/ | Obtener producto |
| POST | /api/productos/crear/ | Crear producto 🔐 |
| PUT | /api/productos/{id}/actualizar/ | Actualizar producto 🔐 |
| DELETE | /api/productos/{id}/eliminar/ | Eliminar producto 🔐 |

### Movimientos de Stock
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/movimientos/ | Listar movimientos 🔐 |
| POST | /api/movimientos/crear/ | Registrar movimiento de entrada o salida 🔐 |

🔐 = Requiere autenticación con token

## 💡 Características principales

- CRUD completo de productos y categorías
- Sistema de movimientos de inventario — entradas y salidas de stock
- Stock se actualiza automáticamente con cada movimiento
- Validaciones profesionales en cada endpoint
- Panel de administración incluido en /admin
- Autenticación por token en endpoints protegidos

## 👨‍💻 Autor

**Andrés Stived Rojas Muñoz**
Python Backend Developer en formación
[LinkedIn](https://www.linkedin.com/in/andres-stived-rojas-muñoz-4953531ab/) | [GitHub](https://github.com/Arock900)
