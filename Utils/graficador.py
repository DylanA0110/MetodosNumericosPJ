import matplotlib.pyplot as plt

def graficar_errores(resultados, metodo):
    iteraciones = [r[0] for r in resultados]
    errores = [r[-1] for r in resultados]  
    
    plt.plot(iteraciones, errores, marker='o', linestyle='-')
    plt.xlabel("Iteración")
    plt.ylabel("Error")
    plt.title(f"Convergencia - {metodo}")
    plt.grid()
    plt.show()
