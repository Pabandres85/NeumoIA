from domain.entities.chest_xray import ChestXray, DiagnosisResult
from domain.interfaces.model_service import ModelService
from domain.interfaces.image_processor import ImageProcessor

class DiagnosisService:
    def __init__(
        self,
        model_service: ModelService,
        image_processor: ImageProcessor
    ):
        self._model_service = model_service
        self._image_processor = image_processor

    def create_diagnosis(self, xray: ChestXray) -> DiagnosisResult:
        # Preprocesar imagen
        preprocessed_image = self._image_processor.preprocess(xray.image_array)
        
        # Obtener predicción y heatmap
        diagnosis, probability, heatmap = self._model_service.predict(preprocessed_image)
        
        # Crear resultado
        return DiagnosisResult(
            patient_id=xray.patient_id,
            diagnosis=diagnosis,
            probability=probability,
            heatmap=heatmap
        )