import sys
import os
import networkx as nx
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

def crear_grafo():
    G = nx.Graph()
    G.add_edges_from([
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 5),
        (5, 6)
    ])
    return G

def recorrido_personalizado():
    return [
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 5),
        (5, 6)
    ]


class VentanaGrafo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafo 7 Animado")
        self.setGeometry(200, 200, 500, 500)

        
        self.G = crear_grafo()
        self.pos = {
            1: (-0.6, 1.2),
            2: (0.9, 1.6),
            3: (1.9, 0.9),
            4: (0.6, 0.6),
            5: (1.1, -0.2),
            6: (-0.1, -0.9)
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
            self.indice = 0
            self.visitados.clear()
            self.aristas_recorridas.clear()

        u, v = self.recorrido[self.indice]
        self.aristas_recorridas.append((u, v))
        self.visitados.add(u)
        self.visitados.add(v)
        self.dibujar_grafo(v)
        self.indice += 1

    def dibujar_grafo(self, nodo_actual):
        plt.figure(figsize=(5, 6))
        nx.draw(self.G, self.pos, with_labels=True, node_color='lightgray',
                edgecolors='black', node_size=900, font_weight='bold')

        
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.visitados,
                               node_color='lightgreen', node_size=900)

        
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.aristas_recorridas,
                               width=3, edge_color='red')

        
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[nodo_actual],
                               node_color='yellow', node_size=950)

        plt.axis('off')

        
        ruta_guardado = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imGrafo7_animado.png")
        plt.savefig(ruta_guardado, bbox_inches='tight', dpi=200)
        plt.close()

    
        pixmap = QPixmap(ruta_guardado)
        self.label.setPixmap(pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaGrafo()
    ventana.show()
    sys.exit(app.exec_())
