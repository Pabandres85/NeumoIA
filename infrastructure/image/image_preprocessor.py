import cv2
import numpy as np
from domain.interfaces.image_processor import ImageProcessor

class XrayPreprocessor(ImageProcessor):
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Implementa el preprocesamiento específico para rayos X:
        - Redimensionar a 512x512
        - Convertir a escala de grises
        - Aplicar CLAHE
        - Normalizar
        - Preparar para el modelo
        """
        # Redimensionar
        image = cv2.resize(image, (512, 512))
        
        # Convertir a escala de grises
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        # Aplicar CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        image = clahe.apply(image)
        
        # Normalizar
        image = image / 255.0
        
        # Preparar para el modelo
        image = np.expand_dims(image, axis=-1)
        image = np.expand_dims(image, axis=0)
        
        return image