import os
import tkinter as tk
from tkinter import Canvas, Toplevel, StringVar, IntVar, messagebox
import numpy as np
from numpy.typing import NDArray
from Lab_1_1 import enmascarar_celda, enmascarar_mapa, mover_agente, personajes, terrenos, desplazamientos

MAPA_TERRENO = "mapa_1.txt"
MAPA_DECISIONES = None
MAPA_MASCARA = None
MAPA_MOVIMIENTO = None

class ConfiguracionInicial(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración Inicial")
        
        # Selección del personaje
        self.personaje = StringVar(self)
        self.personaje.set("humano")  # Valor por defecto
        personajes = ["humano", "mono", "pulpo", "piegrande"]
        tk.Label(self, text="Selecciona el personaje:").pack(pady=10)
        self.menu_personaje = tk.OptionMenu(self, self.personaje, *personajes)
        self.menu_personaje.pack(pady=5)
        
        # Posiciones iniciales
        self.x_inicio = IntVar(self)
        self.y_inicio = IntVar(self)
        tk.Label(self, text="Posición inicial (x):").pack(pady=5)
        self.entry_x_inicio = tk.Entry(self, textvariable=self.x_inicio)
        self.entry_x_inicio.pack(pady=5)
        
        tk.Label(self, text="Posición inicial (y):").pack(pady=5)
        self.entry_y_inicio = tk.Entry(self, textvariable=self.y_inicio)
        self.entry_y_inicio.pack(pady=5)
        
        # Posiciones finales
        self.x_final = IntVar(self)
        self.y_final = IntVar(self)
        tk.Label(self, text="Posición final (x):").pack(pady=5)
        self.entry_x_final = tk.Entry(self, textvariable=self.x_final)
        self.entry_x_final.pack(pady=5)
        
        tk.Label(self, text="Posición final (y):").pack(pady=5)
        self.entry_y_final = tk.Entry(self, textvariable=self.y_final)
        self.entry_y_final.pack(pady=5)
        
        # Botón para confirmar la configuración e iniciar el mapa
        self.boton_iniciar = tk.Button(self, text="Iniciar", command=self.on_iniciar)
        self.boton_iniciar.pack(pady=20)
        
    def on_iniciar(self):
        # Recolecta los datos y cierra la ventana de configuración
        self.withdraw()
        self.update_idletasks()
        # Abrir la ventana principal del mapa con los valores configurados
        self.master.iniciar_mapa(self.personaje.get(), self.x_inicio.get(), self.y_inicio.get(), self.x_final.get(), self.y_final.get())
        self.destroy()

class InterfazMapa:
    def inicializar_terreno(self, direcion_terreno: str = None) -> NDArray[np.int_]:
        self.ruta_absoluta_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), direcion_terreno)
        print(f"Intentando cargar el mapa desde: {self.ruta_absoluta_mapa}")
        if os.path.exists(self.ruta_absoluta_mapa):
            print("Se encontró el archivo\n")
            try:
                terreno = np.genfromtxt(self.ruta_absoluta_mapa, delimiter=',', dtype=int)
                return terreno
            except ValueError as e:
                raise ValueError(f"Error al leer el archivo de mapa: {e}")
        else:
            raise FileNotFoundError("No se ha encontrado el archivo de mapa. Asegúrate de colocarlo en la misma carpeta que este programa")
    
    def inicializar_decisiones(self, direcion_terreno: str = None, mapa_terreno: NDArray[np.int_] = None) -> NDArray[np.int_]:
        if mapa_terreno is None:
            raise ValueError("No se ha indicado el mapa del terreno")
        if direcion_terreno is None:
            print("No se ha indicado un mapa de decisiones, generando uno en blanco...\n")
            mapa = np.zeros_like(mapa_terreno)
        else:
            self.ruta_absoluta_mapa_decisiones = os.path.join(os.path.dirname(os.path.abspath(__file__)), direcion_terreno)
            print(f"Intentando cargar el mapa de decisiones desde: {self.ruta_absoluta_mapa_decisiones}")
            if os.path.exists(self.ruta_absoluta_mapa_decisiones):
                try:
                    mapa = np.genfromtxt(self.ruta_absoluta_mapa_decisiones, delimiter=',', dtype=int)
                    if mapa_terreno.shape != mapa.shape:
                        raise ValueError("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado")
                except ValueError as e:
                    raise ValueError(f"Error al leer el archivo de decisiones: {e}")
            else:
                raise FileNotFoundError("No se ha encontrado el archivo de decisiones")
        return mapa
    
    def inicializar_mascara(self, direccion_mascara: str = None, x_inicio: int = None, y_inicio: int = None, mapa_terreno: NDArray[np.int_] = None) -> NDArray[np.int_]:
        if mapa_terreno is None:
            raise ValueError("No se ha indicado el mapa del terreno")
        if direccion_mascara is None:
            print("No se ha indicado una máscara para el mapa, generando uno en blanco...\n")

            x_inicio = np.random.randint(0, mapa_terreno.shape[0]) if x_inicio is None else np.clip(x_inicio, 0, mapa_terreno.shape[0] - 1)
            y_inicio = np.random.randint(0, mapa_terreno.shape[1]) if y_inicio is None else np.clip(y_inicio, 0, mapa_terreno.shape[1] - 1)
            
            mapa_mascara = enmascarar_mapa(self.mapa, self.mapa_decisiones, x_inicio, y_inicio)
        else:
            self.ruta_absoluta_mapa_mascara = os.path.join(os.path.dirname(os.path.abspath(__file__)), direccion_mascara)
            print(f"Intentando cargar el mapa de máscara desde: {self.ruta_absoluta_mapa_mascara}")
            if os.path.exists(self.ruta_absoluta_mapa_mascara):
                mapa_mascara = np.genfromtxt(self.ruta_absoluta_mapa_mascara, delimiter=',', dtype=int)
                if self.mapa.shape != mapa_mascara.shape:
                    raise ValueError("Las dimensiones del mapa 'máscara' no corresponden al del mapa cargado")
            else:
                raise FileNotFoundError("No se ha encontrado el archivo de máscara")
        return mapa_mascara
    
    def inicializar_movimiento(self, direccion_movimiento: str = None, mapa_decisiones: NDArray[np.int_] = None, mapa_terreno: NDArray[np.int_] = None) -> NDArray[np.int_]:
        if mapa_terreno is None:
            raise ValueError("No se ha indicado el mapa del terreno")
        if mapa_decisiones is None:
            raise ValueError("No se ha indicado el mapa de decisiones")
        if direccion_movimiento is None:
            print("No se tiene registro de la posición del agente, generando uno en blanco...\n")
            mapa_movimiento = np.zeros_like(mapa_terreno)
            indices = np.where(mapa_decisiones == 1)
            if indices[0].size > 0:
                self.pos_agente_x, self.pos_agente_y = indices[0][0], indices[1][0]
                print(f"Se encontró la posición inicial en las coordenadas ({self.pos_agente_x}, {self.pos_agente_y})")
                mapa_movimiento[self.pos_agente_x, self.pos_agente_y] = 1
            else:
                print("No se encontró ningún '1' en el arreglo.")
        else:
            ruta_absoluta_mapa_movimiento = os.path.join(os.path.dirname(os.path.abspath(__file__)), direccion_movimiento)
            if os.path.exists(ruta_absoluta_mapa_movimiento):
                mapa_movimiento = np.genfromtxt(ruta_absoluta_mapa_movimiento, delimiter=',', dtype=int)
                if mapa_terreno.shape != mapa_movimiento.shape:
                    raise ValueError("Las dimensiones del mapa de movimiento no corresponden al del mapa cargado")
            else:
                raise FileNotFoundError("No se ha encontrado el archivo de movimiento")
        return mapa_movimiento

    def crear_botones_personajes(self):
        # Crear un label para indicar la selección de personaje
        label = tk.Label(self.root, text="Selecciona tu personaje:")
        label.pack()
        for personaje, valor in personajes.items():
            boton = tk.Button(self.root, text=personaje, command=lambda p=personaje: self.seleccionar_personaje(p))
            boton.pack(pady=5)
    def seleccionar_personaje(self, personaje):
        self.personaje_seleccionado = personaje
        messagebox.showinfo("Personaje seleccionado", f"Has seleccionado a {personaje}")
        print(f"Personaje seleccionado: {self.personaje_seleccionado}")

    def obtener_personaje_seleccionado(self):
        return self.personaje_seleccionado
    
    def __init__(self, root, ruta_mapa:str = None, ruta_mapa_decisiones: str = None, ruta_mapa_mascara: str = None, ruta_mapa_movimiento: str = None, x_inicio: int = None, y_inicio: int = None):
        self.root = root
        self.personaje_seleccionado = None 
        self.root.title("Interfaz de Mapas")
        self.crear_botones_personajes()

        # Tamaño de las celdas de la cuadrícula
        self.cell_size = 20
        
# ----------- Generar y dibujar mapas iniciales ------------------------------------------
        # Inicializando mapa de terreno
        self.mapa = self.inicializar_terreno(ruta_mapa)

        # Inicializando mapa de decisiones
        self.mapa_decisiones = self.inicializar_decisiones(ruta_mapa_decisiones, self.mapa)

        # Inicializando mapa máscara
        self.mapa_mascara = self.inicializar_mascara(ruta_mapa_decisiones, x_inicio, y_inicio, self.mapa)
        
        # Iniciaizando mapa de movimiento
        self.mapa_movimiento = self.inicializar_movimiento(ruta_mapa_movimiento, self.mapa_decisiones, self.mapa)
        
        # Crear el lienzo donde se dibujarán las cuadrículas
        self.canvas = Canvas(root, width=self.mapa.shape[0] * self.cell_size, height=self.mapa.shape[1] * self.cell_size)
        self.canvas.pack()
        self.controles = tk.Tk()

        self.bttn_arriba = tk.Button(self.controles, text='^', command=lambda: self.actualizar_posicion('arriba'))
        self.bttn_abajo = tk.Button(self.controles, text='v', command=lambda: self.actualizar_posicion('abajo'))
        self.bttn_izquierda = tk.Button(self.controles, text='<-', command=lambda: self.actualizar_posicion('izquierda'))
        self.bttn_derecha = tk.Button(self.controles, text='->', command=lambda: self.actualizar_posicion('derecha'))

        self.bttn_arriba.grid(row=0, column=1)
        self.bttn_abajo.grid(row=1, column=1)
        self.bttn_izquierda.grid(row=1, column=0)
        self.bttn_derecha.grid(row=1, column=2)

        self.root.bind('<Up>', lambda event: self.actualizar_posicion('arriba'))
        self.root.bind('<Down>', lambda event: self.actualizar_posicion('abajo'))
        self.root.bind('<Left>', lambda event: self.actualizar_posicion('izquierda'))
        self.root.bind('<Right>', lambda event: self.actualizar_posicion('derecha'))

        self.dibujar_mapa()

    def actualizar_posicion(self, direccion):
        # Llamar a mover_agente para obtener la nueva posición
        nueva_x, nueva_y = mover_agente(self.mapa, self.mapa_decisiones, self.mapa_mascara, self.mapa_movimiento, self.pos_agente_x, self.pos_agente_y, direccion, self.personaje_seleccionado)
        # print('*' * 50)

        # Actualizar las coordenadas del agente
        self.pos_agente_x, self.pos_agente_y = nueva_x, nueva_y

        # Redibujar el mapa para reflejar el movimiento
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
    root.title("Selección de Personaje")
    root.geometry("300x200")

    # Crear una instancia de la interfaz
    interfaz = InterfazMapa(root, ruta_mapa=MAPA_TERRENO, ruta_mapa_decisiones=MAPA_DECISIONES, ruta_mapa_mascara=MAPA_MASCARA, ruta_mapa_movimiento=MAPA_MOVIMIENTO)

    # Iniciar el loop de Tkinter
    root.mainloop()
