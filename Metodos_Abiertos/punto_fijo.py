import numpy as np

def punto_fijo(g, x0, tol, max_iter=100):
    resultados = []
    x = x0

    for i in range(max_iter):
        try:
            x_next = g(x)
            error = abs(x_next - x)

            if not np.isfinite(x_next):
                print(f"[Iteración {i}] x_next no es válido (NaN o infinito). Se aborta.")
                break

            resultados.append([i, x, x_next, error])

            if error < tol:
                print(f"Convergió en la iteración {i} con error {error}")
                break

            x = x_next

        except Exception as e:
            print(f"Error en la iteración {i}: {e}")
            break

    else:
        print(f"No convergió en {max_iter} iteraciones. Último error: {error}")

    return resultados
