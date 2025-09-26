# Dockerfile para MedicConsult - Producción
FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=crud.settings

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gettext \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /app/static /app/media /app/logs /app/staticfiles

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Crear directorios con permisos correctos
RUN mkdir -p /app/staticfiles/js /app/staticfiles/css /app/staticfiles/images

# Exponer puerto
EXPOSE 8000

# Script de inicio
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Comando por defecto
ENTRYPOINT ["/bin/bash", "/app/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "crud.wsgi:application"]
