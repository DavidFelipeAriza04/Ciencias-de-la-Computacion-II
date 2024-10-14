import random as rd

class Router:
    def __init__(self, name, ancho_banda, conexiones):
        self.name = name
        self.ancho_banda = ancho_banda
        self.conexiones = conexiones
    
    def caido(self, prob_caida):
        caido = rd.random()
        # print(caido)
        if  caido < prob_caida:
            return 0
        return 1
    
    def id(self):
        return int(self.name[-1])

BIG_NUM = 1000000