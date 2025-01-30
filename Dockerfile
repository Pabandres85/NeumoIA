# Usar una versión específica y estable de python
FROM python:3.8-slim-buster

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0
ENV PYTHONPATH=/app

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar versiones específicas en orden
RUN pip install --no-cache-dir keras==2.4.0 && \
    pip install --no-cache-dir numpy==1.19.2 && \
    pip install --no-cache-dir tensorflow==2.4.0 && \
    pip install --no-cache-dir h5py==2.10.0 && \
    pip install --no-cache-dir protobuf==3.19.6

# Instalar el resto de dependencias
RUN pip install --no-cache-dir \
    opencv-python==4.11.0.86 \
    Pillow==8.2.0 \
    pydicom==2.2.2 \
    pandas==1.3.3 \
    matplotlib==3.4.3 \
    tkcap==0.0.4 \
    PyAutoGUI==0.9.54

# Copiar el código y el modelo
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "detector_neumonia.py"]
