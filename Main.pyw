import sys
import sympy as sp
import pywt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon 

print(pywt.__version__)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Metodos_Abiertos.punto_fijo import punto_fijo
from Metodos_Abiertos.newton_raphson import newton_raphson
from Metodos_Abiertos.secante import secante
from Metodos_Abiertos.newton_raphson_sistemas import newton_raphson_sistemas
from Utils.exportador import exportar_excel, exportar_sistemas
from Utils.graficador import graficar_errores

class MetodoNumericoGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Métodos Numéricos - Interfaz Gráfica")
        self.setMinimumWidth(900)
        self.init_ui()
        

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowIcon(QIcon("logo.ico"))
        # Selección de método
        self.metodo_combo = QComboBox()
        self.metodo_combo.addItems(["punto_fijo", "newton_raphson", "secante", "sistemas"])
        self.metodo_combo.currentTextChanged.connect(self.actualizar_inputs)
        
        layout.addWidget(QLabel("Seleccione el método:"))
        layout.addWidget(self.metodo_combo)

        # Entrada de función y parámetros
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Ej: x**2 - 2")

        self.x0_input = QLineEdit()
        self.x0_input.setPlaceholderText("Ej: 1.0")

        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText("Solo para método de la secante")

        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Número de variables (para sistemas)")

        self.multi_func_inputs = QTextEdit()
        self.multi_func_inputs.setPlaceholderText("Escriba una función por línea")

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Función f(x) o g(x):"))
        form_layout.addWidget(self.func_input)
        form_layout.addWidget(QLabel("x0:"))
        form_layout.addWidget(self.x0_input)
        form_layout.addWidget(QLabel("x1 (secante):"))
        form_layout.addWidget(self.x1_input)
        form_layout.addWidget(QLabel("n (sistemas):"))
        form_layout.addWidget(self.n_input)
        form_layout.addWidget(QLabel("Funciones del sistema (una por línea):"))
        form_layout.addWidget(self.multi_func_inputs)

        layout.addLayout(form_layout)

        # Botón ejecutar
        self.boton_ejecutar = QPushButton("Ejecutar")
        self.boton_ejecutar.clicked.connect(self.ejecutar_metodo)
        layout.addWidget(self.boton_ejecutar)

        # Mostrar función utilizada en formato matemático
        self.funcion_label = QLabel()
        self.funcion_label.setFont(QFont("Times", 12, QFont.Bold))
        self.funcion_label.setAlignment(Qt.AlignCenter)
        self.funcion_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.funcion_label.setLineWidth(1)
        self.funcion_label.setStyleSheet(
    "font-family: 'Courier New'; font-size: 16px; background-color: #f9f9f9; padding: 10px; border: 1px solid #ccc;"
)

        layout.addWidget(QLabel("Función utilizada (formato legible):"))
        layout.addWidget(self.funcion_label)

        # Resultado y tabla
        self.resultado_area = QTextEdit()
        self.resultado_area.setReadOnly(True)
        layout.addWidget(QLabel("Resultado:"))
        layout.addWidget(self.resultado_area)

        self.tabla_resultados = QTableWidget()
        layout.addWidget(QLabel("Tabla de Resultados:"))
        layout.addWidget(self.tabla_resultados)

        self.setLayout(layout)
        self.actualizar_inputs(self.metodo_combo.currentText())

    def actualizar_inputs(self, metodo):
        visible = metodo != "sistemas"
        self.func_input.setVisible(visible)
        self.x1_input.setVisible(metodo == "secante")
        self.n_input.setVisible(metodo == "sistemas")
        self.multi_func_inputs.setVisible(metodo == "sistemas")

    def mostrar_en_tabla(self, resultados, metodo):
        columnas_map = {
            "newton_raphson": ["Iteración", "X_i-1", "f(X_i-1)", "f'(X_i-1)", "X_i", "Error"],
            "secante": ["Iteración", "X_i-1", "X_i", "f(X_i-1)", "f(X_i)", "X_i+1", "f(X_i+1)", "Error"],
            "punto_fijo": ["Iteración", "X_n", "X_n+1", "Error"],
            "sistemas": ["Iteración", "X_i", "F(X_i)", "J(X_i)", "Error"]
        }

        columnas = columnas_map.get(metodo, [])
        self.tabla_resultados.setColumnCount(len(columnas))
        self.tabla_resultados.setHorizontalHeaderLabels(columnas)
        self.tabla_resultados.setRowCount(len(resultados))

        for i, fila in enumerate(resultados):
            for j, valor in enumerate(fila):
                if isinstance(valor, (list, tuple)):
                    valor = str(valor)
                item = QTableWidgetItem(str(valor))
                self.tabla_resultados.setItem(i, j, item)

    def ejecutar_metodo(self):
        metodo = self.metodo_combo.currentText()
        x = sp.Symbol('x')

        try:
            if metodo == "punto_fijo":
                g_expr = sp.sympify(self.func_input.text())
                g = sp.lambdify(x, g_expr, "numpy")
                x0 = float(self.x0_input.text())
                resultados = punto_fijo(g, x0, tol=0.01)
                self.mostrar_en_tabla(resultados, metodo)
                exportar_excel(resultados, metodo=metodo, funcion_str_expr=g_expr)
                graficar_errores(resultados, "Punto Fijo")
                
                self.funcion_label.setText(f"<pre>f(x) = {pretty(f_expr)}</pre>")

            elif metodo == "newton_raphson":
                f_expr = sp.sympify(self.func_input.text())
                df_expr = sp.diff(f_expr, x)
                f = sp.lambdify(x, f_expr, "numpy")
                df = sp.lambdify(x, df_expr, "numpy")
                x0 = float(self.x0_input.text())
                resultados, _ = newton_raphson(f, df, x0, tol=0.01)
                self.mostrar_en_tabla(resultados, metodo)
                exportar_excel(resultados, metodo=metodo, funcion_str_expr=f_expr)
                graficar_errores(resultados, "Newton-Raphson")
                
                self.funcion_label.setText(f"<pre>f(x) = {pretty(f_expr)}</pre>")

            elif metodo == "secante":
                f_expr = sp.sympify(self.func_input.text())
                f = sp.lambdify(x, f_expr, "numpy")
                x0 = float(self.x0_input.text())
                x1 = float(self.x1_input.text())
                resultados = secante(f, x0, x1, tol=0.01)
                self.mostrar_en_tabla(resultados, metodo)
                exportar_excel(resultados, metodo=metodo, funcion_str_expr=f_expr)
                graficar_errores(resultados, "Secante")
                
                self.funcion_label.setText(f"<pre>f(x) = {pretty(f_expr)}</pre>")

            elif metodo == "sistemas":
                n = int(self.n_input.text())
                variables = sp.symbols([f'x{i+1}' for i in range(n)])
                funciones_input = self.multi_func_inputs.toPlainText().splitlines()
                funciones_expr = [sp.sympify(expr) for expr in funciones_input]
                jacobiana_expr = sp.Matrix(funciones_expr).jacobian(variables)
                F = sp.lambdify(variables, funciones_expr, 'numpy')
                J = sp.lambdify(variables, jacobiana_expr, 'numpy')
                x0 = [float(self.x0_input.text())] * n
                resultados, _ = newton_raphson_sistemas(F, J, x0, tol=0.01)
                self.mostrar_en_tabla(resultados, metodo)
                exportar_sistemas(resultados, funcion_str_expr=funciones_expr)
                ss = "<pre>" + "\\n".join([f"f{i+1}(x) = {pretty(expr)}" for i, expr in enumerate(funciones_expr)]) + "</pre>"
                self.funcion_label.setText(s)


            self.resultado_area.setText("✅ Cálculo realizado correctamente. Revisa la tabla y Excel.")

        except Exception as e:
            self.resultado_area.setText(f"❌ Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetodoNumericoGUI()
    window.show()
    sys.exit(app.exec_())
