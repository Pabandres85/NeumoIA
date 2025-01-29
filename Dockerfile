# 
FROM python:3.8-slim-buster

#  Variables de entorno 
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0
ENV PYTHONPATH=/app

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#  Actualizar pip
RUN python -m pip install --upgrade pip

# Copiar los archivos de requerimientos
COPY requirements.txt .

#  dependencias de Python sin caché para reducir tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código y el modelo al contenedor
COPY . .

# Configurar el comando por defecto para ejecutar la aplicación
CMD ["python", "detector_neumonia.py"]
