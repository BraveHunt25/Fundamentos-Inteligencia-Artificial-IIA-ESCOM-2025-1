# Hernández Jiménez Erick Yael
# Laboratorio 1 de la materia Fundamentos de Inteligencia Artificial
import os                           # Para acceder a las rutas y a los archivos
import numpy as np                  # Para manipular arreglos multidimensionales
from numpy.typing import NDArray    # Para reconocer las propiedades de los arreglos

# Ruta del archivo de los mapas
ruta_mapa: str = "mapa_1.txt"
ruta_mapa_decisiones: str = None #"mapa_decisiones_1.txt"
ruta_mapa_mascara: str = None

# Para fines de estandarización toda posición:
# x: filas del arreglo bidimensional (primera posición en las dimensiones)
# y: columnas del arreglo bidimensional (segunda posición en las dimensiones)

# Definición de la función para acceder a los valores del mapa
def valor_celda(arr: NDArray[np.int_], pos_x: int, pos_y: int) -> int:
    value: int = arr[pos_x, pos_y]
    print(f"El valor en la celda {pos_x}, {pos_y} es {value}")
    return value

# Definición de la función que cambia el valor de una celda
def cambiar_valor(arr: NDArray[np.int_], pos_x: int, pos_y: int, new_value: int) -> None:
    if new_value > 4:
        new_value = 4
    prev_value: int = arr[pos_x, pos_y]
    print(f"Cambiando el valor del arreglo en la posición {pos_x}, {pos_y} con valor {prev_value} a {new_value}")
    arr[pos_x, pos_y] = new_value
    if arr[pos_x, pos_y] != prev_value:
        print(f"El arreglo se ha cambiado con éxito a {arr[pos_x, pos_y]}")
        print(arr, "\n")
    else:
        print("No se ha hecho el cambio o se ha cambiado por el mismo valor\n")
    return

# Definición de la función que genera la máscara de un mapa
def enmascarar_mapa(mapa_original: NDArray[np.int_], mapa_decisiones: NDArray[np.int_], pos_ini_x: int, pos_ini_y: int) -> NDArray[np.int_]:
    mascara: NDArray[np.int_] = np.zeros_like(mapa_original)
    pos_ini_x:int = np.clip(pos_ini_x, 0, mapa_original.shape[0] - 1)
    pos_ini_y:int = np.clip(pos_ini_y, 0, mapa_original.shape[1] - 1)
    mascara[pos_ini_x][pos_ini_y] = mapa_original[pos_ini_x][pos_ini_y]
    mapa_decisiones[pos_ini_x][pos_ini_y] = 1
    return mascara

# Definición de la función para enmascara una celda
def enmascarar_celda(mapa_mascara: NDArray[np.int_], pos_x: int, pos_y: int) -> None:
    mapa_mascara[pos_x][pos_y] = 0
    return

# Definición de la función para desenmascarar una celda

# Los archivos de mapa serán aquellos que indiquen el terreno
# o entorno en el que se envolverá el agente.
# Adicionalmente se creará un archivo de texto espejo que 
# indicará la información que vaya recolectando el agente
# Las relaciones son las siguientes:
# - 0 = Lugares que no ha visitado
# - 1 = Punto inicial
# - 2 = Lugares ya visitados
# - 3 = Punto actual
# - 4 = Lugares donde se hizo una decisión

# Declaración inicial de los mapas
mapa: NDArray[np.int_]
mapa_decisiones: NDArray[np.int_]
mapa_mascara: NDArray[np.int_]

# Búsqueda de archivo del mapa
ruta_absoluta_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa)
if os.path.exists(ruta_absoluta_mapa):
    print("Se encontró el archivo\n")
else:
    print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa\n")
    
# Conversión de archivo a arreglo numpy
mapa = np.genfromtxt(ruta_absoluta_mapa, delimiter=',', dtype=int)
# Impresión de mapa
print(mapa, "\n")

# Búsqueda o creación de mapa de decisiones
if ruta_mapa_decisiones is None:
    print("No se ha indicado un mapa de decisiones, generando uno en blanco...\n")
    mapa_decisiones = np.zeros_like(mapa)
    print("El mapa de decisiones se llena con ceros\n", mapa_decisiones, "\n")
else:
    ruta_absoluta_mapa_decisiones = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_decisiones)
    if os.path.exists(ruta_absoluta_mapa):
        print("Se encontró el archivo\n")
        mapa_decisiones = np.genfromtxt(ruta_absoluta_mapa_decisiones, delimiter=',', dtype=int)
        if mapa.shape == mapa_decisiones.shape:
            print("Mapa cargado y válido\n", mapa_decisiones, "\n")
        else:
            print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
    else:
        print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")

# Búsqueda o creación de máscara
if ruta_mapa_mascara is None:
    print("No se ha indicado una máscara para el mapa, generando uno en blanco...\n")
    mapa_mascara = enmascarar_mapa(mapa, mapa_decisiones, int(input("Ingrese la fila en la que desea iniciar\n")), int(input("Ingrese la columna en la que desea iniciar\n")))
    print("La máscara para el mapa ha sido creado:\n", mapa_decisiones, "\n")
else:
    ruta_absoluta_mapa_mascara = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_mascara)
    if os.path.exists(ruta_absoluta_mapa):
        print("Se encontró el archivo\n")
        mapa_decisiones = np.genfromtxt(ruta_absoluta_mapa_decisiones, delimiter=',', dtype=int)
        if mapa.shape == mapa_decisiones.shape:
            print("Mapa cargado y válido\n", mapa_decisiones, "\n")
        else:
            print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
    else:
        print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")