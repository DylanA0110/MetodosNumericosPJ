import sys
import os
import sympy as sp
import numpy as np

# Añadir rutas de módulos
sys.path.append(os.path.abspath('Metodos_Abiertos'))
sys.path.append(os.path.abspath('Utils'))

# Importar funciones personalizadas
from Metodos_Abiertos.punto_fijo import punto_fijo
from Metodos_Abiertos.newton_raphson import newton_raphson
from Metodos_Abiertos.secante import secante
from Utils.graficador import graficar_errores
from Utils.exportador import exportar_excel

# Definir símbolo simbólico
x = sp.Symbol('x')

# 👉 Entrada de la función principal f(x)
funcion_input = input("Ingresa la función f(x): ")
f_expr = sp.sympify(funcion_input)

# 👉 Derivada de la función
df_expr = sp.diff(f_expr, x)

# 👉 Convertir las expresiones simbólicas a funciones numéricas
f = sp.lambdify(x, f_expr, "numpy")
df = sp.lambdify(x, df_expr, "numpy")

# 👉 Método a usar
metodo = input("Elige un método (punto_fijo, newton_raphson, secante): ").strip()

# Si es punto fijo, también pide g(x)
g_expr = None
g = None
if metodo == "punto_fijo":
    g_input = input("Ingresa la función g(x): ")
    g_expr = sp.sympify(g_input)
    g = sp.lambdify(x, g_expr, "numpy")

# 👉 Valores iniciales
x00 = float(input("Ingresa el valor inicial x0: "))
x11 = None
if metodo == "secante":
    x11 = float(input("Ingresa el segundo valor inicial x1: "))

# 👉 Tolerancia fija
tol = 0.01
print("Usando tolerancia fija: 0.01")

# 🧮 Ejecutar método según selección
if metodo == "punto_fijo":
    resultados = punto_fijo(g, x00, tol)
    graficar_errores(resultados, "Punto Fijo")
    exportar_excel(resultados, metodo="punto_fijo", funcion_str_expr=g_expr)

elif metodo == "newton_raphson":
    resultados, raiz = newton_raphson(f, df, x00, tol)  # Pasando las funciones numéricas
    graficar_errores(resultados, "Newton-Raphson")
    exportar_excel(resultados, metodo="newton_raphson", funcion_str_expr=f_expr)

elif metodo == "secante":
    resultados = secante(f, x00, x11, tol)
    graficar_errores(resultados, "Secante")
    exportar_excel(resultados, metodo="secante", funcion_str_expr=f_expr)

else:
    print("❌ Método no válido.")
