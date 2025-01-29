from Material import Material

class Superficie():
    material = None
    salonesSeparados=[]
    tipoSuperficie=""
    
    def __init__(self, material, salonesSeparados, tipoSuperficie):
        self.material = material
        self.salonesSeparados = salonesSeparados
        self.tipoSuperficie = tipoSuperficie