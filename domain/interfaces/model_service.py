from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple

class ModelService(ABC):
    @abstractmethod
    def predict(self, preprocessed_image: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """Realiza la predicción y genera el heatmap"""
        pass