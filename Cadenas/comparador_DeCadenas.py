import sys
import time
import warnings
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

import matplotlib
matplotlib.use("Qt5Agg")


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ComparadorCadenas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparador de Cadenas")
        self.setGeometry(200, 100, 850, 650)
        self.setStyleSheet("background-color: #F2F2F2; font-family: Arial; font-size: 13px;")

        
        self.label1 = QLabel("Cadena 1:")
        self.label2 = QLabel("Cadena 2:")
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input1.setPlaceholderText("Ingrese la primera cadena")
        self.input2.setPlaceholderText("Ingrese la segunda cadena")

        # Botones
        self.btn_comparar = QPushButton("Comparar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_salir = QPushButton("Salir")

        for btn in [self.btn_comparar, self.btn_limpiar, self.btn_salir]:
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; 
                    color: white; 
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)

        # Eventos
        self.btn_comparar.clicked.connect(self.comparar_cadenas)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_salir.clicked.connect(QApplication.quit)

        # Etiqueta de resultados 
        self.resultado = QLabel("")
        self.resultado.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")

        # Gráficos (matplotlib embebido) 
        self.fig, self.ax = plt.subplots(1, 2, figsize=(8, 3))
        self.canvas = FigureCanvas(self.fig)

        # Layouts 
        layout_inputs = QHBoxLayout()
        layout_inputs.addWidget(self.label1)
        layout_inputs.addWidget(self.input1)
        layout_inputs.addWidget(self.label2)
        layout_inputs.addWidget(self.input2)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_comparar)
        layout_botones.addWidget(self.btn_limpiar)
        layout_botones.addWidget(self.btn_salir)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_inputs)
        layout_main.addLayout(layout_botones)
        layout_main.addWidget(self.resultado)
        layout_main.addWidget(self.canvas)

        self.setLayout(layout_main)

    # Función principal 
    def comparar_cadenas(self):
        c1 = self.input1.text().strip()
        c2 = self.input2.text().strip()

        if not c1 or not c2:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese ambas cadenas.")
            return

        # Comparaciones 
        son_identicas = c1 == c2
        misma_longitud = len(c1) == len(c2)

        if c1 < c2:
            orden = f'"{c1}" es menor lexicográficamente que "{c2}".'
            valor_lex = [-1, 1]
        elif c1 > c2:
            orden = f'"{c1}" es mayor lexicográficamente que "{c2}".'
            valor_lex = [1, -1]
        else:
            orden = "Las cadenas son idénticas lexicográficamente."
            valor_lex = [0, 0]

        # Texto del resultado
        texto = (
            f"Cadenas idénticas: {'Sí' if son_identicas else 'No'}\n"
            f"Misma longitud: {'Sí' if misma_longitud else 'No'}\n"
            f"Orden lexicográfico: {orden}"
        )
        self.resultado.setText(texto)

        # Colores de barras dinámicos 
        color1 = "#4CAF50" if son_identicas else "#2196F3"
        color2 = "#FF9800" if not misma_longitud else "#9C27B0"

        # Limpiar ejes anteriores 
        for a in self.ax:
            a.clear()

        # Gráfico 1: Longitud
        self.ax[0].bar(["Cadena 1", "Cadena 2"], [len(c1), len(c2)], color=[color1, color2])
        self.ax[0].set_title("Comparación de Longitud")
        self.ax[0].set_ylabel("Número de caracteres")

        # Mostrar valores encima de las barras
        for i, v in enumerate([len(c1), len(c2)]):
            self.ax[0].text(i, v + 0.1, str(v), ha='center', fontsize=10, fontweight='bold')

        # Gráfico 2: Orden lexicográfico
        colors_lex = ["#FF5722" if v < 0 else "#4CAF50" if v > 0 else "#9E9E9E" for v in valor_lex]
        self.ax[1].bar(["Cadena 1", "Cadena 2"], valor_lex, color=colors_lex)
        self.ax[1].set_title("Orden Lexicográfico")
        self.ax[1].set_ylabel("Posición relativa")

        self.fig.tight_layout()
        self.canvas.draw()

        # Conclusión emergente
        if son_identicas:
            QMessageBox.information(self, "Conclusión", "Las cadenas son completamente idénticas.")
        elif misma_longitud:
            QMessageBox.information(self, "Conclusión", "Tienen la misma longitud pero son diferentes.")
        else:
            QMessageBox.information(self, "Conclusión", "Son diferentes tanto en contenido como en longitud.")

    #  Botón limpiar
    def limpiar_campos(self):
        self.input1.clear()
        self.input2.clear()
        self.resultado.setText("")
        for a in self.ax:
            a.clear()
        self.canvas.draw()


# Programa principal 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComparadorCadenas()
    window.show()
    sys.exit(app.exec_())
