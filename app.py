from flask import Flask, render_template, request, jsonify
import numpy as np
from collections import namedtuple
import sympy as sp
import os
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

def calcular_error(x_new, x_old):
    """Calcula el error relativo porcentual según la fórmula de la imagen"""
    if x_new == 0:
        return float('inf')
    return abs((x_new - x_old) / x_new) * 100

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    if tol <= 0:
        raise ValueError("La tolerancia debe ser positiva.")
    if max_iter <= 0:
        raise ValueError("El número máximo de iteraciones debe ser positivo.")

    Iteration = namedtuple('Iteration', ['iter', 'x', 'fx', 'dfx', 'x_next', 'error'])
    results = []

    x_current = x0
    for i in range(1, max_iter + 1):
        fx = f(x_current)
        dfx = df(x_current)

        if not np.isfinite(fx) or not np.isfinite(dfx) or abs(dfx) < 1e-12:
            raise ZeroDivisionError(f"Problema numérico en x = {x_current}")

        x_next = x_current - fx / dfx
        error = calcular_error(x_next, x_current)

        results.append(Iteration(i, x_current, fx, dfx, x_next, error))

        if error < tol:
            break

        x_current = x_next

    return {'resultados': results, 'raiz': x_next, 'iteraciones': i}

def punto_fijo(g, x0, tol, max_iter=100):
    resultados = []
    x = x0

    for i in range(max_iter):
        try:
            x_next = g(x)
            error = calcular_error(x_next, x)

            if not np.isfinite(x_next):
                raise ValueError(f"[Iteración {i}] x_next no es válido (NaN o infinito). Se aborta.")

            resultados.append([i, x, x_next, error])

            if error < tol:
                break

            x = x_next

        except Exception as e:
            raise ValueError(f"Error en la iteración {i}: {e}")

    return {'resultados': resultados, 'raiz': x_next, 'iteraciones': i}

def secante(f, x0, x1, tol, max_iter=100):
    resultados = []

    for i in range(max_iter):
        f_x0, f_x1 = f(x0), f(x1)

        if not np.isfinite(f_x0) or not np.isfinite(f_x1):
            raise ValueError(f"f(x) no es finita en la iteración {i}. Terminando.")

        if f_x1 - f_x0 == 0:
            raise ZeroDivisionError(f"División por cero en la iteración {i}. Terminando.")

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = f(x2)
        error = calcular_error(x2, x1)

        resultados.append([i, x0, x1, f_x0, f_x1, x2, f_x2, error])

        if error < tol:
            break

        x0, x1 = x1, x2

    return {'resultados': resultados, 'raiz': x2, 'iteraciones': i}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    metodo = data['metodo']
    
    try:
        # Convertir la función string a una función Python
        x = sp.symbols('x')
        
        if metodo == 'newton':
            f_expr = sp.sympify(data['funcion'])
            f = sp.lambdify(x, f_expr, 'numpy')
            df_expr = sp.diff(f_expr, x)
            df = sp.lambdify(x, df_expr, 'numpy')
            x0 = float(data['x0'])
            tol = float(data['tolerancia'])
            max_iter = int(data['max_iter'])
            
            resultados = newton_raphson(f, df, x0, tol, max_iter)
            
        elif metodo == 'punto_fijo':
            g_expr = sp.sympify(data['funcion_g'])
            g = sp.lambdify(x, g_expr, 'numpy')
            x0 = float(data['x0'])
            tol = float(data['tolerancia'])
            max_iter = int(data['max_iter'])
            
            resultados = punto_fijo(g, x0, tol, max_iter)
            
        elif metodo == 'secante':
            f_expr = sp.sympify(data['funcion'])
            f = sp.lambdify(x, f_expr, 'numpy')
            x0 = float(data['x0'])
            x1 = float(data['x1'])
            tol = float(data['tolerancia'])
            max_iter = int(data['max_iter'])
            
            resultados = secante(f, x0, x1, tol, max_iter)
            
        else:
            raise ValueError("Método no válido")
        
        # Convertir namedtuple a dict para JSON
        if metodo == 'newton':
            resultados['resultados'] = [r._asdict() for r in resultados['resultados']]
            
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)