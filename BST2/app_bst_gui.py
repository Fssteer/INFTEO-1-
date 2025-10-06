# app_bst_gui.py
import sys
import os
import csv
from binarytree import Node
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic

def construir_bst(nombres):
    if not nombres:
        return None
    nombres.sort()
    def build_bst(sorted_list):
        if not sorted_list:
            return None
        mid = len(sorted_list) // 2
        node = Node(sorted_list[mid])
        node.left = build_bst(sorted_list[:mid])
        node.right = build_bst(sorted_list[mid + 1:])
        return node
    return build_bst(nombres)

def buscar_por_extension(root, extension, resultado):
    if root:
        buscar_por_extension(root.left, extension, resultado)
        if root.value.endswith(extension):
            resultado.append(root.value)
        buscar_por_extension(root.right, extension, resultado)

def exportar_csv(lista, nombre_archivo='inventario_archivos.csv'):
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nombre del archivo'])
            for item in lista:
                writer.writerow([item])
        print(f"Archivo exportado como {nombre_archivo}")
    except Exception as e:
        print(f"Error al exportar CSV: {e}")

def obtener_recorridos(root):
    if not root:
        return {'inorder': [], 'preorder': [], 'postorder': []}
    return {
        'inorder': [node.value for node in root.inorder],
        'preorder': [node.value for node in root.preorder],
        'postorder': [node.value for node in root.postorder]
    }

def procesar_archivo_txt(ruta_txt):
    if not os.path.exists(ruta_txt):
        print(f"El archivo '{ruta_txt}' no existe. Crea uno con rutas válidas.")
        return None, None
    with open(ruta_txt, 'r', encoding='utf-8') as f:
        rutas = [line.strip() for line in f.readlines() if line.strip()]
    if not rutas:
        print("El archivo está vacío o no tiene rutas válidas.")
        return None, None
    nombres = [os.path.basename(ruta) for ruta in rutas]
    root = construir_bst(nombres)
    if not root:
        print("No se pudo construir el árbol.")
        return None, None
    recorridos = obtener_recorridos(root)
    return root, recorridos

# ---------------- GUI ----------------

class BSTInterface(QWidget):
    def __init__(self):
        super().__init__()
        # Ruta relativa para que cargue hansolo.ui desde la misma carpeta
        current_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(current_dir, "hansolo.ui"), self)

        self.root = None
        self.recorridos = None

        # Conectar botones
        self.btnCargar.clicked.connect(self.cargar_files)
        self.btnBuscar.clicked.connect(self.buscar_extension)
        self.btnInorden.clicked.connect(lambda: self.mostrar_recorrido('inorder'))
        self.btnPreorden.clicked.connect(lambda: self.mostrar_recorrido('preorder'))
        self.btnPostorden.clicked.connect(lambda: self.mostrar_recorrido('postorder'))
        self.btnExportar.clicked.connect(self.exportar_resultados)

    def cargar_files(self):
        archivo = os.path.join(os.getcwd(), "files.txt")
        self.root, self.recorridos = procesar_archivo_txt(archivo)
        if self.root:
            self.textResultado.setPlainText("Archivo cargado y árbol generado.")
        else:
            self.textResultado.setPlainText("No se pudo cargar el archivo.")

    def buscar_extension(self):
        if not self.root:
            QMessageBox.warning(self, "Error", "Primero carga el archivo.")
            return
        ext = self.entradaExt.text()
        resultado = []
        buscar_por_extension(self.root, ext, resultado)
        self.textResultado.setPlainText("\n".join(resultado) if resultado else "No se encontraron archivos.")

    def mostrar_recorrido(self, tipo):
        if not self.recorridos:
            QMessageBox.warning(self, "Error", "Primero carga el archivo.")
            return
        self.textResultado.setPlainText("\n".join(self.recorridos[tipo]))

    def exportar_resultados(self):
        if not self.recorridos:
            QMessageBox.warning(self, "Error", "Primero carga el archivo.")
            return
        exportar_csv(self.recorridos['inorder'])
        QMessageBox.information(self, "Listo", "Archivo CSV exportado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BSTInterface()
    ventana.show()
    sys.exit(app.exec_())