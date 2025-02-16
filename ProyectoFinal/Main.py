import random
from Edificio import Edificio
from Actividad import Actividad
from Salon import Salon
from Material import Material
from Superficie import Superficie

class Init:

    def __init__(self, numero_pisos, numero_salones_por_piso):
        self.numero_pisos = numero_pisos
        self.numero_salones_por_piso = numero_salones_por_piso

        # Crear el edificio al inicializar la clase
        self.salones, self.superficies = self.crear_edificio(self.numero_salones_por_piso, self.numero_pisos)
        self.edificio = Edificio(self.salones, self.superficies)

        # Realizar operaciones sobre el edificio
        self.edificio.determinar_habitabilidad()
        self.edificio.calcular_numero_espacios_habitables()

    actividades = [
        Actividad(40, 100, "Lectura(Biblioteca)", 50),
        Actividad(50, 100, "Seminario", 55),
        Actividad(55, 250, "Clases Magistrales", 60),
        Actividad(70, 100, "Exámenes", 65),
        Actividad(60, 400, "Salones de esparcimiento", 100),
    ]

    hormigon = Material(
        {"100": 0.30, "250": 0.45, "500": 0.30,
            "1000": 0.25, "2000": 0.40, "4000": 0.25},
        "Hormigon", "ORANGE"
    )
    ladrillo = Material(
        {
            "100": 0.013,
            "250": 0.015,
            "500": 0.020,
            "1000": 0.028,
            "2000": 0.04,
            "4000": 0.05,
        },
        "Ladrillo", "RED"
    )
    vidrio = Material(
        {"100": 0.035, "250": 0.04, "500": 0.027,
            "1000": 0.03, "2000": 0.02, "4000": 0.02},
        "Vidrio", "BLUE"
    )
    escayola = Material(
        {"100": 0.02, "250": 0.03, "500": 0.04,
            "1000": 0.05, "2000": 0.05, "4000": 0.06},
        "Escayola", "GREY"
    )

    def crear_edificio(self, numero_salones_por_piso, numero_pisos):
        # Generar salones y asignar actividades aleatorias
        salones = []
        materiales = [self.hormigon, self.vidrio, self.ladrillo]
        for piso in range(1, numero_pisos + 1):
            for id in range(1, numero_salones_por_piso + 1):
                actividad = random.choice(self.actividades)
                salon = Salon(actividad, [], piso, piso * 100 + id)
                salones.append(salon)

        # Crear diccionario para acceso rápido por número de salón
        salon_dict = {salon.id: salon for salon in salones}

        # Asignar salones adyacentes
        for salon in salones:
            piso = salon.piso
            numero = salon.id % 100
            adyacentes = []

            # Salón a la izquierda
            if numero > 1 and numero % 2 == 0:
                adyacentes.append(salon_dict[piso * 100 + (numero - 1)])

            if (piso * 100 + (numero - 2)) in salon_dict:
                adyacentes.append(salon_dict[piso * 100 + (numero - 2)])
            # Salón a la derecha
            if numero < numero_salones_por_piso and numero % 2 == 1:
                adyacentes.append(salon_dict[piso * 100 + (numero + 1)])

            if (piso * 100 + (numero + 2)) in salon_dict:
                adyacentes.append(salon_dict[piso * 100 + (numero + 2)])
                
            # Salón arriba
            if piso < numero_pisos:
                adyacentes.append(salon_dict[(piso + 1) * 100 + numero])
            # Salón abajo
            if piso > 1:
                adyacentes.append(salon_dict[(piso - 1) * 100 + numero])

            salon.salonesAdyacentes = adyacentes

        # Crear superficies
        superficies = []

        for salon in salones:
            for adyacente in salon.salonesAdyacentes:
                if salon.id < adyacente.id:  # Evitar duplicados
                    tipo = "Pared" if salon.piso == adyacente.piso else "Techo"
                    material = self.escayola if tipo == "Techo" else random.choice(materiales)
                    superficies.append(Superficie(material, [salon, adyacente], tipo))

        return salones,superficies
