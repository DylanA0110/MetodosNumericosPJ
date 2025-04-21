import pandas as pd
import sympy as sp
import os

def exportar_excel(resultados, nombre_archivo="resultados.xlsx", metodo="Metodo", funcion_str_expr=None):
    # Ruta de destino en el escritorio
    carpeta_destino = r"C:\Users\PC\Desktop\exceles calculados"
    os.makedirs(carpeta_destino, exist_ok=True)  # Crear la carpeta si no existe
    if metodo == "newton_raphson":
        columnas = ["Iteración", "X_i-1", "f(X_i-1)", "f'(X_i-1)", "X_i", "Error"]
    elif metodo == "secante":
        columnas = ["Iteración", "X_i-1", "X_i", "f(X_i-1)", "f(X_i)", "X_i+1", "f(X_i+1)", "Error"]
    else:  # punto fijo
        columnas = ["Iteración", "X_n", "X_n+1", "Error"]

    nombre_archivo = f"resultados_{metodo}.xlsx"

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Resultados')
        writer.sheets['Resultados'] = worksheet

        # Crear formato para encabezados en negrita
        formato_negrita = workbook.add_format({'bold': True})

        # Fila 0: función usada
        if funcion_str_expr is not None:
            funcion_str = f"Función usada: {sp.sstr(funcion_str_expr)}"
            worksheet.write(0, 0, funcion_str)

        # Fila 1: encabezados
        for col_num, value in enumerate(columnas):
            worksheet.write(1, col_num, value, formato_negrita)  # Aplicar formato en negrita

        # Fila 2+: datos
        for row_num, fila in enumerate(resultados, start=2):
            for col_num, value in enumerate(fila):
                worksheet.write(row_num, col_num, value)

    print(f"Resultados guardados en {nombre_archivo}")

# Ejemplo de uso
# exportar_excel(resultados, metodo="secante", funcion_str_expr=sp.sympify("x**2 - x*sin(x) - cos(x)"))