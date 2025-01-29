from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np
from enum import Enum

class PneumoniaType(Enum):
    """Tipos posibles de neumonía"""
    BACTERIAL = "bacteriana"
    VIRAL = "viral"
    NORMAL = "normal"

@dataclass
class DiagnosisResult:
    """
    Entidad que representa el resultado de un diagnóstico de neumonía.

    Attributes:
        id (str): Identificador único del diagnóstico
        patient_id (str): Identificador del paciente
        prediction_type (PneumoniaType): Tipo de neumonía detectada
        probability (float): Probabilidad de la predicción (0-100)
        heatmap (np.ndarray): Mapa de calor generado por Grad-CAM
        created_at (datetime): Fecha y hora del diagnóstico
        notes (Optional[str]): Notas adicionales del diagnóstico
    """
    id: str
    patient_id: str
    prediction_type: PneumoniaType
    probability: float
    heatmap: np.ndarray
    created_at: datetime = datetime.now()
    notes: Optional[str] = None

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not 0 <= self.probability <= 100:
            raise ValueError("La probabilidad debe estar entre 0 y 100")
        
        if not isinstance(self.prediction_type, PneumoniaType):
            if isinstance(self.prediction_type, str):
                try:
                    # Intenta convertir string a enum
                    self.prediction_type = PneumoniaType(self.prediction_type.lower())
                except ValueError:
                    raise ValueError(f"Tipo de predicción no válido: {self.prediction_type}")
            else:
                raise ValueError("prediction_type debe ser de tipo PneumoniaType")

    @property
    def is_pneumonia(self) -> bool:
        """Indica si se detectó neumonía"""
        return self.prediction_type != PneumoniaType.NORMAL

    @property
    def confidence_level(self) -> str:
        """Retorna el nivel de confianza basado en la probabilidad"""
        if self.probability >= 90:
            return "Muy Alta"
        elif self.probability >= 75:
            return "Alta"
        elif self.probability >= 60:
            return "Media"
        else:
            return "Baja"

    def to_dict(self) -> dict:
        """Convierte el resultado a diccionario para almacenamiento/serialización"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'prediction_type': self.prediction_type.value,
            'probability': self.probability,
            'confidence_level': self.confidence_level,
            'is_pneumonia': self.is_pneumonia,
            'created_at': self.created_at.isoformat(),
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DiagnosisResult':
        """Crea una instancia desde un diccionario"""
        # Convertir string ISO a datetime
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        
        # Asegurar que prediction_type sea un enum
        if isinstance(data['prediction_type'], str):
            data['prediction_type'] = PneumoniaType(data['prediction_type'])

        return cls(**data)

    def add_note(self, note: str) -> None:
        """Agrega una nota al diagnóstico"""
        if self.notes:
            self.notes += f"\n{note}"
        else:
            self.notes = note

    def get_summary(self) -> str:
        """Retorna un resumen del diagnóstico"""
        status = "NEUMONÍA DETECTADA" if self.is_pneumonia else "NO SE DETECTÓ NEUMONÍA"
        return (
            f"RESULTADO DEL DIAGNÓSTICO\n"
            f"------------------------\n"
            f"Status: {status}\n"
            f"Tipo: {self.prediction_type.value}\n"
            f"Probabilidad: {self.probability:.1f}%\n"
            f"Nivel de Confianza: {self.confidence_level}\n"
            f"Fecha: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Notas: {self.notes if self.notes else 'Sin notas adicionales'}"
        )