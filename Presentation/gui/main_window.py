import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui
import tkcap
import img2pdf
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
import os

class PneumoniaDetectorGUI:
    def __init__(self, diagnosis_service):
        self.root = tk.Tk()
        self.diagnosis_service = diagnosis_service
        self._setup_gui()
        self.report_counter = 0

    def _setup_gui(self):
        """Configuración de la interfaz gráfica usando Tkinter"""
        self.root.title("Detector de Neumonía")
        self.root.geometry("815x560")
        self.root.resizable(0, 0)
        
        # Configurar widgets principales
        self._setup_labels()
        self._setup_inputs()
        self._setup_buttons()
        self._setup_displays()

    def save_to_csv(self):
        """Guarda resultados usando pandas 1.3.3"""
        try:
            data = {
                'patient_id': [self.patient_id_var.get()],
                'diagnosis': [self.current_diagnosis],
                'probability': [self.current_probability],
                'timestamp': [datetime.now()]
            }
            df = pd.DataFrame(data)
            df.to_csv('historial.csv', mode='a', header=not os.path.exists('historial.csv'), index=False)
            tk.messagebox.showinfo("Éxito", "Datos guardados correctamente")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def generate_pdf(self):
        """Genera PDF usando tkcap 0.0.4 y img2pdf 0.4.1"""
        try:
            # Capturar pantalla
            cap = tkcap.CAP(self.root)
            img_path = f"reporte_{self.report_counter}.jpg"
            cap.capture(img_path)
            
            # Convertir a PDF
            with open(f"reporte_{self.report_counter}.pdf", "wb") as pdf_file:
                img = Image.open(img_path)
                img = img.convert('RGB')
                pdf_bytes = img2pdf.convert(img_path)
                pdf_file.write(pdf_bytes)
            
            self.report_counter += 1
            os.remove(img_path)  # Limpiar archivo temporal
            tk.messagebox.showinfo("Éxito", "PDF generado correctamente")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")

if __name__ == "__main__":
    from infrastructure.ml.cnn_model import PneumoniaCNN
    from infrastructure.image.dicom_reader import DicomReader
    
    # Inicializar servicios
    model = PneumoniaCNN('conv_MLP_84.h5')
    reader = DicomReader()
    
    # Crear y ejecutar GUI
    app = PneumoniaDetectorGUI(model)
    app.run()

    # main.py
def main():
    # Configurar servicios
    model = PneumoniaCNN('conv_MLP_84.h5')
    preprocessor = XrayPreprocessor()
    diagnosis_service = DiagnosisService(model, preprocessor)
    
    # Iniciar GUI
    app = PneumoniaDetectorGUI(diagnosis_service)
    app.run()

if __name__ == "__main__":
    main()