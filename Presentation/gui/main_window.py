import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from PIL import Image, ImageTk
import cv2
import numpy as np
from application.services.diagnosis_service import DiagnosisService
from domain.entities.chest_xray import ChestXray
import tkcap
import csv
from datetime import datetime

class PneumoniaDetectorGUI:
    def __init__(self, diagnosis_service: DiagnosisService):
        """Inicializa la interfaz gráfica del detector de neumonía"""
        self._diagnosis_service = diagnosis_service
        self.root = tk.Tk()
        self.current_image = None
        self.report_counter = 0
        self._setup_gui()

    def _setup_gui(self):
        """Configura todos los elementos de la interfaz gráfica"""
        self.root.title("Herramienta para la detección rápida de neumonía")
        self.root.geometry("815x560")
        self.root.resizable(0, 0)
        
        # Configurar fuentes y estilos
        self._setup_styles()
        
        # Configurar todos los elementos
        self._setup_labels()
        self._setup_entries()
        self._setup_image_displays()
        self._setup_buttons()
        
        # Configurar layout
        self._setup_layout()

    def _setup_styles(self):
        """Configura los estilos y fuentes de la interfaz"""
        self.bold_font = font.Font(weight="bold")

    def _setup_labels(self):
        """Configura las etiquetas de la interfaz"""
        self.labels = {
            'title': ttk.Label(
                self.root,
                text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
                font=self.bold_font
            ),
            'xray': ttk.Label(
                self.root,
                text="Imagen Radiográfica",
                font=self.bold_font
            ),
            'heatmap': ttk.Label(
                self.root,
                text="Imagen con Heatmap",
                font=self.bold_font
            ),
            'result': ttk.Label(
                self.root,
                text="Resultado:",
                font=self.bold_font
            ),
            'patient_id': ttk.Label(
                self.root,
                text="Cédula Paciente:",
                font=self.bold_font
            ),
            'probability': ttk.Label(
                self.root,
                text="Probabilidad:",
                font=self.bold_font
            )
        }

    def _setup_entries(self):
        """Configura los campos de entrada"""
        # Variables de control
        self.patient_id_var = tk.StringVar()
        
        # Campos de entrada
        self.patient_id_entry = ttk.Entry(
            self.root,
            textvariable=self.patient_id_var,
            width=10
        )
        
        # Campos de texto para resultados
        self.result_text = tk.Text(self.root, width=10, height=1)
        self.probability_text = tk.Text(self.root, width=10, height=1)

    def _setup_image_displays(self):
        """Configura las áreas de visualización de imágenes"""
        self.xray_display = tk.Text(self.root, width=31, height=15)
        self.heatmap_display = tk.Text(self.root, width=31, height=15)

    def _setup_buttons(self):
        """Configura los botones de la interfaz"""
        self.buttons = {
            'load': ttk.Button(
                self.root,
                text="Cargar Imagen",
                command=self._load_image
            ),
            'predict': ttk.Button(
                self.root,
                text="Predecir",
                command=self._predict,
                state="disabled"
            ),
            'save': ttk.Button(
                self.root,
                text="Guardar",
                command=self._save_results
            ),
            'pdf': ttk.Button(
                self.root,
                text="PDF",
                command=self._generate_pdf
            ),
            'clear': ttk.Button(
                self.root,
                text="Borrar",
                command=self._clear_form
            )
        }

    def _setup_layout(self):
        """Configura la disposición de los elementos en la interfaz"""
        # Posicionar etiquetas
        self.labels['title'].place(x=122, y=25)
        self.labels['xray'].place(x=110, y=65)
        self.labels['heatmap'].place(x=545, y=65)
        self.labels['result'].place(x=500, y=350)
        self.labels['patient_id'].place(x=65, y=350)
        self.labels['probability'].place(x=500, y=400)
        
        # Posicionar campos de entrada y texto
        self.patient_id_entry.place(x=200, y=350)
        self.result_text.place(x=610, y=350, width=90, height=30)
        self.probability_text.place(x=610, y=400, width=90, height=30)
        
        # Posicionar áreas de imagen
        self.xray_display.place(x=65, y=90)
        self.heatmap_display.place(x=500, y=90)
        
        # Posicionar botones
        self.buttons['load'].place(x=70, y=460)
        self.buttons['predict'].place(x=220, y=460)
        self.buttons['save'].place(x=370, y=460)
        self.buttons['pdf'].place(x=520, y=460)
        self.buttons['clear'].place(x=670, y=460)

    def _load_image(self):
        """Maneja la carga de imágenes"""
        try:
            # Verificar ID del paciente
            if not self.patient_id_var.get().strip():
                messagebox.showwarning("Advertencia", "Por favor, ingrese la cédula del paciente")
                return

            # Seleccionar archivo
            filepath = filedialog.askopenfilename(
                initialdir="/",
                title="Seleccionar imagen",
                filetypes=(
                    ("DICOM", "*.dcm"),
                    ("JPEG", "*.jpeg"),
                    ("jpg files", "*.jpg"),
                    ("png files", "*.png"),
                )
            )

            if filepath:
                # Crear objeto ChestXray
                self.current_image = ChestXray.from_file(
                    patient_id=self.patient_id_var.get(),
                    file_path=filepath
                )
                
                # Mostrar imagen en la interfaz
                img_pil = self.current_image.to_pil_image()
                img_pil = img_pil.resize((250, 250), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(img_pil)
                
                # Limpiar display anterior
                self.xray_display.delete("1.0", tk.END)
                
                # Insertar nueva imagen
                self.xray_display.image_create(tk.END, image=img_tk)
                self.xray_display.image = img_tk  # Mantener referencia
                
                # Habilitar botón de predicción
                self.buttons['predict']['state'] = 'normal'

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging

    def _predict(self):
        """Realiza la predicción de la imagen"""
        if not self.current_image:
            messagebox.showwarning("Advertencia", "Por favor, cargue una imagen primero.")
            return
            
        try:
            # Obtener diagnóstico
            result = self._diagnosis_service.create_diagnosis(self.current_image)
            
            # Mostrar resultados
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result.prediction_type.value)
            
            self.probability_text.delete(1.0, tk.END)
            self.probability_text.insert(tk.END, f"{result.probability:.2f}%")
            
            # Mostrar heatmap
            heatmap_pil = Image.fromarray(result.heatmap)
            heatmap_pil = heatmap_pil.resize((250, 250), Image.ANTIALIAS)
            heatmap_tk = ImageTk.PhotoImage(heatmap_pil)
            
            self.heatmap_display.delete(1.0, tk.END)
            self.heatmap_display.image_create(tk.END, image=heatmap_tk)
            self.heatmap_display.image = heatmap_tk  # Mantener referencia
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la predicción: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debugging

    def _save_results(self):
        """Guarda los resultados en un archivo CSV"""
        try:
            if not self.current_image:
                messagebox.showwarning("Advertencia", "No hay resultados para guardar.")
                return

            with open("historial.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter="-")
                writer.writerow([
                    self.patient_id_var.get(),
                    self.result_text.get("1.0", tk.END).strip(),
                    self.probability_text.get("1.0", tk.END).strip(),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
            
            messagebox.showinfo("Éxito", "Los datos se guardaron correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {str(e)}")

    def _generate_pdf(self):
        """Genera un reporte en formato PDF"""
        try:
            if not self.current_image:
                messagebox.showwarning("Advertencia", "No hay resultados para generar PDF.")
                return

            # Capturar la ventana
            cap = tkcap.CAP(self.root)
            image_path = f"Reporte{self.report_counter}.jpg"
            cap.capture(image_path)
            
            # Convertir a PDF
            img = Image.open(image_path)
            img = img.convert('RGB')
            pdf_path = f"Reporte{self.report_counter}.pdf"
            img.save(pdf_path)
            
            self.report_counter += 1
            messagebox.showinfo("Éxito", "El PDF fue generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")

    def _clear_form(self):
        """Limpia todos los campos del formulario"""
        if messagebox.askokcancel("Confirmar", "¿Desea borrar todos los datos?"):
            try:
                # Limpiar campos de texto
                self.patient_id_var.set("")
                self.result_text.delete(1.0, tk.END)
                self.probability_text.delete(1.0, tk.END)
                
                # Limpiar imágenes
                self.xray_display.delete(1.0, tk.END)
                self.heatmap_display.delete(1.0, tk.END)
                
                # Restablecer estado
                self.current_image = None
                self.buttons['predict']['state'] = 'disabled'
                
                messagebox.showinfo("Éxito", "Los datos se borraron correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al borrar los datos: {str(e)}")

    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()