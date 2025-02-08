import random as rnd
from Superficie import Superficie
from Salon import Salon
import copy
from collections import deque

PORCENTAJE_HABITABILIDAD = 0.7

def determinar_superficies_adyacentes(salones: list[Salon], superficies: list[Superficie]) \
    -> dict[Salon, list[Superficie]]:

    out: dict[Salon, list[Superficie]] = {}
    for salon in salones:
        for superficie in superficies:
            ss = superficie.salonesSeparados
            if ss[0] == salon or ss[1] == salon:
                if salon not in out:
                    out[salon] = [superficie]
                out[salon].append(superficie)

    return out

class Edificio:
    salones = []
    superficies = []
    superficies_adyacentes = {}
    recomendaciones = {
        "YELLOW" : ["Es recomendable instalar una capa de páneles de espuma acústica para disminuir el ruido", "Se sugiere usar páneles de yeso acústico"],
        "RED" : "La estructura no es adecuada para habitabilidad, se recomienda realizar una reestructuración."
    }

    def __init__(self, salones, superficies):
        self.salones = salones
        self.superficies = superficies
        self.superficies_adyacentes = determinar_superficies_adyacentes(salones, superficies)
        
        self.matriz_conexiones = [
            [0 for _ in range(len(salones))] for _ in range(len(salones))
        ]
        # Inicializa la matriz de superficies con ceros o valores predeterminados
        for i in range(len(salones)):
            # print(f"{salones[i].id:5}", end="\n")
            for j in range(len(salones)):
                if salones[j] in salones[i].salonesAdyacentes:
                    for superficie in superficies:
                        if (
                            salones[i].id == superficie.salonesSeparados[0].id
                            and salones[j].id == superficie.salonesSeparados[1].id
                        ):
                            print(f"Salon {salones[i].id} adyacente a {salones[j].id}")
                            self.matriz_conexiones[i][j] = superficie.material.nombre
                            self.matriz_conexiones[j][i] = superficie.material.nombre
                            break
        print("     ", " ".join(f"{col.id:5}" for col in salones))
        print("     ", "-" * (len(salones) * 6))  # Línea separadora
        print("\n")
        for i in range(len(salones)):
            print(f"{salones[i].id:5}", end=" ")
            for j in range(len(salones)):
                print(f"{self.matriz_conexiones[i][j]:5}", end=" ")
            print("\n")
    
    def calcular_habitabilidad(self):
        noHabitables = 0
        for salon in self.salones:
            color = salon._DeterminarHabitabilidad(self.superficies_adyacentes[salon])
            if color == "RED": noHabitables += 1
        
        return 1 - (noHabitables / len(self.salones))

    def determinar_habitabilidad(self):
        return self.calcular_habitabilidad() >= PORCENTAJE_HABITABILIDAD

    def __reorder(self, idxs: list[int]):
        best_percentage = self.calcular_habitabilidad()
        for i in idxs:
            x = self.salones[i]
            for j in range(i, len(idxs)):
                y = self.salones[idxs[j]]
                x.actividad, y.actividad = y.actividad, x.actividad
                percentage = self.calcular_habitabilidad()
                if percentage > best_percentage:
                    best_percentage = percentage
                else:
                    x.actividad, y.actividad = y.actividad, x.actividad

    def _reorganizar_actividades(self):
        idxs = {"RED":[], "YELLOW":[], "GREEN":[]}
        for i,salon in enumerate(self.salones):
            color = salon._DeterminarHabitabilidad(self.superficies_adyacentes[salon])
            idxs[color].append(i)

# metodo 1: reorganizar listas separadas (eficiente, no mejora tanto la habitabilidad)
#       self.__reorder(idxs["RED"])
#     self.__reorder(idxs["YELLOW"])        
#      self.__reorder(idxs["GREEN"])

# metodo 2: reorganizar toda la lista (bastante mas complejo, mejora 
        self.__reorder([i for i in range(len(self.salones))])

    
    def imprimir_recomendaciones(self):
        salonesHabitables = [0, 0, 0]
        for salon in self.salones:
            salon.DeterminarHabitabilidad(self.superficies_adyacentes[salon])
            if salon.habitable == "GREEN":
                salonesHabitables[0] += 1
            elif salon.habitable == "YELLOW":
                print(f"Para el salon {salon.id} {self.recomendaciones["YELLOW"][rnd.randint(0,1)]}")
                salonesHabitables[1] += 1
            else:
                print(f"Para el salon {salon.id} {self.recomendaciones["RED"]}")
                salonesHabitables[2] += 1

        if (salonesHabitables[0] + salonesHabitables[1]) / len(self.salones) >= PORCENTAJE_HABITABILIDAD:
            print("El edificio es habitable")
        else:
            print("El edificio no habitable")

    def obtener_grafo_reducido(self, salones):
        visitados = set()
        num_salones = len(salones)

        def reducir_grafo(salon):
            nonlocal visitados, num_salones

            if len(visitados) == num_salones:
                return 

            visitados.add(salon)
            adyacentes_a_remover = []

            # Explora todos los adyacentes primero
            for a in salon.salonesAdyacentes: 
                if salon.habitable == "GREEN":
                    adyacentes_a_remover.append(a)
            
                if a.habitable == "GREEN" and salon.habitable != "GREEN":
                    adyacentes_a_remover.append(a)

                if a not in visitados:
                    reducir_grafo(a)

            # Remueve los adyacentes verdes después del recorrido
            for a in adyacentes_a_remover:
                salon.salonesAdyacentes.remove(a)

        salones_copia = copy.deepcopy(salones)   
        print(len(salones_copia))

        reducir_grafo(salones_copia[0])
        reducir_grafo(salones_copia[1]) 
        salones_copia = [s for s in salones_copia if s.habitable != "GREEN"]  

        print(len(salones_copia))
        x = self.encontrar_subgrafos(salones_copia)

        print(len(x))
        for i in x:
            print(f"Tamaño subgrafos {len(i)}")
        return salones_copia
    
    def encontrar_subgrafos(self,salones):
        salones_recorridos = set()
        subgrafos = []

        def BFS(nodo):
            nonlocal salones_recorridos
            cola = deque()
            subgrafo = set()

            cola.append(nodo)
            subgrafo.add(nodo)

            while cola:
                s = cola.pop()

                for adj in s.salonesAdyacentes:
                    if adj not in subgrafo:
                        subgrafo.add(adj)
                        salones_recorridos.add(adj)
                        cola.append(adj)
            
            return subgrafo
        
        for salon in salones:
            if salon not in salones_recorridos:
                subgrafos.append(BFS(salon))
        
        return subgrafos

        
    def reorganizar_actividades(self):
        actividades = [salon.actividad for salon in self.salones]
        n = len(actividades)  # Número total de actividades
        best_permutation = []
        contador = [0]  # Usamos una lista para modificar el valor dentro de la función

        def bactracking(start):
            nonlocal best_permutation
            contador[0] += 1  # Incrementar el contador en cada llamada
            print(f"Número total de llamadas a bactracking: {contador[0]}")
            for i, salon in enumerate(self.salones):
                salon.actividad = actividades[i]

            if self.determinar_habitabilidad():
                best_permutation = actividades[:]
                return

            for i in range(start, n):
                actividades[start], actividades[i] = actividades[i], actividades[start]
                bactracking(start + 1)
                actividades[start], actividades[i] = actividades[i], actividades[start]


        bactracking(0)

        self.imprimir_recomendaciones()

    def calcular_numero_espacios_habitables(self):
        sz = len(self.salones)
        x = self.calcular_habitabilidad() * sz
        print(
            f"Salones habitables: {x} de {sz}"
        )
        return x
