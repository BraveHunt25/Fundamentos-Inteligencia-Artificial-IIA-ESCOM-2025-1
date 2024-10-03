# Hernández Jiménez Erick Yael
# Laboratorio 1 de la materia Fundamentos de Inteligencia Artificial
# Este archivo integra las funciones lógicas necesarias para su posterior impresión 
# gráfica con Tkinter en el archivo `Lab_1-2.py`
import os                           # Para acceder a las rutas y a los archivos
import numpy as np                  # Para manipular arreglos multidimensionales
from numpy.typing import NDArray    # Para reconocer las propiedades de los arreglos

# Ruta del archivo de los mapas
ruta_mapa: str = "mapa_1.txt"
ruta_mapa_decisiones: str = None #"mapa_decisiones_1.txt"
ruta_mapa_mascara: str = None
ruta_mapa_movimiento: str = None

personajes = {
    'humano': 0,
    'mono': 1,
    'pulpo': 2,
    'piegrande': 3
}

terrenos = {
    'montaña': 0,
    'tierra': 1,
    'agua': 2,
    'arena': 3,
    'bosque': 4,
    'pantano': 5,
    'nieve': 6
}

desplazamientos = {
    'montaña': {
        'pie-grande': 15
    },
    'tierra': {
        'humano': 1,
        'mono': 2,
        'pulpo': 2,
        'pie-grande': 4
    },
    'agua': {
        'humano': 2,
        'mono': 4,
        'pulpo': 1
    },
    'arena': {
        'humano': 3,
        'mono': 3
    },
    'bosque': {
        'humano': 4,
        'mono': 1, 
        'pulpo': 3,
        'pie-grande': 4
    },
    'pantano': {
        'humano': 5,
        'mono': 5,
        'pulpo': 2,
        'pie-grande': 5
    },
    'nieve': {
        'humano': 5,
        'pie-grande': 3
    }
}

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
    desenmascarar_celda(mascara, pos_ini_x, pos_ini_y)
    mapa_decisiones[pos_ini_x][pos_ini_y] = 1
    return mascara

# Definición de la función para enmascara una celda
def enmascarar_celda(mapa_mascara: NDArray[np.int_], pos_x: int, pos_y: int) -> None:
    mapa_mascara[pos_x][pos_y] = 0
    return

# Definición de la función para desenmascarar una celda
def desenmascarar_celda(mapa_mascara: NDArray[np.int_], pos_x: int, pos_y: int) -> None:
    # Asegurarse de que las posiciones iniciales estén dentro de los límites del mapa
    pos_x = np.clip(pos_x, 0, mapa_mascara.shape[0] - 1)
    pos_y = np.clip(pos_y, 0, mapa_mascara.shape[1] - 1)
    
    # Lista de desplazamientos (x, y) para los vecinos (arriba, abajo, izquierda, derecha)
    vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Desenmascarar a los vecinos
    for dx, dy in vecinos:
        vecino_x = pos_x + dx
        vecino_y = pos_y + dy
        
        # Verificar que el vecino está dentro de los límites del mapa
        if 0 <= vecino_x < mapa_mascara.shape[0] and 0 <= vecino_y < mapa_mascara.shape[1]:
            if mapa_mascara[vecino_x, vecino_y] != 2:  # No sobrescribir si ya es 2
                mapa_mascara[vecino_x, vecino_y] = 1
    
    # Marcar la celda actual como 2
    mapa_mascara[pos_x, pos_y] = 2
    
    return

# Definición de la función para mover al agente
def mover_agente(mapa: NDArray[np.int_], mapa_decisiones: NDArray[np.int_], mapa_mascara: NDArray[np.int_], mapa_movimiento: NDArray[np.int_], pos_x: int, pos_y: int, direccion: str, personaje: str):
    # Definir las direcciones
    movimientos = {
        'arriba': (-1, 0),
        'abajo': (1, 0),
        'izquierda': (0, -1),
        'derecha': (0, 1)
    }
    
    if direccion not in movimientos:
        print("Dirección inválida.")
        return pos_x, pos_y  # Retorna a la posición original si la dirección es inválida
    
    dx, dy = movimientos[direccion]
    nueva_x = pos_x + dx
    nueva_y = pos_y + dy

    # Comprueba los límites del mapa
    if nueva_x < 0 or nueva_x >= mapa.shape[0] or nueva_y < 0 or nueva_y >= mapa.shape[1]:
        print("Movimiento fuera de límites.")
        return pos_x, pos_y  # Retorna a la posición original si el movimiento es fuera de los límites

    # Comprueba si el movimiento es accesible
    if mapa_decisiones[nueva_x, nueva_y] not in range(0, 3):  # Véase la representación del mapa de decisiones
        print("Movimiento no accesible.")
        return pos_x, pos_y  # Retorna a la posición original si no es accesible
    
    # Obtiene el tipo de terreno en la nueva posición
    tipo_terreno = mapa[nueva_x, nueva_y]
    if tipo_terreno not in terrenos.values():
        print("Terreno inválido.")
        return pos_x, pos_y  # Retorna si el terreno no es válido

    # Verificar la movilidad del personaje en el terreno
    movilidad_personaje = desplazamientos[terrenos[tipo_terreno]][personaje]
    if movilidad_personaje is None:
        print(f"El personaje '{personaje}' no puede moverse en el terreno '{list(terrenos.keys())[list(terrenos.values()).index(tipo_terreno)]}'.")
        return pos_x, pos_y

    # Actualiza las posiciones en los mapas
    mapa_movimiento[pos_x, pos_y] = 0  # Limpiar la posición anterior
    mapa_movimiento[nueva_x, nueva_y] = 1  # Establecer la nueva posición

    # Actualiza el mapa de decisiones
    if mapa_decisiones[nueva_x, nueva_y] != 1:
        mapa_decisiones[nueva_x, nueva_y] = 2  # Marca como visitado
    
    # Desenmascara la nueva posición
    desenmascarar_celda(mapa_mascara, nueva_x, nueva_y)

    # Retorna la nueva posición
    return nueva_x, nueva_y 


# Los archivos de mapa serán aquellos que indiquen el terreno
# o entorno en el que se envolverá el agente.
# Adicionalmente se creará un archivo de texto espejo que 
# indicará la información que vaya recolectando el agente
# como mapa de decisiones
# Las relaciones son las siguientes:
# - 0 = Lugares que no ha visitado
# - 1 = Punto inicial
# - 2 = Lugares ya visitados
# - 3 = Lugares donde se hizo una decisión
# - 4 = Punto final
# Aunado a ello, se agregará una capa 'máscara' que contendrá
# la información de lo que el agente podrá ver o la
# 'disponibilidad de visibilidad'. Las relaciones son las siguientes:
# - 0 = No visible ni accesible
# - 1 = No visible pero accesible
# - 2 = Visible y accesible
# - 3 = Visible pero no accesible (esta opción se agrega para completar
# todos los casos posibles pero inicialmente no se tiene planeado su uso)

# Declaración inicial de los mapas
contador_pasos: int = 0
# mapa_decisiones: NDArray[np.int_]
# mapa_mascara: NDArray[np.int_]
# mapa_movimiento: NDArray[np.int_]
# mapa: NDArray[np.int_]
# pos_agente_x: int
# pos_agente_y: int
personaje: int

# Búsqueda de archivo del mapa
# ruta_absoluta_mapa = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa)
# if os.path.exists(ruta_absoluta_mapa):
#     print("Se encontró el archivo\n")
# else:
#     print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa\n")
#     
# Conversión de archivo a arreglo numpy
# mapa = np.genfromtxt(ruta_absoluta_mapa, delimiter=',', dtype=int)
# Impresión de mapa
# print(mapa, "\n")

# Búsqueda o creación de mapa de decisiones
# if ruta_mapa_decisiones is None:
#     print("No se ha indicado un mapa de decisiones, generando uno en blanco...\n")
#     mapa_decisiones = np.zeros_like(mapa)
#     print("El mapa de decisiones se llena con ceros\n")
#     # print(mapa_decisiones, "\n")
# else:
#     ruta_absoluta_mapa_decisiones = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_decisiones)
#     if os.path.exists(ruta_absoluta_mapa_decisiones):
#         print("Se encontró el archivo\n")
#         mapa_decisiones = np.genfromtxt(ruta_absoluta_mapa_decisiones, delimiter=',', dtype=int)
#         if mapa.shape == mapa_decisiones.shape:
#             print("Mapa cargado y válido\n")
#             # print(mapa_decisiones, "\n")
#         else:
#             print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
#     else:
#         print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
# 
# Búsqueda o creación de máscara
# if ruta_mapa_mascara is None:
#     print("No se ha indicado una máscara para el mapa, generando uno en blanco...\n")
#     mapa_mascara = enmascarar_mapa(mapa, mapa_decisiones, int(input("Ingrese la fila en la que desea iniciar\n")), int(input("Ingrese la columna en la que desea iniciar\n")))
#     print("La máscara para el mapa ha sido creado:\n")
#     # print(mapa_mascara, "\n")
# else:
#     ruta_absoluta_mapa_mascara = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_mascara)
#     if os.path.exists(ruta_absoluta_mapa_mascara):
#         print("Se encontró el archivo\n")
#         mapa_mascara = np.genfromtxt(ruta_absoluta_mapa_mascara, delimiter=',', dtype=int)
#         if mapa.shape == mapa_mascara.shape:
#             print("Mapa cargado y válido\n")
#             # print(mapa_mascara, "\n")
#         else:
#             print("Las dimensiones del mapa 'máscara' no corresponden al del mapa cargado\n")
#     else:
#         print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
# 
# Búsqueda o inicialización de posicionamiento
# if ruta_mapa_movimiento is None:
#     print("No se tiene registro de la posición del agente, generando uno en blanco...\n")
#     mapa_movimiento = np.zeros_like(mapa)
#     indices = np.where(mapa_decisiones == 1)
#     if indices[0].size > 0:
#     # Obtener la primera posición
#         pos_agente_x = indices[0][0]
#         pos_agente_y = indices[1][0]
#         print(f"Se encontró la posición inicial en las coordenadas ({pos_agente_x}, {pos_agente_y})")
#         mapa_movimiento[pos_agente_x, pos_agente_y] = 1
#         print("El mapa de decisiones de movilidad se ha iniciado\n")
#     else:
#         print("No se encontró ningún '1' en el arreglo.")
#     print(mapa_movimiento, "\n")
# else:
#     ruta_absoluta_mapa_movimiento = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa_movimiento)
#     if os.path.exists(ruta_absoluta_mapa_movimiento):
#         print("Se encontró el archivo\n")
#         mapa_movimiento = np.genfromtxt(ruta_absoluta_mapa_movimiento, delimiter=',', dtype=int)
#         if mapa.shape == mapa_movimiento.shape:
#             print("Mapa cargado y válido\n")
#             # print(mapa_movimiento, "\n")
#         else:
#             print("Las dimensiones del mapa de decisiones no corresponden al del mapa cargado\n")
#     else:
#         print("No se ha encontrado el archivo, asegúrate de colocarlo en la misma carpeta que este programa")
# 
# print("Imprimiendo los mapas\n", '*' * 20, "Mapa", '*' * 20, "\n", mapa)
# print('*' * 10, "Mapa decisiones", '*' * 10, "\n",  mapa_decisiones)
# print('*' * 10, "Mapa máscara", '*' * 10, "\n",  mapa_mascara)
# print('*' * 10, "Mapa de movimiento", '*' * 10, "\n",  mapa_movimiento)
# print("Generando un punto final aleatorio...\n")
# pos_final_x: int = np.random.randint(0, mapa_decisiones.shape[0])
# pos_final_y: int = np.random.randint(0, mapa_decisiones.shape[1])
# mapa_decisiones[pos_final_x, pos_final_y]
# desenmascarar_celda(mapa_mascara, pos_final_x, pos_final_y)