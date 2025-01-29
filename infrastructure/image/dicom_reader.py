import pydicom
import numpy as np
import cv2
from PIL import Image
from typing import Tuple

class DicomReader:
    @staticmethod
    def read_image(filepath: str) -> Tuple[np.ndarray, Image.Image]:
        """
        Lee una imagen DICOM o JPG y retorna tanto el array numpy como la imagen PIL
        Compatible con pydicom 2.2.2 y Pillow 8.2.0
        """
        try:
            if filepath.endswith('.dcm'):
                # Lectura DICOM usando pydicom 2.2.2
                img = pydicom.dcmread(filepath)
                img_array = img.pixel_array
                
                # Convertir a formato compatible
                img_array = img_array.astype(float)
                img_array = ((img_array - img_array.min()) * (255.0 / (img_array.max() - img_array.min())))
                img_array = img_array.astype(np.uint8)
                
                # Asegurar que sea RGB
                if len(img_array.shape) == 2:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
                
                # Crear imagen PIL
                img_pil = Image.fromarray(img_array)
                
            else:
                # Lectura JPG/PNG usando Pillow 8.2.0
                img_pil = Image.open(filepath)
                img_array = np.array(img_pil)
                
                # Asegurar que sea RGB
                if len(img_array.shape) == 2:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
                    img_pil = Image.fromarray(img_array)
                
            return img_array, img_pil
            
        except Exception as e:
            raise ValueError(f"Error al leer la imagen: {str(e)}")