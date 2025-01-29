#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Importaciones de las capas
from infrastructure.ml.cnn_model import PneumoniaCNN
from infrastructure.image.image_preprocessor import XrayPreprocessor
from infrastructure.image.dicom_reader import DicomReader
from application.services.diagnosis_service import DiagnosisService
from Presentation.gui.main_window import PneumoniaDetectorGUI
from domain.entities.chest_xray import ChestXray

class ApplicationFactory:
    """Fábrica para crear e inicializar los componentes de la aplicación"""
    
    @staticmethod
    def create_services():
        # Inicializar componentes de infraestructura
        model_service = PneumoniaCNN('conv_MLP_84.h5')
        image_processor = XrayPreprocessor()
        dicom_reader = DicomReader()
        
        # Crear servicio de diagnóstico
        diagnosis_service = DiagnosisService(
            model_service=model_service,
            image_processor=image_processor
        )
        
        return {
            'diagnosis_service': diagnosis_service,
            'dicom_reader': dicom_reader
        }

def setup_logging():
    """Configurar el sistema de logging"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pneumonia_detector.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Punto de entrada principal de la aplicación"""
    try:
        # Configurar logging
        setup_logging()
        
        # Crear servicios
        services = ApplicationFactory.create_services()
        
        # Iniciar interfaz gráfica
        app = PneumoniaDetectorGUI(
            diagnosis_service=services['diagnosis_service'],
            dicom_reader=services['dicom_reader']
        )
        
        # Ejecutar la aplicación
        app.run()
        
    except Exception as e:
        import logging
        logging.error(f"Error en la aplicación: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()