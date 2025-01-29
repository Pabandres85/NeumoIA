import uuid
from domain.entities.chest_xray import ChestXray
from domain.entities.diagnosis_result import DiagnosisResult
from domain.interfaces.model_service import ModelService
from domain.interfaces.image_processor import ImageProcessor

class DiagnosisService:
    """Servicio para realizar diagnósticos de neumonía"""
    
    def __init__(
        self,
        model_service: ModelService,
        image_processor: ImageProcessor
    ):
        self._model_service = model_service
        self._image_processor = image_processor

    def create_diagnosis(self, xray: ChestXray) -> DiagnosisResult:
        try:
            # Preprocesar imagen
            preprocessed_image = self._image_processor.preprocess(xray.image_array)
            
            # Obtener predicción
            diagnosis, probability, heatmap = self._model_service.predict(preprocessed_image)
            
            # Crear resultado
            return DiagnosisResult(
            id=str(uuid.uuid4()),  # ✅ Generar un identificador único
            patient_id=xray.patient_id,
            prediction_type=diagnosis,
            probability=probability,
            heatmap=heatmap
)
        except Exception as e:
            raise Exception(f"Error en el diagnóstico: {str(e)}")