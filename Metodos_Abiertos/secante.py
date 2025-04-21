import pandas as pd
import numpy as np

def secante(f, x0, x1, tol, max_iter=100):
    resultados = []

    for i in range(max_iter):
        f_x0, f_x1 = f(x0), f(x1)

        # ⚠️ Verificación de valores numéricos válidos
        if not np.isfinite(f_x0) or not np.isfinite(f_x1):
            print(f"❌ f(x) no es finita en la iteración {i}. Terminando.")
            break

        # ⚠️ Prevención de división por cero
        if f_x1 - f_x0 == 0:
            print(f"❌ División por cero en la iteración {i}. Terminando.")
            break

        # 📐 Fórmula de la secante
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = f(x2)
        error = abs(x2 - x1)

        # 📝 Guardar resultados de la iteración
        resultados.append([i, x0, x1, f_x0, f_x1, x2, f_x2, error])

        # ✅ Verificación de tolerancia
        if error < tol:
            print(f"✅ Tolerancia alcanzada en la iteración {i}.")
            break

        # 🔁 Actualización de valores
        x0, x1 = x1, x2

    else:
        print(f"⚠️ No se alcanzó la tolerancia después de {max_iter} iteraciones.")

    return resultados
