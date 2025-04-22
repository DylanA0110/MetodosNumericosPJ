import os
import sympy as sp
import numpy as np
import sys

sys.path.append(os.path.abspath('Metodos_Abiertos'))
sys.path.append(os.path.abspath('Utils'))

from Metodos_Abiertos.punto_fijo import punto_fijo
from Metodos_Abiertos.newton_raphson import newton_raphson
from Metodos_Abiertos.secante import secante
from Metodos_Abiertos.newton_raphson_sistemas import newton_raphson_sistemas
from Utils.exportador import exportar_sistemas
from Utils.graficador import graficar_errores
from Utils.exportador import exportar_excel

x = sp.Symbol('x')

metodo = input("Elige un método (punto_fijo, newton_raphson, secante, sistemas): ").strip()

tol = 0.01
print("Usando tolerancia fija: 0.01")

if metodo == "punto_fijo":
    g_input = input("Ingresa la función g(x): ")
    g_expr = sp.sympify(g_input)
    g = sp.lambdify(x, g_expr, "numpy")
    x0 = float(input("Ingresa el valor inicial x0: "))

    resultados = punto_fijo(g, x0, tol)
    graficar_errores(resultados, "Punto Fijo")
    exportar_excel(resultados, metodo="punto_fijo", funcion_str_expr=g_expr)

elif metodo == "newton_raphson":
    f_input = input("Ingresa la función f(x): ")
    f_expr = sp.sympify(f_input)
    df_expr = sp.diff(f_expr, x)
    f = sp.lambdify(x, f_expr, "numpy")
    df = sp.lambdify(x, df_expr, "numpy")
    x0 = float(input("Ingresa el valor inicial x0: "))

    resultados, raiz = newton_raphson(f, df, x0, tol)
    graficar_errores(resultados, "Newton-Raphson")
    exportar_excel(resultados, metodo="newton_raphson", funcion_str_expr=f_expr)

elif metodo == "secante":
    f_input = input("Ingresa la función f(x): ")
    f_expr = sp.sympify(f_input)
    f = sp.lambdify(x, f_expr, "numpy")
    x0 = float(input("Ingresa el valor inicial x0: "))
    x1 = float(input("Ingresa el segundo valor inicial x1: "))

    resultados = secante(f, x0, x1, tol)
    graficar_errores(resultados, "Secante")
    exportar_excel(resultados, metodo="secante", funcion_str_expr=f_expr)

elif metodo == "sistemas":
    n = int(input("¿Cuántas variables tiene el sistema?: "))
    variables = sp.symbols([f'x{i+1}' for i in range(n)])

    funciones_input = [input(f"Ingrese f{i+1}(x): ") for i in range(n)]
    funciones_expr = [sp.sympify(expr) for expr in funciones_input]

    jacobiana_expr = sp.Matrix(funciones_expr).jacobian(variables)

    F = sp.lambdify(variables, funciones_expr, 'numpy')
    J = sp.lambdify(variables, jacobiana_expr, 'numpy')

    # Valores iniciales: uno por cada variable
    x0 = [float(input(f"Ingresa x{i+1}_0: ")) for i in range(n)]

    # Ejecutar
    resultados, solucion = newton_raphson_sistemas(F, J, x0, tol)

    exportar_sistemas(resultados, funcion_str_expr=funciones_expr)


else:
    print("❌ Método no válido.")
