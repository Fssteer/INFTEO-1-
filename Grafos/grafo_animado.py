import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

def crear_grafo():
    G = nx.Graph()
    G.add_edges_from([
        (1, 2), (1, 5), (2, 5),
        (2, 4), (4, 3), (4, 5)
    ])
    return G

def recorrido_personalizado():
    return [
        (1, 5), (5, 1), (1, 2), (2, 5),
        (5, 4), (4, 2), (2, 4), (4, 3)
    ]

class VentanaGrafo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imagen 7")
        self.setGeometry(200, 200, 600, 500)

        self.G = crear_grafo()
        self.pos = {
            1: (0, 1),
            2: (1, 1),
            3: (2, 0),
            4: (1.5, 0),
            5: (0.5, 0)
        }

        self.recorrido = recorrido_personalizado()
        self.visitados = set()
        self.aristas_recorridas = []
        self.indice = 0

        layout = QVBoxLayout()
        self.label = QLabel(alignment=Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_animacion)
        self.timer.start(800)

    def actualizar_animacion(self):
        if self.indice >= len(self.recorrido):
            self.timer.stop()
            return

        u, v = self.recorrido[self.indice]
        self.aristas_recorridas.append((u, v))
        self.visitados.add(u)
        self.visitados.add(v)
        self.dibujar_grafo(v)
        self.indice += 1

    def dibujar_grafo(self, nodo_actual):
        plt.figure(figsize=(4, 3))
        nx.draw(self.G, self.pos, with_labels=True, node_color='lightgray',
                edgecolors='black', node_size=700, font_weight='bold')

        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.visitados,
                               node_color='lightgreen', node_size=700)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.aristas_recorridas,
                               width=3, edge_color='red')
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nodo_actual],
                               node_color='yellow', node_size=750)

        plt.axis('off')
        plt.savefig("grafo_animado.png", bbox_inches='tight')
        plt.close()

        pixmap = QPixmap("grafo_animado.png")
        self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGrafo()
    ventana.show()
    sys.exit(app.exec_())
