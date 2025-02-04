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

    salon101 = Salon(actividades[0], [],1, 101)
    salon102 = Salon(actividades[2], [], 1, 102)
    salon103 = Salon(actividades[3], [], 1, 103)
    salon104 = Salon(actividades[1], [], 1, 104)
    salon201 = Salon(actividades[4], [], 2, 201)
    salon202 = Salon(actividades[1], [], 2, 202)

    salones = [salon101, salon102, salon103, salon104, salon201, salon202]

    salon101.salonesAdyacentes = [salon102, salon201]
    salon102.salonesAdyacentes = [salon101, salon202]
    salon103.salonesAdyacentes = [salon104]
    salon104.salonesAdyacentes = [salon103]
    salon201.salonesAdyacentes = [salon202, salon101]
    salon202.salonesAdyacentes = [salon201, salon102]

    superficies = [
        Superficie(hormigon, [salon101, salon102], "Pared"),
        Superficie(ladrillo, [salon103, salon104], "Pared"),
        Superficie(escayola, [salon101, salon201], "Techo"),
        Superficie(escayola, [salon102, salon202], "Techo"),
    ]

    edificio = Edificio(salones, superficies)
    # salon103.CalcularRuido(superficies)
    edificio.determinar_habitabilidad()
    edificio.calcular_numero_espacios_habitables()