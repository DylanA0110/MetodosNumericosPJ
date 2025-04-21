import pandas as pd
import numpy as np
import sympy as sp
import os

import pandas as pd
import os

def exportar_excel(resultados, nombre_archivo="resultados.xlsx", metodo="Metodo", funcion_str_expr=None):
    # Ruta de destino en el escritorio
    carpeta_destino = r"C:\Users\PC\Desktop\exceles calculados"
    os.makedirs(carpeta_destino, exist_ok=True)  # Crear la carpeta si no existe
    if metodo == "newton_raphson":
        columnas = ["Iteración", "X_i-1", "f(X_i-1)", "f'(X_i-1)", "X_i", "Error"]
    elif metodo == "secante":
        columnas = ["Iteración", "X_i-1", "X_i", "f(X_i-1)", "f(X_i)", "X_i+1", "f(X_i+1)", "Error"]
    elif metodo == "punto_fijo":
        columnas = ["Iteración", "X_n", "X_n+1", "Error"]

    # Guardar el archivo Excel en la carpeta de destino
    nombre_archivo = os.path.join(carpeta_destino, f"resultados_{metodo}.xlsx")

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Resultados')
        writer.sheets['Resultados'] = worksheet

        # Crear formato para encabezados en negrita
        formato_negrita = workbook.add_format({'bold': True})

        # Fila 0: función usada
        if funcion_str_expr is not None:
            funcion_str = f"Función usada: {funcion_str_expr}"
            worksheet.write(0, 0, funcion_str)

        # Fila 1: encabezados
        for col_num, value in enumerate(columnas):
            worksheet.write(1, col_num, value, formato_negrita)  # Aplicar formato en negrita

        # Fila 2+: datos
        for row_num, fila in enumerate(resultados, start=2):
            for col_num, value in enumerate(fila):
                # Escribir valores numéricos directamente
                worksheet.write(row_num, col_num, value)

    print(f"Resultados guardados en {nombre_archivo}")
import pandas as pd
import os

def exportar_sistemas(resultados, nombre_archivo="resultados_sistemas.xlsx", funcion_str_expr=None):
    # Ruta de destino en el escritorio
    carpeta_destino = r"C:\Users\PC\Desktop\exceles calculados"
    os.makedirs(carpeta_destino, exist_ok=True)  # Crear la carpeta si no existe

    columnas = ["Iteración", "X_i", "F(X_i)", "J(X_i)", "Error"]

    # Guardar el archivo Excel en la carpeta de destino
    nombre_archivo = os.path.join(carpeta_destino, f"resultados_sistemas.xlsx")

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Resultados')
        writer.sheets['Resultados'] = worksheet

        # Crear formato para encabezados en negrita
        formato_negrita = workbook.add_format({'bold': True})

        # Fila 0: función usada
        if funcion_str_expr is not None:
            funcion_str = f"Función usada: {funcion_str_expr}"
            worksheet.write(0, 0, funcion_str)

        # Fila 1: encabezados
        for col_num, value in enumerate(columnas):
            worksheet.write(1, col_num, value, formato_negrita)  # Aplicar formato en negrita

        # Fila 2+: datos
        for row_num, fila in enumerate(resultados, start=2):
            for col_num, value in enumerate(fila):
                # Verificar si el valor es una lista o array
                if isinstance(value, (list, tuple)):
                    value = str(value)  # Convertir a cadena
                worksheet.write(row_num, col_num, value)

    print(f"Resultados de sistemas guardados en {nombre_archivo}")
