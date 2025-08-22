# Imagen base
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Bogota \
    DJANGO_SETTINGS_MODULE=appCeviche.settings

# Dependencias del sistema necesarias para mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar el proyecto
COPY . /app

# Instalar dependencias de Python (sin requirements.txt, instalamos las claves)
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir \
      "django>=5.0,<6.0" \
      djangorestframework \
      mysqlclient \
      django-cors-headers \
      gunicorn

# Exponer puerto
EXPOSE 8000

# Comando por defecto: gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "appCeviche.wsgi:application"]

