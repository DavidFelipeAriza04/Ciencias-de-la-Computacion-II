import math
from Actividad import Actividad

# Frecuencias estándar para coeficientes de absorción
frecuencias_estandar = [100, 250, 500, 1000, 2000, 4000]

def aproximar_frecuencia(frecuencia):
    """
    Aproxima una frecuencia dada a las frecuencias estándar.
    """
    return min(frecuencias_estandar, key=lambda x: abs(x - frecuencia))

class Salon:
    actividad = None
    habitable = ""
    salonesAdyacentes = []
    piso = 0
    id = 0

    def __init__(self, actividad, salonesAdyacentes, piso, id):
        self.actividad = actividad
        self.salonesAdyacentes = salonesAdyacentes
        self.piso = piso
        self.id = id
    
    def CalcularRuido(self, superficies):
        intensidadesEntrantes = []
        frecuenciasEntrantes = []
        for salon in self.salonesAdyacentes:
            intensidadesEntrantes.append(salon.actividad.intensidad)
            frecuenciasEntrantes.append(salon.actividad.frecuencia)
        frecuencia = sum(frecuenciasEntrantes) / len(frecuenciasEntrantes)

        if frecuencia in range(100):
            frecuencia = "100"
        elif frecuencia in range(250):
            frecuencia = "250"
        elif frecuencia in range(500):
            frecuencia = "500"
        elif frecuencia in range(1000):
            frecuencia = "1000"
        elif frecuencia in range(2000):
            frecuencia = "2000"
        elif frecuencia in range(4000):
            frecuencia = "4000"
        coeficienteAbsorcion = 0
        for superficie in superficies:
            coeficienteAbsorcion += superficie.material.coeficienteAbsorcion[
                str(aproximar_frecuencia(int(frecuencia)))
            ]
        # Revisar
        coeficienteAbsorcion /= len(superficies)
        # Revisar
        intensidad = sum([10 ** (db / 10) for db in intensidadesEntrantes])
        intensidad = 10 * math.log10(intensidad)
        sonidoEntrante = intensidad * math.log10(1 / coeficienteAbsorcion)
# #        print(
#             f"El ruido en el salon {self.id} es de {sonidoEntrante} con una frecuencia de {frecuencia}"
#         )
        return sonidoEntrante, frecuencia

    def _DeterminarHabitabilidad(self, superficies):
        sonidoEntrante, frecuencia = self.CalcularRuido(superficies)
        if sonidoEntrante <= self.actividad.maximoPermisible - 10:
            self.habitable = "GREEN"
        elif sonidoEntrante <= self.actividad.maximoPermisible + 20:
            self.habitable = "YELLOW"
        else:
            self.habitable = "RED"
        return self.habitable
    
    def DeterminarHabitabilidad(self, superficies):
        color = self._DeterminarHabitabilidad(superficies)
        return (color == "GREEN") or (color == "YELLOW")
