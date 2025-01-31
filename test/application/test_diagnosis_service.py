import pytest
from unittest.mock import Mock, patch
import numpy as np
from domain.entities.chest_xray import ChestXray
from domain.entities.diagnosis_result import DiagnosisResult
from application.services.diagnosis_service import DiagnosisService

# Fixtures para configurar el ambiente de pruebas
@pytest.fixture
def mock_model_service():
    mock = Mock()
    # Configurar el comportamiento esperado
    mock.predict.return_value = ("PNEUMONIA", 0.95, np.zeros((224, 224)))
    return mock

@pytest.fixture
def mock_image_processor():
    mock = Mock()
    # Configurar el comportamiento esperado
    mock.preprocess.return_value = np.zeros((224, 224, 3))
    return mock

@pytest.fixture
def diagnosis_service(mock_model_service, mock_image_processor):
    return DiagnosisService(
        model_service=mock_model_service,
        image_processor=mock_image_processor
    )

# Pruebas
def test_create_diagnosis_successful(diagnosis_service):
    # Arrange
    test_image = np.zeros((500, 500, 3))
    test_xray = ChestXray(
        patient_id="TEST123",
        image_array=test_image
    )

    # Act
    result = diagnosis_service.create_diagnosis(test_xray)

    # Assert
    assert isinstance(result, DiagnosisResult)
    assert result.patient_id == "TEST123"
    assert result.prediction_type == "PNEUMONIA"
    assert result.probability == 0.95
    assert isinstance(result.id, str)  # Verificar que se generó un UUID
    
def test_create_diagnosis_processor_error(diagnosis_service, mock_image_processor):
    # Arrange
    mock_image_processor.preprocess.side_effect = Exception("Error de procesamiento")
    test_image = np.zeros((500, 500, 3))
    test_xray = ChestXray(
        patient_id="TEST123",
        image_array=test_image
    )

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        diagnosis_service.create_diagnosis(test_xray)
    assert "Error en el diagnóstico" in str(exc_info.value)

def test_create_diagnosis_model_error(diagnosis_service, mock_model_service):
    # Arrange
    mock_model_service.predict.side_effect = Exception("Error de predicción")
    test_image = np.zeros((500, 500, 3))
    test_xray = ChestXray(
        patient_id="TEST123",
        image_array=test_image
    )

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        diagnosis_service.create_diagnosis(test_xray)
    assert "Error en el diagnóstico" in str(exc_info.value)

def test_diagnosis_result_contains_heatmap(diagnosis_service):
    # Arrange
    test_image = np.zeros((500, 500, 3))
    test_xray = ChestXray(
        patient_id="TEST123",
        image_array=test_image
    )

    # Act
    result = diagnosis_service.create_diagnosis(test_xray)

    # Assert
    assert result.heatmap is not None
    assert isinstance(result.heatmap, np.ndarray)