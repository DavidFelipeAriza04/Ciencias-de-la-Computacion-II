from rest_framework import viewsets
from .models import Municipio
from .serializers import MunicipioSerializer
from rest_framework.response import Response
from django.db.models import Q
from Algoritmos.Algoritmos import busqueda, Dijkstra , Bellman_Ford, algoritmo_Kruskal, algoritmo_Prim

diccionarioPosiciones = {
    0: "Leticia",
    1: "Medellin",
    2: "Arauca",
    3: "Barranquilla",
    4: "Bogota",
    5: "Cartagena",
    6: "Tunja",
    7: "Manizales",
    8: "Mitu",
    9: "Yopal",
    10: "Popayan",
    11: "Valledupar",
    12: "Quibdo",
    13: "Monteria",
    14: "Inirida",
    15: "Riohacha",
    16: "San Jose del Guaviare",
    17: "Neiva",
    18: "Santa Marta",
    19: "Villavicencio",
    20: "Pasto",
    21: "Cucuta",
    22: "Santa Rita",
    23: "Armenia",
    24: "Union",
    25: "Bucaramanga",
    26: "Sincelejo",
    27: "Puerto Trujillo",
    28: "Cali",
    29: "Puerto Carreno",
}


# Create your views here.
class MunicipiosViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    matriz = [[100 for x in range(30)] for y in range(30)]

    def list(self, request, *args, **kwargs):
        # Lee el archivo y crea municipios
        with open("Municipios.txt", "r") as archivo:
            lineas = archivo.readlines()
            contador = 0
            for linea in lineas:
                municipio = linea.split(", ")
                if not self.queryset.count() == 30:
                    Municipio.objects.create(
                        nombre=municipio[0].replace("_", " "),
                        latitud=municipio[1],
                        longitud=municipio[2],
                        LeticiaConexion=municipio[3],
                        MedellinConexion=municipio[4],
                        AraucaConexion=municipio[5],
                        BarranquillaConexion=municipio[6],
                        BogotaConexion=municipio[7],
                        CartagenaConexion=municipio[8],
                        TunjaConexion=municipio[9],
                        ManizalesConexion=municipio[10],
                        MituConexion=municipio[11],
                        YopalConexion=municipio[12],
                        PopayanConexion=municipio[13],
                        ValleduparConexion=municipio[14],
                        QuibdoConexion=municipio[15],
                        MonteriaConexion=municipio[16],
                        IniridaConexion=municipio[17],
                        RiohachaConexion=municipio[18],
                        SanJosedelGuaviareConexion=municipio[19],
                        NeivaConexion=municipio[20],
                        SantaMartaConexion=municipio[21],
                        VillavicencioConexion=municipio[22],
                        PastoConexion=municipio[23],
                        CucutaConexion=municipio[24],
                        SantaRitaConexion=municipio[25],
                        ArmeniaConexion=municipio[26],
                        UnionConexion=municipio[27],
                        BucaramangaConexion=municipio[28],
                        SincelejoConexion=municipio[29],
                        PuertoTrujilloConexion=municipio[30],
                        CaliConexion=municipio[31],
                        PuertoCarrenoConexion=municipio[32].replace("\n", ""),
                    )
                for i in range(contador, 30):
                    self.matriz[contador][i] = municipio[i + 3]
                    self.matriz[i][contador] = self.matriz[contador][i]
                contador += 1
        archivo.close()

        max_ancho = max(
            len("San Jose Del Guaviare") for fila in self.matriz for valor in fila
        )

        with open("Matriz.txt", "w") as archivo:
            # Escribe la fila de encabezados
            archivo.write("x")
            archivo.write(
                " " * (max_ancho + 1)
            )  # Espacios en blanco para la columna de nombres
            for i in range(30):
                archivo.write(
                    f"{diccionarioPosiciones[i].replace(' ', '_').ljust(max_ancho + 2)}"
                )  # Encabezados de columna alineados
            archivo.write("\n")

            # Escribe las filas de la matriz
            for i in range(30):
                archivo.write(
                    f"{diccionarioPosiciones[i].replace(' ', '_').ljust(max_ancho + 2)}"
                )  # Nombre de la fila alineado
                for j in range(30):
                    # print(f"{str(self.matriz[i][j]).ljust(max_ancho + 2)}")
                    if i == 29:
                        archivo.write(
                            f"{str(self.matriz[i][j]).ljust(max_ancho + 3).replace('\n', '')}"
                        )
                    else:
                        archivo.write(
                            f"{str(self.matriz[i][j]).ljust(max_ancho + 2)}"
                        )  # Valores de la matriz alineados
                archivo.write("\n")
        archivo.close()
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        match request.data.get("algoritmo"):
            case "GBFS" | "A*":
                origen = Municipio.objects.filter(
                    Q(nombre=request.data.get("origen")["nombre"])
                )
                destino = Municipio.objects.filter(
                    Q(nombre=request.data.get("destino")["nombre"])
                )
                municipios, distancia = busqueda(
                    origen.values().first()["nombre"].replace(" ", "_"),
                    destino.values().first()["nombre"].replace(" ", "_"),
                    request.data.get("algoritmo")
                )
                print(municipios, end="\n")
                print(distancia)
                print(request.data.get("algoritmo"))
            case "Dijkstra":
                origen = Municipio.objects.filter(
                    Q(nombre=request.data.get("origen")["nombre"])
                )
                destino = Municipio.objects.filter(
                    Q(nombre=request.data.get("destino")["nombre"])
                )
                municipios, distancia = Dijkstra(
                    origen.values().first()["nombre"].replace(" ", "_"),
                    destino.values().first()["nombre"].replace(" ", "_"),
                    diccionarioPosiciones
                )
                print(municipios, end="\n")
                print(distancia)
                print(request.data.get("algoritmo"))
            case "Bellman-Ford":
                origen = Municipio.objects.filter(
                    Q(nombre=request.data.get("origen")["nombre"])
                )
                destino = Municipio.objects.filter(
                    Q(nombre=request.data.get("destino")["nombre"])
                )
                municipios, distancia = Bellman_Ford(
                    origen.values().first()["nombre"].replace(" ", "_"),
                    destino.values().first()["nombre"].replace(" ", "_"),
                    diccionarioPosiciones
                )
                print(municipios, end="\n")
                print(distancia)
                print(request.data.get("algoritmo"))
            case "Kruskal":
                recorrido = algoritmo_Kruskal()
                for municipio in recorrido:
                    print(municipio)
                return Response({"recorrido": recorrido})
            case "Prim":
                recorrido = algoritmo_Prim()
                for municipio in recorrido:
                    print(municipio)
                return Response({"recorrido": recorrido})
        return Response({"recorrido": municipios, "distancia": distancia})
