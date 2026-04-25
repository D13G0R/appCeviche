# appCeviche

Breve proyecto Django para la gestión de productos y pedidos.

**Requisitos**
- Python 3.8+
- PostgreSQL (recomendado) o SQLite para desarrollo

**Instalación local**

1. Clona el repositorio:

```bash
git clone <repo-url>
cd appCeviche
```

2. Crea y activa un entorno virtual:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Crea el archivo de entorno a partir del ejemplo y configura las variables:

```bash
copy .env.example .env
# editar .env y ajustar SECRET_KEY, DATABASE_URL, DEBUG, etc.
```

5. Aplica migraciones y crea un superusuario:

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Recopila archivos estáticos (producción):

```bash
python manage.py collectstatic
```

7. Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

**Despliegue**
- El proyecto incluye `Procfile` y `runtime.txt` pensados para plataformas tipo Heroku.
- Asegúrate de configurar las variables de entorno en el proveedor de hosting (SECRET_KEY, DATABASE_URL, DEBUG= False, ALLOWED_HOSTS, etc.).

**Archivos relevantes**
- [requirements.txt](requirements.txt): dependencias del proyecto
- [.env.example](.env.example): ejemplo de variables de entorno
- [Procfile](Procfile): configuración de arranque para Heroku

Si quieres que prepare un `docker-compose` o que fije versiones concretas de paquetes, dímelo y lo agrego.
