import tkinter as tk
from tkinter import filedialog
from controllers.file_controller import leer_csv_desde_fila_11, procesar_zip_a_dataframe  # Ajusta el import al nombre de tu módulo o archivo
from controllers.process_controller import procesar
def main():
    # Crear la ventana raíz de Tkinter (oculta)
    root = tk.Tk()
    root.withdraw()

    # --- Seleccionar y procesar el archivo ZIP ---
    zip_path = filedialog.askopenfilename(
        title="Seleccionar archivo ZIP",
        filetypes=[("Archivos ZIP", "*.zip"), ("Todos los archivos", "*.*")]
    )

    if not zip_path:
        print("No se seleccionó ningún archivo ZIP.")
    else:
        dataframes_zip = procesar_zip_a_dataframe(zip_path)


    # --- Seleccionar y procesar el archivo CSV ---
    csv_path = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )

    if not csv_path:
        print("No se seleccionó ningún archivo CSV.")
    else:
        df_csv = leer_csv_desde_fila_11(csv_path)

    procesar(dataframes_zip, df_csv)

    # Cerrar la ventana raíz
    root.destroy()

if __name__ == "__main__":
    main()