from dataclasses import dataclass
import numpy as np
from datetime import datetime

@dataclass
class ChestXray:
    """Entidad que representa una imagen de rayos X de tórax"""
    patient_id: str
    image_array: np.ndarray
    image_type: str  # 'DICOM' or 'JPG'
    created_at: datetime = datetime.now()

@dataclass
class DiagnosisResult:
    """Entidad que representa el resultado del diagnóstico"""
    patient_id: str
    diagnosis: str  # 'bacterial', 'viral', 'normal'
    probability: float
    heatmap: np.ndarray
    created_at: datetime = datetime.now()

