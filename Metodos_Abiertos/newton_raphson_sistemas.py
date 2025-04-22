import numpy as np
from collections import namedtuple

def newton_raphson_sistemas(F, J, x0, tol=1e-6, max_iter=100, verbose=False):
    
    Iteracion = namedtuple('Iteracion', ['iter', 'x', 'Fx', 'Jx', 'delta', 'error'])
    resultados = []

    x_current = np.array(x0, dtype=float)

    for i in range(1, max_iter + 1):
        Fx = np.array(F(*x_current), dtype=float)
      
        Jx = np.array(J(*x_current), dtype=float)

        try:
            delta = np.linalg.solve(Jx, -Fx)
        except np.linalg.LinAlgError:
            raise ValueError(f"Jacobian no invertible en la iteración {i}")

        x_next = x_current + delta
        error = np.linalg.norm(delta, 2)

        resultados.append(Iteracion(i, x_current.copy(), Fx.copy(), Jx.copy(), delta.copy(), error))
        if verbose:
            print(f"Iter {i}: x={x_current}, Fx={Fx}, error={error:.2e}")

        if error < tol:
            break
        x_current = x_next

    return resultados, x_current
