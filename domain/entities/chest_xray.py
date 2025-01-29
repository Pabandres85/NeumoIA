from dataclasses import dataclass
from datetime import datetime
import numpy as np
import pydicom
import cv2
from PIL import Image

@dataclass
class ChestXray:
    """Entidad que representa una imagen de rayos X de tórax"""
    patient_id: str
    image_array: np.ndarray
    image_type: str  # 'DICOM' o 'JPG'
    created_at: datetime = datetime.now()

    @classmethod
    def from_file(cls, patient_id: str, file_path: str):
        """Crea una instancia de ChestXray desde un archivo"""
        try:
            if file_path.lower().endswith('.dcm'):
                # Lectura de archivo DICOM
                img = pydicom.dcmread(file_path)
                img_array = img.pixel_array
                img2 = img_array.astype(float)
                img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
                img2 = np.uint8(img2)
                img_array = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
                image_type = 'DICOM'
            else:
                # Lectura de archivo JPG/PNG
                img_array = cv2.imread(file_path)
                if img_array is None:
                    raise ValueError("No se pudo leer la imagen")
                image_type = 'JPG'

            return cls(
                patient_id=patient_id,
                image_array=img_array,
                image_type=image_type
            )
        except Exception as e:
            raise ValueError(f"Error al leer la imagen: {str(e)}")

    def to_pil_image(self) -> Image.Image:
        """Convierte el array de la imagen a formato PIL Image"""
        return Image.fromarray(self.image_array)

