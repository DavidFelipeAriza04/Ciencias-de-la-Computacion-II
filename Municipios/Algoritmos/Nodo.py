class Nodo:
    def __init__(self, estado, padre, accion, heuristica):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.heuristica = heuristica

    def __lt__(self, other):
        return self.heuristica < other.heuristica



class Pueblo():
    def __init__(self,nombre,latitud,longitud,heuristica,coordenadas):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.heuristica = heuristica
        self.x, self.y = coordenadas


        