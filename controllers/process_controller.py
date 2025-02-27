from services.comparador import comparar_dataframes
from controllers.file_controller import export_excel_with_style

def procesar(df_pedidos, df_llegadas):

    df_resultado = comparar_dataframes(df_pedidos, df_llegadas)

    df_resultado.to_excel("resultado.xlsx", index=False)

    return export_excel_with_style(df_resultado, "resultado.xlsx")