# Hernández Jiménez Erick Yael
# Laboratorio 1 de la materia Fundamentos de Inteligencia Artificial
# Este archivo integra las funciones lógicas necesarias para su posterior impresión 
# gráfica con gamePy en el archivo `interfaz-1.py`
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
    'pie-grande': 3
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
    if mapa_decisiones[nueva_x, nueva_y] not in range(0, 5):  # Véase la representación del mapa de decisiones
        print("Movimiento no accesible.")
        return pos_x, pos_y  # Retorna a la posición original si no es accesible
    
    tipos_terreno = ['montaña', 'tierra', 'agua', 'arena', 'bosque', 'pantano', 'nieve']
    # Obtiene el tipo de terreno en la nueva posición
    tipo_terreno = mapa[nueva_x, nueva_y]
    if tipo_terreno not in terrenos.values():
        print("Terreno inválido.")
        return pos_x, pos_y  # Retorna si el terreno no es válido
    nombre_terreno = tipos_terreno[int(tipo_terreno)]

    # Verificar la movilidad del personaje en el terreno
    if nombre_terreno not in desplazamientos or personaje not in desplazamientos[nombre_terreno]:
        print(f"El personaje '{personaje}' no puede moverse en el terreno '{list(terrenos.keys())[list(terrenos.values()).index(tipo_terreno)]}'.")
        return pos_x, pos_y

    # Actualiza las posiciones en los mapas
    mapa_movimiento[pos_x, pos_y] = 0  # Limpiar la posición anterior
    mapa_movimiento[nueva_x, nueva_y] = 1  # Establecer la nueva posición

    # Actualiza el mapa de decisiones
    if mapa_decisiones[nueva_x, nueva_y] != 1 and mapa_decisiones[nueva_x, nueva_y] != 4:
        # Contador de direcciones válidas
        direcciones_validas = 0
        vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in vecinos:
            nuevo_x, nuevo_y = nueva_x + dx, nueva_y + dy
            if 0 <= nuevo_x < mapa_mascara.shape[0] and 0 <= nuevo_y < mapa_mascara.shape[1]:
                terreno_vecino = mapa[nuevo_x, nuevo_y]  # Obtener el terreno del vecino
                nombre_terreno_vecino = tipos_terreno[int(terreno_vecino)]

                # Verificar si el personaje puede moverse a ese terreno
                costo_movimiento_vecino = desplazamientos.get(nombre_terreno_vecino, {}).get(personaje, None)

                # Si el personaje puede moverse a ese terreno (costo de movimiento no es None)
                if costo_movimiento_vecino is not None:
                    direcciones_validas += 1

        # Si hay más de 2 direcciones válidas, es un punto de decisión
        if direcciones_validas > 2:
            mapa_decisiones[nueva_x, nueva_y] = 3  # Marcar como punto de decisión
        else:
            mapa_decisiones[nueva_x, nueva_y] = 2  # Marcar como celda visitada
    
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