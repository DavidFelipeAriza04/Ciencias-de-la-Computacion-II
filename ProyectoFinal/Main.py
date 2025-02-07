import random
from Edificio import Edificio
from Actividad import Actividad
from Salon import Salon
from Material import Material
from Superficie import Superficie

class Init():
    actividades = [
        Actividad(40, 100, "Lectura(Biblioteca)", 50),
        Actividad(50, 100, "Seminario", 55),
        Actividad(55, 250, "Clases Magistrales", 60),
        Actividad(70, 100, "Exámenes", 65),
        Actividad(60, 400, "Salones de esparcimiento", 100),
        Actividad(80, 500, "Construcción", 1000),
    ]

    hormigon = Material(
        {"100": 0.30, "250": 0.45, "500": 0.30,
            "1000": 0.25, "2000": 0.40, "4000": 0.25},
        "Hormigon","ORANGE"
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
        "Ladrillo","RED"
    )
    vidrio = Material(
        {"100": 0.035, "250": 0.04, "500": 0.027,
            "1000": 0.03, "2000": 0.02, "4000": 0.02},
        "Vidrio","BLUE"
    )
    escayola = Material(
        {"100": 0.02, "250": 0.03, "500": 0.04,
            "1000": 0.05, "2000": 0.05, "4000": 0.06},
        "Escayola", "GREY"
    )

    # Generar salones y asignar actividades aleatorias
    salones = []
    materiales = [hormigon, vidrio, ladrillo]
    for piso in range(1, 3):  # Cambiado a solo 2 pisos: 1 y 2
        for id in range(1, 17):  # Salones del 101 al 108, 201 al 208
            actividad = random.choice(actividades)
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
        if numero > 1 and (piso * 100 + (numero - 2)) in salon_dict:
            adyacentes.append(salon_dict[piso * 100 + (numero - 2)])
        # Salón a la derecha
        if numero < 16 and (piso * 100 + (numero + 2)) in salon_dict:
            adyacentes.append(salon_dict[piso * 100 + (numero + 2)])
        '''
        # Salón a la izquierda
        if numero > 1 and numero % 2 == 0:
            adyacentes.append(salon_dict[piso * 100 + (numero - 1)])
        # Salón a la derecha
        if numero < 12 and numero % 2 == 1:
            adyacentes.append(salon_dict[piso * 100 + (numero + 1)])
        if (piso * 100 + (numero + 2)) in salon_dict and numero %2 == 0:
            pass
            #adyacentes.append(salon_dict[piso * 100 + (numero + 2)])
        '''
        # Salón arriba
        if piso < 2:
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
                material = escayola if tipo == "Techo" else random.choice(materiales)
                superficies.append(Superficie(material, [salon, adyacente], tipo))

    edificio = Edificio(salones, superficies)
    # salon103.CalcularRuido(superficies)
    edificio.determinar_habitabilidad()
    edificio.calcular_numero_espacios_habitables()
    edificio.obtener_grafo_reducido(salones)
    #edificio.reorganizar_actividades()