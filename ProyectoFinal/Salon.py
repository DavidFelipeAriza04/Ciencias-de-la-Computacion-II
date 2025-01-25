import math
from Actividad import Actividad


class Salon():
    actividad = None
    salonesAdyacentes = []
    maximoPermisible = 0.0
    piso = 0
    id = 0
    
    def __init__(self, actividad, salonesAdyacentes, maximoPermisible, piso, id):
        self.actividad = actividad
        self.salonesAdyacentes = salonesAdyacentes
        self.maximoPermisible = maximoPermisible
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
            frecuencia = '1000'
        elif frecuencia in range(2000):
            frecuencia = "2000"
        elif frecuencia in range(4000):
            frecuencia = "4000"
        coeficienteAbsorcion = 0
        for superficie in superficies:
            if superficie.salonesSeparados[0] == self or superficie.salonesSeparados[1] == self:
                print(f"Salon {self.id} adyacente a {superficie.salonesSeparados[0].id}"if superficie.salonesSeparados[1] == self else f"Salon {self.id} adyacente a {superficie.salonesSeparados[1].id}")
                coeficienteAbsorcion += superficie.material.coeficienteAbsorcion[frecuencia]
        intensidad = sum([10 ** (db / 10) for db in intensidadesEntrantes])
        intensidad = 10 * math.log10(intensidad)
        sonidoEntrante = intensidad * math.log10(1/coeficienteAbsorcion)
        print (f"El ruido en el salon {self.id} es de {sonidoEntrante} con una frecuencia de {frecuencia}")
    
    def DeterminarHabitabilidad(self):
        if self.actividad.CalcularRuido() > self.maximoPermisible:
            return False
        else:
            return True