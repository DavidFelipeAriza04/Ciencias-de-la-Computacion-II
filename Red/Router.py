import random

class Router:
    def __init__(self, name, ancho_banda, conexiones):
        self.name = name
        self.ancho_banda = ancho_banda
        self.conexiones = conexiones
    
    def caido(self):
        caido = random.random()
        # print(caido)
        if  caido <0.2:
            return 0
        return 1