import pytest
import numpy as np
from unittest.mock import patch, Mock
from datetime import datetime
from PIL import Image
import cv2
from domain.entities.chest_xray import ChestXray

@pytest.fixture
def sample_dicom_array():
    # Crear un array de prueba que simula una imagen DICOM
    return np.random.randint(0, 4096, (100, 100), dtype=np.uint16)

@pytest.fixture
def sample_jpg_array():
    # Crear un array de prueba que simula una imagen JPG
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

def test_chest_xray_creation():
    # Arrange
    patient_id = "TEST123"
    image_array = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Act
    xray = ChestXray(
        patient_id=patient_id,
        image_array=image_array,
        image_type='JPG'
    )
    
    # Assert
    assert xray.patient_id == patient_id
    assert np.array_equal(xray.image_array, image_array)
    assert xray.image_type == 'JPG'
    assert isinstance(xray.created_at, datetime)

@patch('pydicom.dcmread')
@patch('cv2.cvtColor')
def test_from_file_dicom(mock_cvtColor, mock_dcmread, sample_dicom_array):
    # Arrange
    mock_dicom = Mock()
    mock_dicom.pixel_array = sample_dicom_array
    mock_dcmread.return_value = mock_dicom
    mock_cvtColor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Act
    xray = ChestXray.from_file("TEST123", "test.dcm")
    
    # Assert
    assert xray.patient_id == "TEST123"
    assert xray.image_type == "DICOM"
    mock_dcmread.assert_called_once_with("test.dcm")
    mock_cvtColor.assert_called_once()

@patch('cv2.imread')
def test_from_file_jpg(mock_imread, sample_jpg_array):
    # Arrange
    mock_imread.return_value = sample_jpg_array
    
    # Act
    xray = ChestXray.from_file("TEST123", "test.jpg")
    
    # Assert
    assert xray.patient_id == "TEST123"
    assert xray.image_type == "JPG"
    assert np.array_equal(xray.image_array, sample_jpg_array)
    mock_imread.assert_called_once_with("test.jpg")

def test_from_file_invalid_jpg():
    # Arrange
    with patch('cv2.imread') as mock_imread:
        mock_imread.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ChestXray.from_file("TEST123", "invalid.jpg")
        assert "No se pudo leer la imagen" in str(exc_info.value)

@patch('pydicom.dcmread')
def test_from_file_invalid_dicom(mock_dcmread):
    # Arrange
    mock_dcmread.side_effect = Exception("Error de lectura DICOM")
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        ChestXray.from_file("TEST123", "invalid.dcm")
    assert "Error al leer la imagen" in str(exc_info.value)

def test_to_pil_image():
    # Arrange
    image_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    xray = ChestXray(
        patient_id="TEST123",
        image_array=image_array,
        image_type="JPG"
    )
    
    # Act
    pil_image = xray.to_pil_image()
    
    # Assert
    assert isinstance(pil_image, Image.Image)
    assert pil_image.size == (100, 100)
    assert np.array_equal(np.array(pil_image), image_array)