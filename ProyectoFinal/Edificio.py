class Edificio:
    salones = []
    superficies = []
    
    def __init__(self, salones, superficies):
        self.salones = salones
        self.superficies = superficies
        self.matriz_conexiones = [[0 for _ in range(len(salones))] for _ in range(len(salones))]
        # Inicializa la matriz de superficies con ceros o valores predeterminados
        for i in range(len(salones)):
            # print(f"{salones[i].id:5}", end="\n")
            for j in range(len(salones)):
                if salones[j] in salones[i].salonesAdyacentes:
                    for superficie in superficies:
                        if salones[i].id == superficie.salonesSeparados[0].id and salones[j].id == superficie.salonesSeparados[1].id:
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

    def determinar_habitabilidad(self):
        salonesHabitables = [0,0,0]
        for salon in self.salones:
            # print(salon)
            salon.DeterminarHabitabilidad(self.superficies)
            if salon.habitable == "GREEN":
                salonesHabitables[0] += 1
            elif salon.habitable == "YELLOW":
                salonesHabitables[1] += 1
            else:
                salonesHabitables[2] += 1
        if (salonesHabitables[0]+salonesHabitables[1])/len(self.salones) >= 0.7:
            print(f"-------------- \nEl edificio es habitable")
        else:
            print(f"-------------- \nEl edificio no es habitable")

    def calcular_numero_espacios_habitables(self):
        self.determinar_habitabilidad()
        salonesHabitables = [0,0,0]
        for salon in self.salones:
            if salon.habitable == "GREEN":
                salonesHabitables[0] += 1
            elif salon.habitable == "YELLOW":
                salonesHabitables[1] += 1
            else:
                salonesHabitables[2] += 1
        print(f"Salones habitables: {salonesHabitables[0] + salonesHabitables[1]} de {len(self.salones)}")
        pass