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
                    self._lim_inf: int = np.min(self._contenido)
                    self._lim_sup: int = np.max(self._contenido)
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
    
    # Regresa el valor de la celda en las coordenadas especificadas
    def valor(self, coordenada_x: int, coordenada_y: int) -> int:
        return self._contenido[coordenada_x, coordenada_y]
    
    # Regresa un diccionario con las direcciones y coordenadas de los vecinos de la celda
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
            
            return vecinos
        else:
            print("Posición no válida")

    def __str__(self):
        return f"Contenido:\n{self._contenido}\nEl tamaño es de {self._ancho_x} de ancho por {self._alto_y} de alto.\nLos límites del contenido son ({self._lim_inf}, {self._lim_sup})"

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

    # Regresa el tipo de terreno que es en la posición dada
    def terreno(self, pos_x: int = 0, pos_y: int = 0) -> str:
        if 0 <= pos_x < self._ancho_x and 0 <= pos_y < self._alto_y:
            return self._terrenos.get(self._contenido[pos_x, pos_y])
        else:
            return None
        
    # Indica si el personaje se puede posicionar en la celda
    def se_puede_posicionar(self, pos_x: int, pos_y: int, personaje: str = "humano") -> bool:
        if 0 <= pos_x < self._ancho_x and 0 <= pos_y < self._alto_y:
            if self._contenido[pos_x, pos_y] not in self._terrenos[self._contenido[pos_x, pos_y]] or personaje not in self._costos_movimientos[self._contenido[pos_x, pos_y]]:
                return False
            else:
                return True
            
class Decisiones(Terreno):
    '''
    0 = Lugares que no ha visitado
    1 = Punto inicial
    2 = Lugares ya visitados
    3 = Lugares donde se hizo una decisión
    4 = Punto final
    '''
    def __init__(self, ancho_x = 1, alto_y = 1, lim_inf = 0, lim_sup = 6, ruta_archivo = None, pos_ini_x: int = None, pos_ini_y: int = None, pos_fin_x: int = None, pos_fin_y: int = None):
        super().__init__(ancho_x, alto_y, lim_inf, lim_sup, ruta_archivo)

        if ruta_archivo is None:
            self._contenido = np.zeros(dtype=int, shape=(ancho_x, alto_y))
            if pos_ini_x is None: pos_ini_x = np.random.randint(0, self._contenido.shape[0])
            if pos_ini_y is None: pos_ini_y = np.random.randint(0, self._contenido.shape[1])
            if pos_fin_x is None: pos_fin_x = np.random.randint(0, self._contenido.shape[0])
            if pos_fin_y is None: pos_fin_y = np.random.randint(0, self._contenido.shape[1])
            self._contenido[pos_ini_x, pos_ini_y] = 1
            self._contenido[pos_fin_x, pos_fin_y] = 4
            self._ancho_x: int = self._contenido.shape[0]
            self._alto_y: int = self._contenido.shape[1]
            self._lim_inf: int = np.min(self._contenido)
            self._lim_sup: int = np.max(self._contenido)
            self._pos_ini: tuple = (int(pos_ini_x), int(pos_ini_y))
            self._pos_fin: tuple = (int(pos_fin_x), int(pos_fin_y))
    
    def decidir(self, origen_x: int, origen_y: int, caminos_posibles: int) -> None:
        if caminos_posibles == 0 or caminos_posibles == 1:
            self._contenido[origen_x, origen_y] = 2
        else:
            self._contenido[origen_x, origen_y] = 3
        return

    def __str__(self):
        return f"Contenido:\n{self._contenido}\nEl tamaño es de {self._ancho_x} de ancho por {self._alto_y} de alto.\nLos límites del contenido son ({self._lim_inf}, {self._lim_sup})\nPosición inicial: {self._pos_ini}.\nPosición final {self._pos_fin}."

class Mascara(Mapa):
    '''
    0 = No visible
    1 = Visible
    '''
    def __init__(self, ancho_x = 1, alto_y = 1, lim_inf = 0, lim_sup = 1, ruta_archivo = None, pos_ini_x: int = None, pos_ini_y: int = None):
        super().__init__(ancho_x, alto_y, lim_inf, lim_sup, ruta_archivo)
        if ruta_archivo is None:
            self._contenido = np.zeros(dtype=int, shape=(ancho_x, alto_y))
            if pos_ini_x is not None: 
                pos_ini_x = np.clip(pos_ini_x, a_min=0, a_max=self._ancho_x - 1) 
            else: 
                pos_ini_x = np.random.randint(0, self._contenido.shape[0])
            if pos_ini_y is not None: 
                pos_ini_y = np.clip(pos_ini_y, a_min=0, a_max=self._alto_y - 1)
            else:
                pos_ini_y = np.random.randint(0, self._contenido.shape[1])

            self._contenido[pos_ini_x, pos_ini_y] = 1
            for dx, dy in self.vecindad(pos_ini_x, pos_ini_y).values():
                self._contenido[dx, dy] = 1
            

    def mostrar(self, origen_x: int, origen_y: int) -> None:
        if 0 <= origen_x < self._ancho_x and 0 <= origen_y < self._alto_y:
            self._contenido[origen_x, origen_y] = 1
            for dx, dy in self.vecindad(origen_x, origen_y).values():
                nueva_x: int = dx
                nueva_y: int = dy
                if 0 <= nueva_x < self._contenido.shape[0] and 0 <= nueva_y < self._contenido.shape[1]:
                    self._contenido[dx, dy] = 1
        else:
            print("Posición no válida")
    
    def __str__(self):
        return f"Contenido:\n{self._contenido}\nEl tamaño es de {self._ancho_x} de ancho por {self._alto_y} de alto.\nLos límites del contenido son ({self._lim_inf}, {self._lim_sup})."

class Laberinto(Mapa):
    def __init__(self, ancho_x = 1, alto_y = 1, lim_inf = 0, lim_sup = 1, ruta_archivo_terreno = None, ruta_archivo_decisiones = None, contenido = None, pos_ini_x: int = None, pos_ini_y: int = None, pos_fin_x: int = None, pos_fin_y: int = None):
        self._terreno: Terreno = Terreno(ancho_x, alto_y, lim_inf, lim_sup, ruta_archivo_terreno)
        if pos_ini_x is not None: 
            pos_ini_x = np.clip(pos_ini_x, a_min=0, a_max=self._terreno._ancho_x - 1) 
        else: 
            pos_ini_x = np.random.randint(0, self._terreno._contenido.shape[0])
        if pos_ini_y is not None: 
            pos_ini_y = np.clip(pos_ini_y, a_min=0, a_max=self._terreno._alto_y - 1)
        else:
            pos_ini_y = np.random.randint(0, self._terreno._contenido.shape[1])
        if pos_fin_x is not None:
            pos_fin_x = np.clip(pos_fin_x, a_min=0, a_max=self._terreno._ancho_x - 1)
        if pos_fin_y is not None:
            pos_fin_y = np.clip(pos_fin_y, a_min=0, a_max=self._terreno._alto_y - 1)

        self._decisiones: Decisiones = Decisiones(self._terreno._contenido.shape[0], self._terreno._contenido.shape[1], self._terreno._lim_inf, self._terreno._lim_sup, ruta_archivo_decisiones, pos_ini_x, pos_ini_y, pos_fin_x, pos_fin_y)

        self._mascara: Mascara = Mascara(self._terreno._ancho_x, self._terreno._alto_y, self._terreno._lim_inf, self._terreno._lim_sup, None, self._decisiones._pos_ini[0], self._decisiones._pos_ini[1])

        self._pos_actual: tuple = (pos_ini_x, pos_ini_y)

    def mover_agente(self, direccion: str) -> None:
        direcciones: dict = {
            'arriba': (-1, 0),
            'abajo': (1, 0),
            'izquierda': (0, -1),
            'derecha': (0, 1)
        }
        if direccion not in direcciones.keys():
            print("La dirección no es válida")
        else:
            nueva_direccion: tuple = (self._pos_actual[0] + direcciones[direccion][0], self._pos_actual[1] + direcciones[direccion][1])
            nueva_direccion = np.clip(nueva_direccion, [0,0], [self._terreno._ancho_x, self._terreno._alto_y])
            self._pos_actual = nueva_direccion
            self._mascara.mostrar(nueva_direccion[0], nueva_direccion[1])
            


    def __str__(self):
        return f"{'*'*20} Terreno: {'*'*20}\n{self._terreno._contenido}\n{'*'*20} Decisiones: {'*'*20}\n{self._decisiones._contenido}\n{'*'*20} Máscara: {'*'*20}\n{self._mascara._contenido}"

if __name__ == '__main__':
    laberinto: Laberinto = Laberinto(ruta_archivo_terreno="mapa_1.txt")
    print(laberinto)
    laberinto.mover_agente("arriba")
    laberinto.mover_agente("izquierda")
    laberinto.mover_agente("abajo")
    laberinto.mover_agente("derecha")
    print(laberinto._mascara)