from collections import deque
from typing import Optional

class Nodo:
    def __init__(self, x: int, y: int, direcciones: list[str], padre: Optional['Nodo'] = None) -> None:
        DIRECCIONES_VALIDAS = {'arriba', 'abajo', 'izquierda', 'derecha'}
        if not all(dir in DIRECCIONES_VALIDAS for dir in direcciones):
            raise ValueError("Direcciones inválidas proporcionadas")
        self._hijos: list[Nodo] = []
        self._x: int = x
        self._y: int = y
        self._direcciones: list[str] = direcciones
        self._nodo_actual: Nodo = self
        self._padre: Nodo = padre
    
    def agregar_hijo(self, nuevo_hijo: 'Nodo') -> None:
        self._hijos.append(nuevo_hijo)

    def imprimir(self, nivel: int = 0) -> None:
        print('   '*nivel, f"|-({self._x}, {self._y}). Direcciones: {self._direcciones}\n")
        for hijo in self._hijos:
            hijo.imprimir(nivel+1)

    def buscar(self, x: int, y: int) -> 'Nodo':
        cola = deque([self])

        while cola:
            nodo_actual = cola.popleft()
            if nodo_actual._x == x and nodo_actual._y == y:
                return nodo_actual
            cola.extend(nodo_actual._hijos)

        return None

    
    def agregar_hijo(self, nueva_x: int, nueva_y: int, direcciones: list[str], direccion_anterior: str) -> None:
        contrarias = {
            'arriba': "abajo",
            'abajo': "arriba",
            'izquierda': "derecha",
            'derecha': "izquierda"
        }

        try:
            # Buscamos si la posición ya existe
            nodo_existente: Nodo = self.buscar(nueva_x, nueva_y)

            # Si existe el nodo, situamos el nodo actual al encontrado
            if nodo_existente: 
                self._nodo_actual = nodo_existente
                raise ValueError(f"Un nodo ya existe en la posición ({nueva_x}, {nueva_y})")

            # Si no, se lo agregamos al nodo actual
            else:
                nuevo_nodo: Nodo = Nodo(nueva_x, nueva_y, direcciones, self._nodo_actual)
                self._nodo_actual._direcciones.remove(direccion_anterior)
                nuevo_nodo._direcciones.remove(contrarias.get(direccion_anterior))
                self._nodo_actual._hijos.append(nuevo_nodo)
                self._nodo_actual = nuevo_nodo
        except ValueError as e:
            print(f"Error: {e}")
        return