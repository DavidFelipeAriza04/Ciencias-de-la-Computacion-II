class Material():
    coeficienteAbsorcion = {}
    nombre = ""
    color = ""

    def __init__(self, coeficienteAbsorcion, nombre,color):
        self.coeficienteAbsorcion = coeficienteAbsorcion
        self.nombre = nombre
        self.color = color