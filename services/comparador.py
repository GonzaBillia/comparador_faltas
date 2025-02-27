import pandas as pd

def roman_to_int(roman: str) -> int:
    """
    Convierte un número romano en un entero.
    Soporta símbolos básicos: I, V, X, L, C, D, M.
    """
    valores = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    total = 0
    roman = roman.upper()  # Asegurarse de que esté en mayúsculas
    for i in range(len(roman)):
        # Si el siguiente símbolo es mayor, resta en lugar de sumar
        if i + 1 < len(roman) and valores[roman[i]] < valores[roman[i + 1]]:
            total -= valores[roman[i]]
        else:
            total += valores[roman[i]]
    return total

def comparar_dataframes(df_pedidos, df_llegadas):
    """
    Compara pedidos y llegadas agrupando por SUCURSAL y TROQUEL para evitar duplicaciones
    y genera un reporte final con:
    
        SUCURSAL | CODBARRA | TROQUEL | PRODUCTO | CANTIDAD PEDIDA | 
        CANTIDAD ENVIADA | DIFERENCIAS | NUMERO DE ENVIO | FECHA DE ENVIO PEDIDO | 
        FECHA DE ENVIO | FECHA RECEPCION | ESTADO
        
    Se asume que en df_pedidos:
      - 'CANTIDAD_PEDIDA' es la cantidad solicitada.
      - 'Fecha_Envio' es la fecha del pedido.
      - 'CODBARRA' y 'DESCRIPCION' son datos del producto.
    Y en df_llegadas:
      - 'CANTIDAD_ENVIADA' es la cantidad llegada.
      - 'NUMERO_ENVIO', 'FECHA_ENVIO', 'FECHA_RECEPCION' y 'ESTADO_LLEGADA'
        provienen del CSV.
      - 'DESCRIPCION_LLEGADA' es la descripción del producto.
    
    Los nuevos estados se definen:
      - COMPLETO: Cantidad pedida == Cantidad enviada.
      - INCOMPLETO: Cantidad pedida > Cantidad enviada.
      - ERRONEO: Cantidad pedida < Cantidad enviada.
      - NO ENVIADO: Si FECHA RECEPCION está vacía.
      - NO PEDIDO: Si no se realizó pedido (por ejemplo, la cantidad pedida es 0).
      
    Finalmente, se convierten las columnas SUCURSAL, CODBARRA, TROQUEL y las cantidades a enteros.
    """
    # Aseguramos que las claves sean cadenas sin espacios extra.
    for col in ['SUCURSAL', 'TROQUEL']:
        df_pedidos[col] = df_pedidos[col].astype(str).str.strip()
        df_llegadas[col] = df_llegadas[col].astype(str).str.strip()
        
    # Convertir a numérico las cantidades en cada DataFrame.
    df_pedidos['CANTIDAD_PEDIDA'] = pd.to_numeric(df_pedidos['CANTIDAD_PEDIDA'], errors='coerce')
    df_llegadas['CANTIDAD_ENVIADA'] = pd.to_numeric(df_llegadas['CANTIDAD_ENVIADA'], errors='coerce')
    
    # Agrupar el DataFrame de pedidos por SUCURSAL y TROQUEL (tomando otros datos relevantes)
    pedidos_agrupados = df_pedidos.groupby(['SUCURSAL', 'TROQUEL'], as_index=False).agg({
        'CANTIDAD_PEDIDA': 'sum',
        'CODBARRA': 'first',
        'DESCRIPCION': 'first',
        'Fecha_Envio': 'first'
    })
    
    # Agrupar el DataFrame de llegadas por SUCURSAL y TROQUEL, incluyendo la columna DESCRIPCION_LLEGADA.
    llegadas_agrupadas = df_llegadas.groupby(['SUCURSAL', 'TROQUEL'], as_index=False).agg({
        'CANTIDAD_ENVIADA': 'sum',
        'NUMERO_ENVIO': 'first',
        'FECHA_ENVIO': 'first',
        'FECHA_RECEPCION': 'max',   # O 'first', según convenga
        'ESTADO_LLEGADA': 'first',
        'DESCRIPCION_LLEGADA': 'first'
    })
    
    # Realizar el merge outer para incluir filas de ambos DataFrames
    df_merged = pd.merge(
        pedidos_agrupados,
        llegadas_agrupadas,
        on=['SUCURSAL', 'TROQUEL'],
        how='outer'
    )
    
    # Rellenar los valores faltantes en las columnas de pedidos con 0.
    df_merged['CANTIDAD_PEDIDA'] = df_merged['CANTIDAD_PEDIDA'].fillna(0)
    df_merged['CODBARRA'] = df_merged['CODBARRA'].fillna(0)
    
    # Rellenar los valores faltantes en la cantidad enviada con 0.
    df_merged['CANTIDAD_ENVIADA'] = df_merged['CANTIDAD_ENVIADA'].fillna(0)
    
    # Calcular la diferencia: (lo que llegó) - (lo pedido)
    df_merged['DIFERENCIAS'] = df_merged['CANTIDAD_ENVIADA'] - df_merged['CANTIDAD_PEDIDA']
    
    # Rellenar la columna PRODUCTO combinando DESCRIPCION_LLEGADA y DESCRIPCION (si falta, usa la otra)
    df_merged['PRODUCTO'] = df_merged['DESCRIPCION_LLEGADA'].fillna(df_merged['DESCRIPCION'])
    
    # Seleccionar las columnas finales en el orden deseado.
    df_final = df_merged[[ 
        'SUCURSAL',             # Clave del merge
        'CODBARRA',             # Del df_pedidos (0 si no existe pedido)
        'TROQUEL',
        'PRODUCTO',             # Columna combinada
        'CANTIDAD_PEDIDA',      # Lo pedido
        'CANTIDAD_ENVIADA',     # Lo que llegó
        'DIFERENCIAS',
        'NUMERO_ENVIO',         # Del df_llegadas
        'FECHA_ENVIO',          # Fecha de envío (llegada)
        'FECHA_RECEPCION'
    ]].copy()
    
    # Renombrar columnas para el formato final
    df_final.rename(columns={
        'CANTIDAD_PEDIDA': 'CANTIDAD PEDIDA',
        'CANTIDAD_ENVIADA': 'CANTIDAD ENVIADA',
        'NUMERO_ENVIO': 'NUMERO DE ENVIO',
        'FECHA_ENVIO': 'FECHA DE ENVIO',
        'FECHA_RECEPCION': 'FECHA RECEPCION'
    }, inplace=True)
    
    # Definir la función para asignar el estado
    def get_estado(row):
        # Si la cantidad pedida es 0, se asume que no se realizó el pedido.
        if row['CANTIDAD PEDIDA'] == 0:
            return 'NO PEDIDO'
        # Si FECHA RECEPCION es nula, se considera NO ENVIADO.
        if pd.isnull(row['FECHA RECEPCION']):
            return 'NO ENVIADO'
        # Comparar cantidades:
        if row['CANTIDAD PEDIDA'] == row['CANTIDAD ENVIADA']:
            return 'COMPLETO'
        elif row['CANTIDAD PEDIDA'] > row['CANTIDAD ENVIADA']:
            return 'INCOMPLETO'
        elif row['CANTIDAD PEDIDA'] < row['CANTIDAD ENVIADA']:
            return 'ERRONEO'
        else:
            return ''
    
    df_final['ESTADO'] = df_final.apply(get_estado, axis=1)
    
    # Convertir las columnas SUCURSAL, CODBARRA, TROQUEL y las cantidades a enteros.
    df_final['SUCURSAL'] = pd.to_numeric(df_final['SUCURSAL'], errors='coerce').fillna(0).astype(int)
    df_final['CODBARRA'] = pd.to_numeric(df_final['CODBARRA'], errors='coerce').fillna(0).astype(int)
    df_final['TROQUEL'] = pd.to_numeric(df_final['TROQUEL'], errors='coerce').fillna(0).astype(int)
    df_final['CANTIDAD PEDIDA'] = pd.to_numeric(df_final['CANTIDAD PEDIDA'], errors='coerce').fillna(0).astype(int)
    df_final['CANTIDAD ENVIADA'] = pd.to_numeric(df_final['CANTIDAD ENVIADA'], errors='coerce').fillna(0).astype(int)
    df_final['DIFERENCIAS'] = pd.to_numeric(df_final['DIFERENCIAS'], errors='coerce').fillna(0).astype(int)
    
    df_final = df_final.sort_values(by='SUCURSAL')

    return df_final

