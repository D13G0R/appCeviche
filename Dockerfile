# Imagen base
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Bogota \
    DJANGO_SETTINGS_MODULE=appCeviche.settings

# Dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# ----> ¡AQUÍ EMPIEZA EL CAMBIO! <----

# 1. Copia solo el archivo de requisitos.
COPY requirements.txt ./

# 2. Instala las dependencias desde ese archivo.
#    Esto se guarda en caché. Si no cambias requirements.txt, este paso no se volverá a ejecutar.
RUN pip install --no-cache-dir -r requirements.txt

# 3. AHORA copia el resto de tu código fuente.
COPY . .

# ----> ¡AQUÍ TERMINA EL CAMBIO! <----

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "-b", "0.0.0.0:8000", "appCeviche.wsgi:application"]