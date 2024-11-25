# Hernández Jiménez Erick Yael
# Sanchez Flores María Fernanda
# Laboratorio 3 de la materia Fundamentos de Inteligencia Artificial ESCOM IIA 2025-1
# Este archivo agrega la clase y los métodos necesarios para cargar datos desde un archivo de texto plano ".txt"
# con el formato de un archivo ".csv", así como ejemplifica su uso si se ejectuta como archivo principal.
class Dataset():
    r'''
    Almacena el contenido y datos básicos relevantes del conjunto de datos.
    '''
    def __init__(self, filepath: str, sep: str = ",", content: list[list] = []):
        r'''
        - **filepath: str**: Ruta hacia el archivo desde el cuál se cargarán los datos
        - **sep: char**: Caractér que separa el contenido de cada campo.
        '''
        # Carga de datos
        self.content: list[list] = [] 
        r'''
        Matriz con el contenido del dataset
        '''
        if filepath:
            with open(filepath, "r") as file:
                for line in file:
                    row: list = []
                    element: str = ""
                    for char in line:
                        if char != sep and char != "\n":
                            element += char
                        else:
                            if element:
                                try:
                                    es_entero: int = int(element)
                                    row.append(es_entero)
                                except:
                                    try:
                                        es_flotante: float = float(element)
                                        row.append(es_flotante)
                                    except:
                                        row.append(element)
                                element = ""
                    if element:
                        try:
                            es_entero: int = int(element)
                            row.append(es_entero)
                        except:
                            try:
                                es_flotante: float = float(element)
                                row.append(es_flotante)
                            except:
                                row.append(element)
                        element = ""
                    self.content.append(row)
            for row in self.content:
                if not row:
                    self.content.remove(row)
        elif content:
            self.content = content
        
        # Definición de dataset vacío
        self.empty: bool = 1
        r'''
        Indicador de dataset vacío
        '''
        for row in self.content:
            if row:
                self.empty = 0
                break
        
        # Definición de dimensiones del dataset
        self.shape: tuple[int] = (len(self.content[0]), len(self.content))
        r'''
        Dimensiones del dataset (columnas, filas)
        '''

        # Definición del número de atributos
        self.attributes: list[str] = []
        r'''
        Lista con los tipos de datos de las columnas
        '''
        for element in self.content[0]:
            if isinstance(element, int):
                self.attributes.append("int")
            elif isinstance(element, float):
                self.attributes.append("float")
            elif isinstance(element, str):
                self.attributes.append("str")
            else:
                self.attributes.append("unknown")  # Para casos de tipos no previstos

    def categorize(self, column: int) -> list:
        r'''
        - **column: int**: índice de la columna que se categorizará
        
        Si la columna `column` es...
        - *cualitativa*: regresará un arreglo con todas las categorías distintas encontradas.
        - *cuantitativa*: regresará un arreglo con los valores `[min, max, media]`
        - *desconocida*: regresa un arreglo vacío
        '''
        res: list = []
        if 0 <= column <= self.shape[0]:
            if self.attributes[column] == "int" or self.attributes[column] == "float":
                min: float = self.content[0][column]
                max: float = self.content[0][column]
                sum: float = 0
                for row in self.content:
                    sum += row[column]
                    if min > row[column]:
                        min = row[column]
                    if max < row[column]:
                        max = row[column]
                res = [min, max, sum/self.shape[1]]
            elif self.attributes[column] == "str":
                for row in self.content:
                    if row[column] not in res:
                        res.append(row[column])
            else:
                res = ["Unknown"]
        else:
            print("Column index out of range")
        return res
    
    def subset(self, indexes: list[int], sorted: bool = 1) -> 'Dataset':
        r'''
        - **indexes: list[int]|set[int]**: índices de columnas que formarán parte del subarreglo.
        - **sorted: bool**: ordenará los índices (1) o construirá el dataset tal como el iterable lo indique(0).
        '''
        indexes.sort() if sorted else indexes

        if any(index < 0 or index >= self.shape[0] for index in indexes):
            raise IndexError("One or more column indexes are out of range.")
    
        matrix: list[list] = []

        new_row: list = []
        for row in self.content:
            new_row = [row[index] for index in indexes]
            matrix.append(new_row)
        return Dataset(filepath=None, content=matrix)
        

if __name__ == "__main__":
    direccion_archivo: str = "datasets/iris.txt"
    datset: Dataset = Dataset(direccion_archivo, ",")
    for row in datset.content:
        print(row)
    print(datset.shape)
    print(datset.attributes)
    print(datset.categorize(0))

    for row in datset.subset([0,1,4,3], sorted=0).content:
        print(row)
    print(datset.subset([0,1,4,3], sorted=0).shape)
    print(datset.subset([0,1,4,3], sorted=0).attributes)
    print(datset.subset([0,1,4,3], sorted=0).categorize(0))
