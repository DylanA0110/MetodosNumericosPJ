import numpy as np
from collections import namedtuple

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100, verbose=False):
  
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
        error = abs(x_next - x_current)

        results.append(Iteration(i, x_current, fx, dfx, x_next, error))
        if verbose:
            print(f"[NR] it={i}, x={x_current:.6f}, f={fx:.3e}, df={dfx:.3e}, x_next={x_next:.6f}, err={error:.2e}")

        if error < tol:
            break

        x_current = x_next

    return results, x_next
