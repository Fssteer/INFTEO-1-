import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

def calculadora(num1, num2, op):
    try:
        n1 = float(num1)
        n2 = float(num2)
        if op == "+":
            return n1 + n2
        elif op == "-":
            return n1 - n2
        elif op == "*":
            return n1 * n2
        elif op == "/":
            return n1 / n2
    except:
        return None

Form, Window = uic.loadUiType("calculadora.ui")

class CalculadoraApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Form()
        self.ui.setupUi(self)

        self.num1 = ""
        self.num2 = ""
        self.operacion = ""
        self.pantalla = self.ui.Variables

        self.ui.Button1.clicked.connect(lambda: self.presionar_numero(1))
        self.ui.Button2.clicked.connect(lambda: self.presionar_numero(2))
        self.ui.Button3_4.clicked.connect(lambda: self.presionar_numero(3))
        self.ui.Button4_2.clicked.connect(lambda: self.presionar_numero(4))
        self.ui.Button5.clicked.connect(lambda: self.presionar_numero(5))
        self.ui.Button6.clicked.connect(lambda: self.presionar_numero(6))
        self.ui.Button7.clicked.connect(lambda: self.presionar_numero(7))
        self.ui.Button8.clicked.connect(lambda: self.presionar_numero(8))
        self.ui.Button9.clicked.connect(lambda: self.presionar_numero(9))
        self.ui.Button10.clicked.connect(lambda: self.presionar_numero(0))
        self.ui.Punto.clicked.connect(lambda: self.presionar_numero("."))

        self.ui.SUMA.clicked.connect(lambda: self.presionar_operacion("+"))
        self.ui.RESTA.clicked.connect(lambda: self.presionar_operacion("-"))
        self.ui.MULTIPLICACION.clicked.connect(lambda: self.presionar_operacion("*"))
        self.ui.DIVISION.clicked.connect(lambda: self.presionar_operacion("/"))

        self.ui.IGUAL.clicked.connect(self.presionar_igual)

    def presionar_numero(self, valor):
        self.pantalla.setText(self.pantalla.text() + str(valor))

    def presionar_operacion(self, op):
        if self.pantalla.text() != "":
            self.num1 = self.pantalla.text()
            self.operacion = op
            self.pantalla.setText("")

    def presionar_igual(self):
        if self.num1 != "" and self.operacion != "" and self.pantalla.text() != "":
            self.num2 = self.pantalla.text()
            resultado = calculadora(self.num1, self.num2, self.operacion)
            if resultado is not None:
                if resultado == int(resultado):
                    self.pantalla.setText(str(int(resultado)))
                else:
                    self.pantalla.setText(str(resultado))
            self.num1 = ""
            self.num2 = ""
            self.operacion = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraApp()
    ventana.show()
    sys.exit(app.exec_())
