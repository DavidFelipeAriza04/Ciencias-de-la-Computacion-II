from Edificio import Edificio
from Actividad import Actividad
from Salon import Salon
from Material import Material
from Superficie import Superficie


actividades = [
    Actividad(45, 55, "Lectura(Biblioteca)"),
    Actividad(50, 0.0, "Seminario"),
    Actividad(55, 0.0, "Clases Magistrales"),
    Actividad(50, 0.0, "Exámenes"),
    Actividad(60, 0.0, "Salones de esparcimiento"),
    Actividad(80, 0.0, "Construcción"),
]

hormigon = Material(
    {"100": 0.30, "250": 0.45, "500": 0.30,
        "1000": 0.25, "2000": 0.40, "4000": 0.25},
    "Hormigon",
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
    "Ladrillo",
)
vidrio = Material(
    {"100": 0.035, "250": 0.04, "500": 0.027,
        "1000": 0.03, "2000": 0.02, "4000": 0.02},
    "Vidrio",
)
escayola = Material(
    {"100": 0.02, "250": 0.03, "500": 0.04,
        "1000": 0.05, "2000": 0.05, "4000": 0.06},
    "Escayola",
)

salon101 = Salon(actividades[0], [], 50, 1, 101)
salon102 = Salon(actividades[2], [], 60, 1, 102)
salon103 = Salon(actividades[3], [], 65, 1, 103)
salon104 = Salon(actividades[1], [], 55, 1, 104)
salon201 = Salon(actividades[4], [], 80, 2, 201)
salon202 = Salon(actividades[1], [], 55, 2, 202)

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
salon103.CalcularRuido(superficies)
edificio.determinar_habilidad()
