import tensorflow as tf
import numpy as np
import cv2
from typing import Tuple, Dict

class PneumoniaCNN:
    def __init__(self, model_path: str):
        # Configuración específica para TensorFlow 2.4.0
        tf.compat.v1.disable_eager_execution()
        tf.compat.v1.experimental.output_all_intermediates(True)
        
        self.model = self._load_model(model_path)
        self.labels: Dict[int, str] = {
            0: "bacteriana",
            1: "normal",
            2: "viral"
        }

    def _load_model(self, model_path: str) -> tf.keras.Model:
        try:
            # Cargar modelo con TensorFlow 2.4.0
            model = tf.keras.models.load_model(model_path, compile=False)
            model.compile(
                optimizer='adam',
                loss=tf.keras.losses.CategoricalCrossentropy(reduction='sum'),
                metrics=['accuracy']
            )
            return model
        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo: {str(e)}")

    def predict_with_gradcam(self, preprocessed_image: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """
        Realiza la predicción y genera el Grad-CAM
        Adaptado para TensorFlow 2.4.0
        """
        # Predicción
        predictions = self.model.predict(preprocessed_image)
        prediction_index = np.argmax(predictions[0])
        probability = float(np.max(predictions[0]) * 100)
        
        # Generar Grad-CAM usando TF 2.4.0
        last_conv_layer = self.model.get_layer("conv10_thisone")
        grad_model = tf.keras.Model(
            [self.model.inputs],
            [last_conv_layer.output, self.model.output]
        )
        
        with tf.GradientTape() as tape:
            conv_output, predictions = grad_model(preprocessed_image)
            loss = predictions[:, prediction_index]
            
        grads = tape.gradient(loss, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        conv_output = conv_output[0]
        for i in range(pooled_grads.shape[-1]):
            conv_output[:, :, i] *= pooled_grads[i]
            
        heatmap = tf.reduce_mean(conv_output, axis=-1)
        heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        
        # Procesar heatmap para visualización
        heatmap = cv2.resize(heatmap, (512, 512))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        return self.labels[prediction_index], probability, heatmap
