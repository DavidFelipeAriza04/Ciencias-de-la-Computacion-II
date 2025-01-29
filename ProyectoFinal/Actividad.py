class Actividad():
    nombre = ""
    frecuencia = 0.0
    intensidad = 0.0
    
    def __init__(self,intensidad, frecuencia, nombre):
        self.intensidad = intensidad
        self.frecuencia = frecuencia
        self.nombre = nombre