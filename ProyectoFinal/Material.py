class Material():
    coeficienteAbsorcion = {}
    nombre = ""
    
    def __init__(self, coeficienteAbsorcion, nombre):
        self.coeficienteAbsorcion = coeficienteAbsorcion
        self.nombre = nombre