import tensorflow as tf
import numpy as np
import cv2
from typing import Tuple, Dict

class PneumoniaCNN:
    def __init__(self, model_path: str):
        """ Inicializa la clase cargando el modelo preentrenado """
        self.model = self._load_model(model_path)
        self.labels: Dict[int, str] = {
            0: "bacteriana",
            1: "normal",
            2: "viral"
        }

    def predict(self, preprocessed_image: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """ Alias para llamar a predict_with_gradcam como predict """
        return self.predict_with_gradcam(preprocessed_image)

    def _load_model(self, model_path: str) -> tf.keras.Model:
        """ Carga el modelo de clasificación de neumonía """
        try:
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
        Realiza la predicción y genera el Grad-CAM mejorado.
        """
        # ✅ Paso 1: Predicción
        predictions = self.model.predict(preprocessed_image)
        prediction_index = np.argmax(predictions[0])
        probability = float(np.max(predictions[0]) * 100)

        # ✅ Paso 2: Obtener capa convolucional final
        last_conv_layer = self.model.get_layer("conv10_thisone")
        grad_model = tf.keras.Model(
            [self.model.inputs],
            [last_conv_layer.output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_output, predictions = grad_model(preprocessed_image)
            loss = predictions[:, prediction_index]

        # ✅ Paso 3: Calcular gradientes
        grads = tape.gradient(loss, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_output = conv_output[0].numpy()
        pooled_grads = pooled_grads.numpy()

        # ✅ Paso 4: Aplicar gradientes a los filtros
        for i in range(pooled_grads.shape[-1]):
            conv_output[:, :, i] *= pooled_grads[i]

        heatmap = np.mean(conv_output, axis=-1)
        heatmap = np.maximum(heatmap, 0)  # ReLU
        heatmap /= np.max(heatmap)  # Normalización

        # ✅ Paso 5: Convertir `heatmap` a formato `uint8` antes de OpenCV
        heatmap = cv2.resize(heatmap, (512, 512))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # ✅ Paso 6: Convertir `preprocessed_image` a `uint8`
        original_img = preprocessed_image[0]  # Extraer imagen del batch
        original_img = (original_img * 255).astype(np.uint8)  # Convertir a uint8
        original_img = cv2.cvtColor(original_img, cv2.COLOR_GRAY2RGB)
        original_img = cv2.resize(original_img, (512, 512))

        # ✅ Paso 7: Fusionar `heatmap` con la imagen original con mejor transparencia
        alpha = 0.6  # 🔥 Ajusta la transparencia del heatmap
        beta = 1 - alpha
        superimposed_img = cv2.addWeighted(original_img, beta, heatmap, alpha, 0)

        return self.labels[prediction_index], probability, superimposed_img
