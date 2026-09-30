# Imagen de la API de tareas. Funciona igual con Podman y con Docker:
#   podman build -t tareas-hexagonal -f Containerfile .
FROM python:3.12-slim

# Evita archivos .pyc y muestra los logs de inmediato.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    RUTA_DB=/datos/tareas.db

WORKDIR /app

# Primero las dependencias: así la capa se reutiliza mientras no cambien.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# Usuario sin privilegios y carpeta para la base de datos.
RUN useradd --create-home appuser && mkdir /datos && chown appuser /datos
USER appuser
VOLUME /datos

EXPOSE 8000
CMD ["uvicorn", "tareas.principal:app", "--host", "0.0.0.0", "--port", "8000"]
