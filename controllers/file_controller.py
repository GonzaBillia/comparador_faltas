import os
import re
import zipfile
import tempfile
import pandas as pd
from services.comparador import roman_to_int

def parse_sucursal(destino_str: str) -> int:
    """
    Toma un string como 'S. ANTONIOLLI II' y devuelve un entero (2 en este caso).
    Si no encuentra un número romano, retorna None (ajusta según prefieras).
    """
    pattern = re.compile(r'([IVXLCDM]+)$', re.IGNORECASE)
    match = pattern.search(destino_str.strip())
    if match:
        roman_part = match.group(1)
        return roman_to_int(roman_part)
    return None

def procesar_zip_a_dataframe(zip_path):
    """
    Procesa un archivo ZIP extrayendo sus archivos .txt y generando un único DataFrame
    con la información de todos los archivos, incluyendo la sucursal extraída del nombre.

    Retorna:
        pd.DataFrame: DataFrame con todas las filas de todos los TXT.
    """
    # DataFrame vacío donde iremos concatenando
    df_final = pd.DataFrame()

    with tempfile.TemporaryDirectory() as extract_path:
        # Descomprimir el ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Recorrer cada archivo extraído
        for filename in os.listdir(extract_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(extract_path, filename)

                # Extraer sucursal y fecha del nombre del archivo
                match = re.search(r"Suc\. (\d+).*Fecha (\d{8})", filename)
                if not match:
                    raise ValueError(f"No se pudo extraer sucursal/fecha del nombre: {filename}")

                sucursal = match.group(1)
                raw_fecha = match.group(2)

                # Ajustar sucursal si es 32, 33, 34
                if sucursal == '32':
                    sucursal = '26'
                elif sucursal == '34':
                    sucursal = '27'
                elif sucursal == '33':
                    sucursal = '28'

                # Formato de fecha YYYY/MM/DD (si necesitas usarla)
                fecha_envio = f"{raw_fecha[:4]}/{raw_fecha[4:6]}/{raw_fecha[6:8]}"

                # Leer el contenido del archivo TXT
                # Ajusta encoding si tus archivos no son utf-8
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # Procesar líneas (slicing fijo)
                data = []
                for line in lines:
                    codebar = line[:13].strip()
                    troquel = line[13:20].strip()
                    descripcion = line[20:50].strip()
                    cantidad = line[50:].strip()
                    data.append([codebar, troquel, descripcion, cantidad])

                # Crear DataFrame para este archivo
                df_temp = pd.DataFrame(data, columns=[
                    'Codebar', 'Troquel', 'Descripción', 'Cantidad'
                ])
                # Añadir sucursal y fecha
                df_temp['Sucursal'] = sucursal
                df_temp['Fecha_Envio'] = fecha_envio

                # Renombrar columnas a las definitivas que usarás para el merge
                df_temp.rename(columns={
                    'Codebar': 'CODBARRA',
                    'Troquel': 'TROQUEL',
                    'Descripción': 'DESCRIPCION',
                    'Cantidad': 'CANTIDAD_PEDIDA',
                    'Sucursal': 'SUCURSAL'
                }, inplace=True)

                # Concatenar al df_final
                df_final = pd.concat([df_final, df_temp], ignore_index=True)

    return df_final


def leer_csv_desde_fila_11(ruta_csv):
    """
    Lee un CSV donde la tabla principal empieza en la fila 11 (cabecera incluida).
    Retorna un DataFrame con las columnas renombradas y la sucursal convertida a entero.
    """
    # Ajusta sep, decimal, encoding según tu archivo
    df = pd.read_csv(
        ruta_csv,
        skiprows=10,      # Omitir las primeras 10 filas
        sep=';',          # Si tu archivo está separado por ';'
        decimal=',',      # Si tus números usan coma como decimal
        encoding='latin-1'
    )

    # Renombrar columnas a algo uniforme
    # Ajusta según las columnas reales de tu CSV
    df.rename(columns={
        'Operación': 'OPERACION',
        'Número': 'NUMERO_ENVIO',
        'Estado': 'ESTADO_LLEGADA',
        'Origen': 'ORIGEN',
        'Destino': 'SUCURSAL',
        'Fecha Envio': 'FECHA_ENVIO',
        'Fecha Recepcion': 'FECHA_RECEPCION',
        'Operador Envio': 'OPERADOR_ENVIO',
        'Operador Recepcion': 'OPERADOR_RECEPCION',
        'Troquel': 'TROQUEL',
        'Producto': 'DESCRIPCION_LLEGADA',
        'Cantidad': 'CANTIDAD_ENVIADA',
        'Unidades': 'UNIDADES_ENVIADAS',
        'CantidadRecibida': 'CANTIDAD_RECIBIDA',
        'UnidadesRecibidas': 'UNIDADES_RECIBIDAS',
        'Importe': 'IMPORTE'
    }, inplace=True)

    # Parsear fechas (si las columnas existen)
    if 'FECHA_ENVIO' in df.columns:
        df['FECHA_ENVIO'] = pd.to_datetime(df['FECHA_ENVIO'], dayfirst=True, errors='coerce')
    if 'FECHA_RECEPCION' in df.columns:
        df['FECHA_RECEPCION'] = pd.to_datetime(df['FECHA_RECEPCION'], dayfirst=True, errors='coerce')

    # Convertir la sucursal (ej. "S. ANTONIOLLI II") a entero
    # Ajusta la lógica si tu texto difiere
    df['SUCURSAL'] = df['SUCURSAL'].astype(str).apply(parse_sucursal)

    return df


def leer_llegadas_csv(ruta_csv):
    """
    Lee el CSV de la primera tabla (lo que llegó).
    Retorna un DataFrame con algunas columnas renombradas
    para unificar criterios.
    """
    # Ajusta 'sep', 'decimal', 'encoding' según corresponda a tu archivo
    df = pd.read_csv(
        ruta_csv,
        sep=';',       # Ej: si tu CSV está separado por comas
        decimal=',',   # Ej: si los decimales usan punto
        encoding='latin1',  # O 'utf-8' si aplica
        parse_dates=['Fecha Envio', 'Fecha Recepcion'],  # Convierte a datetime
        dayfirst=True,  # Interpreta día/mes/año
        # ... si tus columnas no calzan exactamente, omite o añade parámetros
    )
    
    # Renombramos columnas para unificar con la segunda tabla
    df.rename(columns={
        'Troquel': 'TROQUEL',
        'Cantidad': 'CANTIDADES_ENVIADAS',
        'Destino': 'SUCURSAL',
        'Número': 'NUMERO_DE_ENVIO',
        'Fecha Envio': 'FECHA_DE_ENVIO',
        'Fecha Recepcion': 'FECHA_RECEPCION',
        'Producto': 'DESCRIPCION_1',  # por si luego prefieres la descripción del 2do CSV
    }, inplace=True)

    return df

def export_excel_with_style(df, output_path):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Reporte')
    workbook  = writer.book
    worksheet = writer.sheets['Reporte']
    
    # Autoajuste de columnas basado en el contenido
    for i, col in enumerate(df.columns):
        column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, column_len)
        
    last_row = len(df) + 1  # considerando que la fila 1 es el header

    # Definir formatos para cada estado (colores claros)
    complete_format   = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    incomplete_format = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C5700'})
    error_format      = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    
    # Formato para marcar la celda de "CANTIDAD ENVIADA" con borde
    border_format = workbook.add_format({'border': 2})
    
    # Aplicar formato condicional a las filas completas (asumiendo que la columna ESTADO es la K)
    worksheet.conditional_format(f'A2:K{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="COMPLETO"',
        'format': complete_format
    })
    worksheet.conditional_format(f'A2:K{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="INCOMPLETO"',
        'format': incomplete_format
    })
    worksheet.conditional_format(f'A2:K{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="ERRONEO"',
        'format': error_format
    })
    worksheet.conditional_format(f'A2:K{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="NO PEDIDO"',
        'format': error_format
    })
    worksheet.conditional_format(f'A2:K{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="NO ENVIADO"',
        'format': error_format
    })
    
    worksheet.conditional_format(f'F2:F{last_row}', {
        'type': 'formula',
        'criteria': '=OR($K2="INCOMPLETO", $K2="ERRONEO")',
        'format': border_format
    })

    worksheet.conditional_format(f'E2:E{last_row}', {
        'type': 'formula',
        'criteria': '=$K2="NO PEDIDO"',
        'format': border_format
    })
    
    writer.close()

