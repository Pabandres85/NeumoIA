from abc import ABC, abstractmethod
import numpy as np

class ImageProcessor(ABC):
    @abstractmethod
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocesa la imagen para el modelo"""
        pass