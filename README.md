# 🐲 Monstro-Mercado

**Monstro-Mercado** es una aplicación web desarrollada con **Django** que simula un mercado en línea, permitiendo a los usuarios explorar productos, agregarlos a favoritos o al carrito, y gestionar su perfil dentro de la plataforma.

---

## 🚀 Características principales

- 🛒 Gestión de productos y categorías  
- ❤️ Sistema de favoritos  
- 👤 Módulo de usuarios y perfiles  
- 🧾 Carrito de compras  
- 📦 Integración de base de datos SQLite  
- 🖼️ Soporte para archivos multimedia (imágenes de productos, etc.)  

---

## 🧩 Tecnologías utilizadas

- **Python 3.12+**
- **Django 5.x**
- **HTML / CSS / JavaScript**
- **SQLite3**
- **Virtualenv**

---

## ⚙️ Instalación y ejecución local

Sigue estos pasos para correr el proyecto en tu entorno local:

bash
# 1. Clonar el repositorio
git clone https://github.com/guuty/Monstro-Mercado.git

# 2. Ingresar al directorio del proyecto
cd Monstro-Mercado

# 3. Crear un entorno virtual
python -m venv venv

# 4. Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 5. Instalar las dependencias
pip install -r requirements.txt

# 6. Ejecutar migraciones
python manage.py migrate

# 7. (Opcional) Cargar datos iniciales
python init_db.py

# 8. Ejecutar el servidor
python manage.py runserver

## 🗃️ Estructura del proyecto

# Monstro-Mercado/
# │
# ├── core/ # Configuración base del sitio
# ├── favoritos/ # Gestión de productos favoritos
# ├── market/ # Lógica principal del mercado
# ├── media/ # Archivos subidos (imágenes, etc.)
# ├── mymarket/ # Configuración del proyecto Django
# ├── perfil/ # Perfiles de usuario
# ├── productos/ # Modelos y vistas de productos
# ├── scripts/ # Scripts de utilidad
# ├── static/ # Archivos estáticos (CSS, JS, imágenes)
# ├── venv/ # Entorno virtual
# │
# ├── db.sqlite3 # Base de datos
# ├── init_db.py # Script para inicializar datos
# ├── manage.py # Comando principal de Django
# ├── requirements.txt # Dependencias del proyecto
# └── build.sh # Script de despliegue

## 👥 Autores

- Ferreyra Gustavo  
- Celiz Leandro

## 💬 Contacto

- 📧 [gustavoleonelferreyra@gmail.com]
- 📧 [leandroceliz9@gmail.com]

## 🔗 Repositorio oficial
- https://github.com/guuty/Monstro-Mercado
