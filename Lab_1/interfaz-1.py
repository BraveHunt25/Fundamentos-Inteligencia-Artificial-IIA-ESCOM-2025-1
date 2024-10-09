import pygame
import os
import numpy as np
from Lab_1_1 import mover_agente, personajes, terrenos, desplazamientos

pygame.init()

# Tamaño de las celdas del mapa
cell_size = 20

# Inicializando variables globales
opcion_seleccionada = None
personaje_seleccionado = "humano"  # Valor por defecto
pos_agente_x, pos_agente_y = 0, 0  # Posición inicial
pos_final_x, pos_final_y = 0, 0    # Posición final
mapa_actual = "terreno"

# Mapas
mapa_terreno = None
mapa_decisiones = None
mapa_mascara = None
mapa_movimiento = None

def dibujar_botones():
    # Dimensiones de los botones
    boton_ancho = 150
    boton_alto = 50
    espacio_vertical = 20
    
    # Posiciones laterales de los botones
    x_pos = ventana.get_width() - boton_ancho - 20  # Lateral derecho
    y_terreno = 50
    y_decisiones = y_terreno + boton_alto + espacio_vertical

    # Dibujar botón "Mapa de Terreno"
    pygame.draw.rect(ventana, (200, 200, 200), (x_pos, y_terreno, boton_ancho, boton_alto))
    texto_terreno = pygame.font.Font(None, 24).render("Mapa de Terreno", True, (0, 0, 0))
    ventana.blit(texto_terreno, (x_pos + 10, y_terreno + 15))

    # Dibujar botón "Mapa de Decisiones"
    pygame.draw.rect(ventana, (200, 200, 200), (x_pos, y_decisiones, boton_ancho, boton_alto))
    texto_decisiones = pygame.font.Font(None, 24).render("Mapa de Decisiones", True, (0, 0, 0))
    ventana.blit(texto_decisiones, (x_pos + 10, y_decisiones + 15))

    # Detección de clic en los botones
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Si se clickea el botón "Mapa de Terreno"
    if x_pos < mouse[0] < x_pos + boton_ancho and y_terreno < mouse[1] < y_terreno + boton_alto and click[0]:
        global mapa_actual
        mapa_actual = "terreno"
    
    # Si se clickea el botón "Mapa de Decisiones"
    if x_pos < mouse[0] < x_pos + boton_ancho and y_decisiones < mouse[1] < y_decisiones + boton_alto and click[0]:
        mapa_actual = "decisiones"

# Función para inicializar el terreno
def inicializar_terreno(ruta_mapa):
    global mapa_terreno
    ruta_absoluta = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_mapa)
    if os.path.exists(ruta_absoluta):
        mapa_terreno = np.genfromtxt(ruta_absoluta, delimiter=',', dtype=int)
    else:
        raise FileNotFoundError(f"El archivo {ruta_mapa} no se encontró.")

# Funciones para inicializar las capas (decisiones, máscara, movimiento)
def inicializar_capas():
    global mapa_decisiones, mapa_mascara, mapa_movimiento
    mapa_decisiones = np.zeros_like(mapa_terreno)
    mapa_mascara = np.zeros_like(mapa_terreno)
    mapa_movimiento = np.zeros_like(mapa_terreno)
    
    # Colocar el personaje en la posición inicial
    mapa_movimiento[pos_agente_x, pos_agente_y] = 1

    # Desenmascarar las celdas alrededor del personaje
    desenmascarar_celda(mapa_mascara, pos_agente_x, pos_agente_y)

def desenmascarar_celda(mapa_mascara, x, y):
    # Desenmascarar la celda actual
    mapa_mascara[x, y] = 2
    
    # Desenmascarar las celdas adyacentes (arriba, abajo, izquierda, derecha)
    vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in vecinos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < mapa_mascara.shape[0] and 0 <= nuevo_y < mapa_mascara.shape[1]:
            mapa_mascara[nuevo_x, nuevo_y] = 1

# Función para mover el agente
def mover_personaje(direccion):
    global pos_agente_x, pos_agente_y
    pos_agente_x, pos_agente_y = mover_agente(mapa_terreno, mapa_decisiones, mapa_mascara, mapa_movimiento, pos_agente_x, pos_agente_y, direccion, personaje_seleccionado)

# Función para dibujar el mapa
def dibujar_mapa():
    ventana.fill((0, 0, 0))  # Limpiar pantalla

    # Dibujar el mapa seleccionado
    for x in range(mapa_terreno.shape[0]):
        for y in range(mapa_terreno.shape[1]):
            if mapa_actual == "terreno":
                color = obtener_color(mapa_terreno[x, y], mapa_mascara[x, y])  # Mapa de terreno
            elif mapa_actual == "decisiones":
                color = obtener_color_decisiones(mapa_decisiones[x, y], mapa_mascara[x, y])  # Mapa de decisiones
            pygame.draw.rect(ventana, color, pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size))

            # Dibujar la "O" en la posición del personaje
            if mapa_movimiento[x, y] == 1:
                fuente = pygame.font.Font(None, int(cell_size * 0.8))
                texto = fuente.render('O', True, (255, 0, 0))
                ventana.blit(texto, (y * cell_size + cell_size // 4, x * cell_size + cell_size // 8))

    # Dibujar los botones para cambiar de mapa
    dibujar_botones()

def obtener_color_decisiones(valor_decisiones, visible):
    colores_decisiones = {
        0: (100, 100, 100),  # No visitado
        1: (0, 255, 0),      # Punto inicial
        2: (255, 255, 0),    # Visitado
        3: (255, 0, 0),      # Punto de decisión
        4: (0, 0, 255)       # Punto final
    }
    if visible == 0:
        return (0, 0, 0)  # No visible
    return colores_decisiones.get(valor_decisiones, (0, 0, 0))

# Función para obtener el color de una celda del mapa
def obtener_color(valor_terreno, visible):
    colores_terrenos = {
        0: (128, 128, 128),  # Montaña
        1: (0, 255, 0),      # Tierra
        2: (0, 0, 255),      # Agua
        3: (255, 255, 0),    # Arena
        4: (0, 128, 0),      # Bosque
        5: (139, 69, 19),    # Pantano
        6: (255, 255, 255)   # Nieve
    }
    if visible == 0:
        return (0, 0, 0)  # No visible
    return colores_terrenos.get(valor_terreno, (0, 0, 0))

# Función para seleccionar personaje (migrada de Tkinter a Pygame)
def menu_personajes():
    global personaje_seleccionado, pos_agente_x, pos_agente_y, pos_final_x, pos_final_y
    # Opciones de personajes
    opciones = ["humano", "mono", "pulpo", "pie-grande"]

    # Obtener las dimensiones actuales de la ventana
    ventana_ancho = ventana.get_width()
    ventana_alto = ventana.get_height()

    # Definir el tamaño del texto y el espaciado dinámico
    fuente = pygame.font.Font(None, int(ventana_alto * 0.05))
    boton_ancho = int(ventana_ancho * 0.4)
    boton_alto = int(ventana_alto * 0.1)
    espacio_vertical = int(ventana_alto * 0.1)

    # Dibujar el menú de personajes
    for i, personaje in enumerate(opciones):
        x_pos = (ventana_ancho - boton_ancho) // 2
        y_pos = espacio_vertical + i * (boton_alto + espacio_vertical)
        texto = fuente.render(personaje.capitalize(), True, (0, 0, 0))
        pygame.draw.rect(ventana, (255, 255, 255), (x_pos, y_pos, boton_ancho, boton_alto))
        ventana.blit(texto, (x_pos + 10, y_pos + 10))

    # Detección de clic para seleccionar el personaje
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for i, personaje in enumerate(opciones):
        x_pos = (ventana_ancho - boton_ancho) // 2
        y_pos = espacio_vertical + i * (boton_alto + espacio_vertical)
        if x_pos < mouse[0] < x_pos + boton_ancho and y_pos < mouse[1] < y_pos + boton_alto and click[0]:
            personaje_seleccionado = personaje

            # Puntos iniciales y finales opcionales (si no, generar aleatorios)
            pos_agente_x = int(input("Ingrese la coordenada X inicial (o presione Enter para aleatorio): ") or np.random.randint(0, mapa_terreno.shape[0]))
            pos_agente_y = int(input("Ingrese la coordenada Y inicial (o presione Enter para aleatorio): ") or np.random.randint(0, mapa_terreno.shape[1]))
            pos_final_x = int(input("Ingrese la coordenada X final (o presione Enter para aleatorio): ") or np.random.randint(0, mapa_terreno.shape[0]))
            pos_final_y = int(input("Ingrese la coordenada Y final (o presione Enter para aleatorio): ") or np.random.randint(0, mapa_terreno.shape[1]))

            return False  # Ocultar el menú después de seleccionar

    return True


# Inicialización del terreno
inicializar_terreno("mapa_1.txt")

# Configuración básica de la ventana de Pygame
ancho = mapa_terreno.shape[0] * cell_size + 170
alto = mapa_terreno.shape[1] * cell_size
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Agentes")

# Inicialización de las capas
inicializar_capas()

# Ciclo principal
jugando = True
menu_visible = True

while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

        # Teclas de dirección para mover al agente
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mover_personaje('arriba')
            elif event.key == pygame.K_DOWN:
                mover_personaje('abajo')
            elif event.key == pygame.K_LEFT:
                mover_personaje('izquierda')
            elif event.key == pygame.K_RIGHT:
                mover_personaje('derecha')

    if menu_visible:
        menu_visible = menu_personajes()
    else:
        dibujar_mapa()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
