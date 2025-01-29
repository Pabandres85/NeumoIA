#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import tensorflow as tf

# ✅ Habilitar Eager Execution antes de importar cualquier otro módulo
tf.compat.v1.enable_eager_execution()  
print("🔹 Eager Execution habilitado:", tf.executing_eagerly())

# Configuración de TensorFlow para GPU
tf.compat.v1.experimental.output_all_intermediates(True)

# Importaciones de las capas de la aplicación
from infrastructure.ml.cnn_model import PneumoniaCNN
from infrastructure.image.image_preprocessor import XrayPreprocessor
from infrastructure.image.dicom_reader import DicomReader
from application.services.diagnosis_service import DiagnosisService
from Presentation.gui.main_window import PneumoniaDetectorGUI

def setup_services():
    """Inicializa y configura todos los servicios necesarios"""
    try:
        # Inicializar servicios de infraestructura
        model_service = PneumoniaCNN('./model/conv_MLP_84.h5')
        image_processor = XrayPreprocessor()
        
        # Crear servicio de diagnóstico
        diagnosis_service = DiagnosisService(
            model_service=model_service,
            image_processor=image_processor
        )
        
        return diagnosis_service
        
    except Exception as e:
        print(f"Error al configurar servicios: {str(e)}")
        raise

def setup_logging():
    """Configura el sistema de logging"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='pneumonia_detector.log'
    )

def main():
    """Punto de entrada principal de la aplicación"""
    try:
        # Configurar logging
        setup_logging()
        
        # Configurar servicios
        diagnosis_service = setup_services()
        
        # Iniciar interfaz gráfica
        app = PneumoniaDetectorGUI(diagnosis_service=diagnosis_service)
        
        # Ejecutar la aplicación
        app.run()
        
    except Exception as e:
        import logging
        logging.error(f"Error en la aplicación: {str(e)}", exc_info=True)
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()