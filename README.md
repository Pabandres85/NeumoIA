
---

# 🏥 Pneumonia Detection System

## 📌 Introducción

Este proyecto tiene como objetivo principal desarrollar un sistema basado en **inteligencia artificial (IA)** para la identificación de **neumonía** en imágenes de radiografías de tórax. Para ello, se partió de un repositorio proporcionado, que contenía parte del código y la estructura necesaria para el sistema.

Este documento describe los pasos implementados para completar el código, asegurar su correcto funcionamiento y garantizar la calidad del sistema mediante **pruebas unitarias**. Además, se incluyen las soluciones aplicadas para alcanzar los objetivos del proyecto.

---

## ✅ Pasos Realizados

### 🔹 1. Clonación del Repositorio

El primer paso fue **clonar el repositorio** proporcionado, lo que permitió obtener una copia local del proyecto en el entorno de desarrollo.

### 🔹 2. Configuración del Entorno con Docker 🐳

Para garantizar que el sistema funcione en un entorno controlado, se utilizó **Docker**. Esto permitió desplegar el sistema en un entorno aislado y asegurar que todas las dependencias estuvieran correctamente instaladas.

### 🔹 3. Funciones Implementadas ⚙️

#### 🔹 `from_file`

La función `from_file` es un método de clase que crea una instancia de `ChestXray` a partir de un archivo de imagen. Maneja dos formatos principales:

- 📌 **DICOM**: Formato especializado para imágenes médicas. La imagen se convierte a escala de grises, se normaliza a valores entre 0 y 255 y finalmente se transforma a formato RGB.
- 📌 **JPG/PNG**: Se lee directamente la imagen sin modificaciones adicionales.

En ambos casos, se genera y retorna un objeto `ChestXray` con el ID del paciente, la imagen procesada y el tipo de imagen correspondiente.

📌 **Las versiones utilizadas en la implementación del proyecto fueron las siguientes:**

![📝 Requerimientos](images_readme/Requeriment.jpg)

También se implementó un **`Dockerfile`**, que define un entorno de contenedor para ejecutar la aplicación de Python, incluyendo todas las dependencias necesarias y estableciendo un comando de inicio para la ejecución del sistema.

---

## 🏗️ 4. Implementación de un Patrón de Diseño

Para facilitar el desarrollo y las pruebas unitarias, se implementó una **arquitectura en capas**. Este enfoque permite separar las responsabilidades del sistema en diferentes componentes, haciendo que el código sea más modular, mantenible y fácil de probar. 

📌 **Las capas implementadas fueron:**

- 🎨 **Capa de Presentación**: Maneja la interfaz de usuario, permitiendo la carga y visualización de imágenes.
- 🧠 **Capa de Lógica de Negocio**: Contiene el algoritmo de predicción de neumonía y la lógica principal del sistema.
- 📂 **Capa de Acceso a Datos**: Gestiona la carga y el procesamiento de las imágenes de radiografías.

Esta separación en capas permitió realizar pruebas unitarias de manera más eficiente, ya que cada componente pudo ser evaluado de forma independiente.

📌 **Estructura del proyecto:**

![📂 Estructura](images_readme/EstructuraProyecto.jpg)

📌 **A continuación, se describen las capas y su propósito en detalle:**

### 📌 Capa de Aplicación (`application/`)

📂 Contiene los servicios que coordinan la lógica de negocio:
- `diagnosis_service.py`: Maneja el flujo del proceso de diagnóstico, coordinando entre el procesamiento de imágenes y el modelo de IA.

### 📌 Capa de Dominio (`domain/`)

📂 Define las entidades centrales del negocio:
- `chest_xray.py`: Representa la radiografía de tórax.
- `diagnosis_result.py`: Modela el resultado del diagnóstico.

### 📌 Capa de Infraestructura (`infrastructure/`)

📂 Implementa los detalles técnicos y la integración con tecnologías específicas:
- `dicom_reader.py`: Lee imágenes en formato DICOM.
- `image_preprocessor.py`: Prepara las imágenes para el modelo de IA.

### 📌 Carpeta `ml/`

📂 Contiene los modelos de IA utilizados:
- `cnn_model.py`: Implementa la red neuronal convolucional para la detección de neumonía.

### 📌 Capa de Presentación (`presentation/`)

📂 Maneja la interfaz de usuario:
- `main_window.py`: Implementa la interfaz gráfica principal.

### 📌 Pruebas (`tests/`)

📂 Contiene la estructura de pruebas unitarias para cada componente principal.

### 📌 Archivos Principales 📑

- `detector_neumonia.py` → Punto de entrada principal de la aplicación.
- `requirements.txt` → Lista de dependencias del proyecto.
- `README.md` → Documentación del proyecto.
- `.gitignore` → Archivos y carpetas que deben ser ignorados por Git.

📌 **Beneficios de esta Arquitectura por Capas:**

✔️ Separación clara de responsabilidades.
✔️ Facilita el mantenimiento y la escalabilidad del sistema.
✔️ Permite modificar o reemplazar componentes sin afectar otras partes del código.
✔️ Proporciona una estructura clara para nuevos desarrolladores que se integren al proyecto.

---

## 🧪 5. Pruebas Unitarias

📌 **Las pruebas se centraron en las siguientes funcionalidades clave:**

- ✅ `diagnosis_service.py`: Se verificó que las funciones de diagnóstico se ejecutaran de manera eficiente y precisa.
- ✅ `chest_xray.py`: Se realizaron pruebas de carga de archivos en formatos JPG y DICOM para validar su correcto procesamiento.

---

## 🚀 6. Despliegue

📸 **Pantallazo de la aplicación:**

![🖼️ Pantallazo](images_readme/Pantallazo.jpg)

📌 Una vez finalizado el desarrollo y las pruebas, el sistema fue **desplegado en un entorno local con Linux** utilizando Docker. Posteriormente, se creó una imagen del contenedor y se subió a **Docker Hub**, donde puede ser accedido mediante el siguiente enlace:

🔗 [Repositorio en Docker Hub](https://hub.docker.com/repository/docker/pabandres13/pneumonia-detector/general)

---