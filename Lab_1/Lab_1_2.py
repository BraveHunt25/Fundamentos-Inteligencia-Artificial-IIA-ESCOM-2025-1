import os
import tkinter as tk
from tkinter import Canvas
import numpy as np
from numpy.typing import NDArray
from Lab_1_1 import enmascarar_celda, enmascarar_mapa

MAPA_TERRENO = "mapa_1.txt"
MAPA_DECISIONES = None
MAPA_MASCARA = None
MAPA_MOVIMIENTO = None


class InterfazMapa:
    def __init__(self, root, ruta_mapa:str = None, ruta_mapa_decisiones: str = None, ruta_mapa_mascara: str = None, ruta_mapa_movimiento: str = None, x_inicio: int = None, y_inicio: int = None):
        self.root = root
        self.root.title("Interfaz de Mapas")
        
        # Tamaño de las celdas de la cuadrícula
        self.cell_size = 20
        
        
# ----------- Generar y dibujar mapas iniciales ------------------------------------------
        # Inicializando mapa de terreno
        self.mapa = None
        self.ruta_absoluta_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa)

        if os.path.exists(self.ruta_absoluta_mapa):
            print("Se encontró el archivo\n")
            # Conversión de archivo a arreglo numpy
            self.mapa = np.genfromtxt(self.ruta_absoluta_mapa, delimiter=',', dtype=int)
        else:
            # print("No se ha encontrado el archivo de mapa. Asegúrate de colocarlo en la misma carpeta que este programa")
            raise FileNotFoundError("No se ha encontrado el archivo de mapa. Asegúrate de colocarlo en la misma carpeta que este programa")


        # Inicializando mapa de decisiones
        self.mapa_decisiones = None
        # Búsqueda o creación de mapa de decisiones
        if ruta_mapa_decisiones is None:
            print("No se ha indicado un mapa de decisiones, generando uno en blanco...\n")
            self.mapa_decisiones = np.zeros_like(self.mapa)
            # print("El mapa de decisiones se llena con ceros\n")
            # print(mapa_decisiones, "\n")
        else:
            self.ruta_absoluta_mapa_decisiones = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_decisiones)
            if os.path.exists(self.ruta_absoluta_mapa_decisiones):
                # print("Se encontró el archivo\n")
                self.mapa_decisiones = np.genfromtxt(self.ruta_absoluta_mapa_decisiones, delimiter=',', dtype=int)
                if self.mapa.shape != self.mapa_decisiones.shape:
                    # print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
                    raise ValueError("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado")
            else:
                # print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
                raise FileNotFoundError("No se ha encontrado el archivo de decisiones")


        # Inicializando mapa máscara
        self.mapa_mascara = None
        # Búsqueda o creación de máscara
        if ruta_mapa_mascara is None:
            print("No se ha indicado una máscara para el mapa, generando uno en blanco...\n")
            x_inicio = np.random.randint(0, self.mapa.shape[0]) if x_inicio is None else np.clip(x_inicio, 0, self.mapa_mascara.shape[0])
            y_inicio = np.random.randint(0, self.mapa.shape[1]) if y_inicio is None else np.clip(y_inicio, 0, self.mapa_mascara.shape[1])
            self.mapa_mascara = enmascarar_mapa(self.mapa, self.mapa_decisiones, x_inicio, y_inicio)
            # print("La máscara para el mapa ha sido creado:\n")
            # print(mapa_mascara, "\n")
        else:
            self.ruta_absoluta_mapa_mascara = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_mascara)
            if os.path.exists(self.ruta_absoluta_mapa_mascara):
                # print("Se encontró el archivo\n")
                self.mapa_mascara = np.genfromtxt(self.ruta_absoluta_mapa_mascara, delimiter=',', dtype=int)
                if self.mapa.shape != self.mapa_mascara.shape:
                    # print("Las dimensiones del mapa 'máscara' no corresponden al del mapa cargado\n")
                    raise ValueError("Las dimensiones del mapa 'máscara' no corresponden al del mapa cargado")
            else:
                # print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
                raise FileNotFoundError("No se ha encontrado el archivo de máscara")
        
        
        # Iniciaizando mapa de movimiento
        self.mapa_movimiento = None
        # Búsqueda o inicialización de posicionamiento
        if ruta_mapa_movimiento is None:
            print("No se tiene registro de la posición del agente, generando uno en blanco...\n")
            self.mapa_movimiento = np.zeros_like(self.mapa)
            self.indices = np.where(self.mapa_decisiones == 1)
            if self.indices[0].size > 0:
            # Obtener la primera posición
                self.pos_agente_x, self.pos_agente_y = self.indices[0][0], self.indices[1][0]
                print(f"Se encontró la posición inicial en las coordenadas ({self.pos_agente_x}, {self.pos_agente_y})")
                self.mapa_movimiento[self.pos_agente_x, self.pos_agente_y] = 1
                # print("El mapa de decisiones de movilidad se ha iniciado\n")
            else:
                print("No se encontró ningún '1' en el arreglo.")
        else:
            self.ruta_absoluta_mapa_movimiento = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_movimiento)
            if os.path.exists(self.ruta_absoluta_mapa_movimiento):
                # print("Se encontró el archivo\n")
                self.mapa_movimiento = np.genfromtxt(self.ruta_absoluta_mapa_movimiento, delimiter=',', dtype=int)
                if self.mapa.shape != self.mapa_movimiento.shape:
                    # print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
                    raise ValueError("Las dimensiones del mapa de movimiento no corresponden al del mapa cargado")
            else:
                # print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
                raise FileNotFoundError("No se ha encontrado el archivo de movimiento")
        
        # Crear el lienzo donde se dibujarán las cuadrículas
        self.canvas = Canvas(root, width=self.mapa.shape[0] * self.cell_size, height=self.mapa.shape[1] * self.cell_size)
        self.canvas.pack()

        self.dibujar_mapa()

# ------------------------- Dibujado de mapa -----------------------------
    def dibujar_mapa(self):
        # Limpiar el canvas
        self.canvas.delete("all")
        
        # Dibujar las celdas del mapa base
        for x in range(self.mapa.shape[0]):
            for y in range(self.mapa.shape[1]):
                color = self.obtener_color_celda(self.mapa[x, y], self.mapa_mascara[x, y])
                self.canvas.create_rectangle(
                    y * self.cell_size, x * self.cell_size, 
                    (y + 1) * self.cell_size, (x + 1) * self.cell_size, 
                    fill=color, outline="black"
                )

# ------------------------- Coloreando el mapa -----------------------------    
    def obtener_color_celda(self, valor, visible):
        """Determina el color de la celda en función del valor del mapa y si está visible."""
        if visible == 0:
            return "white"  # Celda oculta
        colores_terrenos = {
            0: "gray",    # Montaña
            1: "green",   # Tierra
            2: "blue",    # Agua
            3: "yellow",  # Arena
            4: "darkgreen", # Bosque
            5: "brown",   # Pantano
            6: "white"    # Nieve
        }
        return colores_terrenos.get(valor, "black")

if __name__ == "__main__":
    root = tk.Tk()
    interfaz = InterfazMapa(root, ruta_mapa=MAPA_TERRENO, ruta_mapa_decisiones=MAPA_DECISIONES, ruta_mapa_mascara=MAPA_MASCARA, ruta_mapa_movimiento=MAPA_MOVIMIENTO)
    root.mainloop()
