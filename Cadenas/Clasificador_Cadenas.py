import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def clasificar():
    texto = entrada.get()
    if not texto.strip():
        messagebox.showwarning("Advertencia", "Por favor, ingrese al menos una cadena.")
        return

    cadenas = [c.strip() for c in texto.split(",")]

    vacias = sum(1 for c in cadenas if c == "")
    cortas = sum(1 for c in cadenas if 1 <= len(c) <= 3)
    pares = sum(1 for c in cadenas if len(c) % 2 == 0 and c != "")
    impares = sum(1 for c in cadenas if len(c) % 2 != 0)
    largas = sum(1 for c in cadenas if len(c) > 5)

    categorias = ["Vacías", "Cortas", "Pares", "Impares", "Largas"]
    valores = [vacias, cortas, pares, impares, largas]

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    figura = Figure(figsize=(5, 3), dpi=100)
    ax = figura.add_subplot(111)
    barras = ax.bar(categorias, valores, color=["yellow", "blue", "green", "red", "pink"], edgecolor="black")

    ax.set_title("Histograma de Cadenas por Longitud", fontsize=12, fontweight="bold")
    ax.set_xlabel("Categorías", fontsize=10)
    ax.set_ylabel("Cantidad", fontsize=10)

    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, '%d' % int(height),
                ha='center', va='bottom', fontsize=9)

    figura.tight_layout()
    canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ventana = tk.Tk()
ventana.title("Clasificador de Cadenas")
ventana.geometry("600x500")
ventana.config(bg="black")

estilo = ttk.Style()
estilo.configure("TButton", font=("Arial", 10, "bold"), padding=6)
estilo.configure("TLabel", background="#E8F6FF", font=("Arial", 10))

titulo = tk.Label(ventana, text="CLASIFICADOR DE CADENAS", 
                  font=("Arial", 16, "bold"), bg="grey", fg="white", pady=5)
titulo.pack(pady=10)

tk.Label(ventana, text="INGRESE UNA O VARIAS CADENAS SEPARADAS POR COMA (,):", bg="grey", fg="white").pack()
entrada = tk.Entry(ventana, width=60)
entrada.pack(pady=5)

boton = tk.Button(ventana, text="Mostrar Histograma", command=clasificar,
                  bg="white", fg="black", font=("Arial", 10, "bold"), relief="raised", bd=2)
boton.pack(pady=10)

frame_grafico = tk.Frame(ventana, bg="grey", relief="solid", bd=1)
frame_grafico.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

ventana.mainloop()
