class Edificio:
    
    def __init__(self, salones, superficies):
        self.salones = [[0 for _ in range(len(salones))] for _ in range(len(salones))]
        # Inicializa la matriz de superficies con ceros o valores predeterminados
        for i in range(len(salones)):
            # print(f"{salones[i].id:5}", end="\n")
            for j in range(len(salones)):
                if salones[j] in salones[i].salonesAdyacentes:
                    for superficie in superficies:
                        if [salones[i],salones[j]] in superficie.salonesSeparados:
                            print(f"Salon {salones[i].id} adyacente a {salones[j].id}")
                            self.salones[i][j] = superficie.material.nombre
                            self.salones[j][i] = superficie.material.nombre
                            
                            break
        print("     ", " ".join(f"{col.id:5}" for col in salones))
        print("     ", "-" * (len(salones) * 6))  # Línea separadora 
        print("\n")
        for i in range(len(salones)):
            print(f"{salones[i].id:5}", end=" ")
            for j in range(len(salones)):
                print(f"{self.salones[i][j]:5}", end=" ")
            print("\n")

    def determinar_habilidad(self):
        pass

    def calcular_numero_espacios_habitables(self):
        pass