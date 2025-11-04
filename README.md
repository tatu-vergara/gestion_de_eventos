# 🗓️ Plataforma de Gestión de Eventos — Django

Proyecto desarrollado para el módulo de **Desarrollo de aplicaciones web con python y Django**, como parte del Bootcamp Fullstack.  
Permite registrar usuarios, crear y gestionar eventos, y aplicar roles y permisos utilizando el modelo **Auth** de Django.

---

## Descripción General

La aplicación permite:
- Registro, inicio y cierre de sesión de usuarios.
- Creación, visualización, edición y eliminación de eventos.
- Control de acceso a eventos **públicos** y **privados**.
- Gestión de **roles y permisos** (administrador, organizador, asistente).
- Uso de `LoginRequiredMixin`, `PermissionRequiredMixin` y sistema de `messages` de Django.
- Redirecciones y manejo de errores 403 con mensajes personalizados.

---

## Tecnologías Utilizadas

- **Python 3.11+**
- **Django 5.x**
- SQLite (por defecto)
- HTML + SimpleCSS

---

## 📦 Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/usuario/nombre-del-repo.git
cd nombre-del-repo

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario (Administrador)
python manage.py createsuperuser

# 6. Inicializar roles y permisos
python manage.py init_roles

# 7. Ejecutar servidor
python manage.py runserver
