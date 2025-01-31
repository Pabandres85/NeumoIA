
## Proyecto deteccion neumonia con IA 

## Grupo 3
## Integrantes: 
Pablo Andrés Muñoz Martínez 
                Código: 2244676 
Lady Yasmin Hoyos Parra 
                Código: 2245224 
Johan David Mendoza Vargas 
                Código: 2245019
Yineth Tatiana Hernández Narvaez 
                Código: 2244789 


## Introducción

Este proyecto tiene como objetivo principal desarrollar un sistema basado en inteligencia artificial (IA) que permita identificar la presencia de neumonía en imágenes de radiografías de tórax. Para dicho objetivo se basó en un repositorio proporcionado, el cual contenía parte del código y la estructura necesaria para el sistema. 
En este documento, describe los pasos que se implementaron para completar el código, asegurar su correcto funcionamiento y garantizar la calidad del sistema mediante pruebas unitarias. Además, se incluyen las soluciones implementadas para alcanzar el objetivo del proyecto.

## Pasos Realizados

## 1. Clonación del Repositorio
El primer paso fue clonar el repositorio proporcionado que nos permitió obtener una copia local del proyecto en el entorno de desarrollo.

## 2. Configuración del Entorno con Docker
Para garantizar que el sistema funcione en un entorno controlado, se utilizó Docker. Esto permitió desplegar el sistema en un entorno aislado y asegurar que todas las dependencias estuvieran correctamente instaladas.

## 3. Implementación del Código con Arquitectura en Capas
El repositorio ya contenía parte del código desarrollado, por lo que la tarea principal fue completar las funciones faltantes. Las principales tareas realizadas fueron:
## Descripción Inicial del Código
Se proporciona una breve descripción del estado inicial del código antes de las modificaciones implementadas, incluyendo la estructura y funcionalidad básica.
## Arquitectura de Archivos Propuesta
detector_neumonia.py Contiene el diseño de la interfaz gráfica utilizando Tkinter. Los botones llaman métodos contenidos en otros scripts.
## integrator.py
 Es un módulo que integra los demás scripts y retorna solamente lo necesario para ser visualizado en la interfaz gráfica. Retorna la clase, la probabilidad y una imagen con el mapa de calor generado por Grad-CAM.
## read_img.py
 Script que lee la imagen en formato DICOM para visualizarla en la interfaz gráfica. Además, la convierte a un arreglo para su preprocesamiento.
## preprocess_img.py 
Script que recibe el arreglo proveniente de read_img.py y realiza las siguientes modificaciones: redimensiona a 512x512 píxeles, conversión a escala de grises, ecualización del histograma con CLAHE, normalización de la imagen entre 0 y 1, conversión del arreglo de imagen a formato de batch (tensor).
## load_model.py Script 
que lee el archivo binario del modelo de red neuronal convolucional previamente entrenado llamado 'WilhemNet86.h5'.
## grad_cam.py Script
 que recibe la imagen, la procesa, carga el modelo, obtiene la predicción y la capa convolucional de interés para extraer las características relevantes de la imagen.
## read_img.py
Se agregaron funciones y se especificaron las versiones de las librerías requeridas para el correcto funcionamiento del código.


## model_fun

def model_fun():
    """Load and return the trained neural network model"""
    try:
        # Load your saved model - update the path to where your model is stored
        model = tf.keras.models.load_model('path_to_your_model.h5')
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
        
La función model_fun carga un modelo de red neuronal desde un archivo especifico y devuelve el modelo cargado si todo va bien. Si ocurre algún error durante la carga del modelo, se captura la excepción, se imprime un mensaje de error y la función devuelve None.
## Inclusión de Funciones Adicionales
Adicionalmente, se incluyó una función para leer imágenes en formato JPG, que no estaba presente en el código original.

if filepath.endswith(".dcm"):
                self.array, img2show = read_dicom_file(filepath)
            else:
                self.array, img2show = read_jpg_file(filepath)

Las versiones que se utilizaron finalmente para la implementación del proyecto son las siguientes:

![Requeriments](C:\Users\guita\OneDrive\Escritorio\Neumon\UAO-Neumonia\images_readme\Requeriment.jpg)

También se implementó el dockerfile que define un entorno de contenedor y configura un entorno reproducible para ejecutar la aplicación de Python, incluyendo todas las dependencias del sistema y las librerías necesarias, y establece un comando para iniciar la aplicación al correr el contenedor

## Implementación de un patrón de diseño 
Para facilitar el desarrollo y las pruebas unitarias, se implementó un diseño de arquitectura en capas. Este enfoque permite separar las responsabilidades del sistema en diferentes componentes, lo que hace que el código sea más modular, mantenible y fácil de probar. Las capas implementadas fueron:

Capa de Presentación: Encargada de la interacción con el usuario, como la carga y visualización de imágenes.
Capa de Lógica de Negocio: Contiene el algoritmo de predicción de neumonía y la lógica principal del sistema.
Capa de Acceso a Datos: Gestiona la carga y el procesamiento de las imágenes de radiografías.

Esta separación en capas permitió realizar pruebas unitarias de manera más eficiente, ya que cada capa pudo ser probada de forma independiente.

![Estructura](C:\Users\guita\OneDrive\Escritorio\Neumon\UAO-Neumonia\images_readme\EstructuraProyecto.jpg)

La estructura de este  proyecto implementa una arquitectura por capas para un sistema de detección de neumonía usando IA. Vamos a desglosar cada capa y su propósito:

## Capa de Aplicación (application/)


Contiene los servicios que coordinan la lógica de negocio
diagnosis_service.py: Maneja el flujo del proceso de diagnóstico, coordinando entre el procesamiento de imágenes y el modelo de IA


## Capa de Dominio (domain/)


Define las entidades centrales del negocio
chest_xray.py: Representa la radiografía de tórax
diagnosis_result.py: Modela el resultado del diagnóstico


## Capa de Infraestructura (infrastructure/)


Implementa los detalles técnicos y la integración con tecnologías específicas
## Carpeta image/:

dicom_reader.py: Lee imágenes en formato DICOM (formato estándar médico)
image_preprocessor.py: Prepara las imágenes para el modelo de IA


## Carpeta ml/:

cnn_model.py: Implementa la red neuronal convolucional para la detección




## Capa de Presentación (presentation/)


Maneja la interfaz de usuario
main_window.py: Implementa la interfaz gráfica principal


## Pruebas (tests/)


Estructura de pruebas que refleja la estructura del proyecto
Incluye pruebas unitarias para cada componente principal

## Archivos Principales:

detector_neumonia.py: Punto de entrada principal de la aplicación
requirements.txt: Lista las dependencias del proyecto
README.md: Documentación del proyecto
.gitignore: Especifica archivos que Git debe ignorar

## Esta arquitectura por capas ofrece varios beneficios:

- Separación clara de responsabilidades
- Facilita el mantenimiento y las pruebas
- Permite cambiar componentes sin afectar otras partes del sistema
- Organización clara para nuevos desarrolladores que se unan al proyecto


## 4. Pruebas Unitarias
Las pruebas se enfocaron en las siguientes funciones:

Prueba de Carga de Imágenes: Se verificó que la función de carga de imágenes maneje correctamente archivos válidos y no válidos.

Prueba de Predicción: Se validó que el algoritmo de predicción devuelva resultados consistentes para diferentes tipos de imágenes.

![Pantallazo](C:\Users\guita\OneDrive\Escritorio\Neumon\UAO-Neumonia\images_readme\Pantallazo.jpg)

## 5. Despliegue 
Una vez completado el código y las pruebas, se desplegó el sistema en un entorno local utilizando Docker. Se realizaron pruebas manuales para asegurar que todas las funcionalidades estuvieran operativas.

