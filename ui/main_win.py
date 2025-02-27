import os
import platform
import subprocess
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from ui.window import Ui_MainWindow  # Asegúrate de que el nombre y ubicación sean correctos
from controllers.file_controller import leer_csv_desde_fila_11, procesar_zip_a_dataframe
from controllers.process_controller import procesar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Conectar botones a sus funciones
        self.ui.pushButton.clicked.connect(self.select_zip)
        self.ui.pushButton_2.clicked.connect(self.select_csv)
        self.ui.pushButton_destination.clicked.connect(self.select_destination)
        self.ui.pushButton_3.clicked.connect(self.process_files)
        
        # Variables para almacenar rutas de archivos
        self.zip_path = None
        self.csv_path = None
        self.dest_path = None

    def select_zip(self):
        self.zip_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo ZIP",
            "",
            "Archivos ZIP (*.zip);;Todos los archivos (*)"
        )
        if self.zip_path:
            self.ui.lineEdit.setText(self.zip_path)
    
    def select_csv(self):
        self.csv_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo CSV",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        if self.csv_path:
            self.ui.lineEdit_2.setText(self.csv_path)
    
    def select_destination(self):
        self.dest_path, _ = QFileDialog.getSaveFileName(
            self,
            "Seleccionar destino para el archivo procesado",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*)"
        )
        if self.dest_path:
            self.ui.lineEdit_destination.setText(self.dest_path)
    
    def process_files(self):
        if not self.zip_path or not self.csv_path or not self.dest_path:
            QMessageBox.warning(self, "Error", "Debes seleccionar el archivo ZIP, el CSV y el destino para el resultado.")
            return
        
        try:
            dataframes_zip = procesar_zip_a_dataframe(self.zip_path)
            df_csv = leer_csv_desde_fila_11(self.csv_path)
            # Procesar y guardar el archivo en la ruta destino seleccionada
            procesar(dataframes_zip, df_csv, self.dest_path)
            QMessageBox.information(self, "Proceso finalizado", "El procesamiento se realizó correctamente.")
            
            # Abrir la carpeta que contiene el archivo procesado
            folder = os.path.dirname(self.dest_path)
            self.open_folder(folder)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error: {str(e)}")
    
    def open_folder(self, path):
        """Abre la carpeta especificada según el sistema operativo."""
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux y otros
            subprocess.Popen(["xdg-open", path])
