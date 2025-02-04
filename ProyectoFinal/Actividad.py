class Actividad():
    nombre = ""
    frecuencia = 0.0
    intensidad = 0.0
    maximoPermisible = 0.0
    
    def __init__(self,intensidad, frecuencia, nombre, maximoPermisible):
        self.intensidad = intensidad
        self.frecuencia = frecuencia
        self.nombre = nombre
        self.maximoPermisible = maximoPermisible