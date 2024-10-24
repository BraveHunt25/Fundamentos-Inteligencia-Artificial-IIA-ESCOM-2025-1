import numpy as np              
import os
import random
from numpy.typing import NDArray

class Mapa():
    def __init__(self, ancho_x: int = 1, alto_y: int = 1, lim_inf: int = 0, lim_sup: int = 1, ruta_archivo: str = None, contenido: NDArray[np.int_] = None):
        self._lim_inf: int | None = lim_inf
        self._lim_sup: int | None = lim_sup
        self._contenido: NDArray[np.int_] | None = None
        if ruta_archivo:
            ruta_absoluta = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_archivo)
            try:
                if os.path.exists(ruta_absoluta):
                    self._contenido = np.genfromtxt(ruta_absoluta, delimiter=',', dtype=int)
                    self._ancho_x: int = self._contenido.shape[0]
                    self._alto_y: int = self._contenido.shape[1]
                else:
                    raise FileNotFoundError(f"El archivo {ruta_archivo} no se encontró.")
            except Exception as e:
                print(f"No se pudo iniciar el contenido desde el archivo: {e}")
        elif contenido is not None:
            self._contenido = contenido
            self._ancho_x: int = self._contenido.shape[0]
            self._alto_y: int = self._contenido.shape[1]
        else:
            self._ancho_x: int = ancho_x
            self._alto_y: int = alto_y
            self._contenido = np.random.randint(self._lim_inf, self._lim_sup, size=(self._ancho_x, self._alto_y))
    
    def valor(self, coordenada_x: int, coordenada_y: int) -> int:
        return self._contenido[coordenada_x, coordenada_y]
    
    def vecindad(self, origen_x: int, origen_y: int) -> dict:
        if 0 <= origen_x < self._ancho_x and 0 <= origen_y < self._alto_y:
            vecinos: dict = {}
            desplazamientos: dict = {
                'arriba': (-1, 0),
                'abajo': (1, 0),
                'izquierda': (0, -1),
                'derecha': (0, 1)
            }
            for direccion, (dx, dy) in desplazamientos.items():
                nueva_x: int = origen_x + dx
                nueva_y: int = origen_y + dy
                if 0 <= nueva_x < self._ancho_x and 0 <= nueva_y < self._alto_y:
                    vecinos[direccion] = (nueva_x, nueva_y)

class Terreno(Mapa):
    def __init__(self, ancho_x: int = 1, alto_y: int = 1, lim_inf: int = 0, lim_sup: int = 6, ruta_archivo: str = None):
        super().__init__(ancho_x=ancho_x, alto_y=alto_y, lim_inf=lim_inf, lim_sup=lim_sup, ruta_archivo=ruta_archivo)
        self._costos_movimientos: dict = {
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

        self._terrenos = {
            0: 'montaña',
            1: 'tierra',
            2: 'agua',
            3: 'arena',
            4: 'bosque',
            5: 'pantano',
            6: 'nieve'
        }

    def terreno(self, pos_x: int = 0, pos_y: int = 0) -> str:
        if 0 <= pos_x < self._ancho_x and 0 <= pos_y < self._alto_y:
            return self._terrenos.get(self._contenido[pos_x, pos_y])
        else:
            return None
        
    def se_puede_posicionar(self, pos_x: int, pos_y: int, personaje: str = "humano") -> bool:
        if 0 <= pos_x < self._ancho_x and 0 <= pos_y < self._alto_y:
            if self._contenido[pos_x, pos_y] not in self._terrenos[self._contenido[pos_x, pos_y]] or personaje not in self._costos_movimientos[self._contenido[pos_x, pos_y]]:
                return False
            else:
                return True
            
class Decisiones(Mapa):
    '''
    0 = Lugares que no ha visitado
    1 = Punto inicial
    2 = Lugares ya visitados
    3 = Lugares donde se hizo una decisión
    4 = Punto final
    '''
    def __init__(self, ancho_x: int = 1, alto_y: int = 1, lim_inf: int = 0, lim_sup: int = 4, ruta_archivo: str = None, pos_ini_x: int = None, pos_ini_y: int = None, pos_fin_x: int = None, pos_fin_y: int = None):
        super().__init__(ancho_x, alto_y, lim_inf, lim_sup, ruta_archivo)
        if ruta_archivo is None:
            self._contenido = np.zeros_like(dtype=int, shape=(ancho_x, alto_y))
            if pos_ini_x is None: pos_ini_x = np.random.randint(0, self._contenido.shape[0])
            if pos_ini_y is None: pos_ini_y = np.random.randint(0, self._contenido.shape[1])
            if pos_fin_x is None: pos_fin_x = np.random.randint(0, self._contenido.shape[0])
            if pos_fin_y is None: pos_fin_y = np.random.randint(0, self._contenido.shape[1])
            self._contenido[pos_ini_x, pos_ini_y] = 1
            self._contenido[pos_fin_x, pos_fin_y] = 4

    def vecindad(self, origen_x: int, origen_y: int, personaje: str = "humano") -> dict:
        if 0 <= origen_x < self._ancho_x and 0 <= origen_y < self._alto_y:
            vecinos: dict = {}
            desplazamientos: dict = {
                'arriba': (-1, 0),
                'abajo': (1, 0),
                'izquierda': (0, -1),
                'derecha': (0, 1)
            }
            for direccion, (dx, dy) in desplazamientos.items():
                nueva_x: int = origen_x + dx
                nueva_y: int = origen_y + dy
                if 0 <= nueva_x < self._ancho_x and 0 <= nueva_y < self._alto_y:
                    vecinos[direccion] = (nueva_x, nueva_y)
    