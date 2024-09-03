import heapq
from Algoritmos.Nodo import Pueblo, Nodo
from math import radians, cos, sin, asin, sqrt

def busqueda(origen, destino, metodo='GBFS'):
    # Leer y procesar la matriz y los pueblos
    with open("Matriz.txt", "r") as f:
        matriz = crearMatriz(f)
    arreglo_pueblos = crearArregloPueblos(matriz)

    # Obtener coordenadas del destino y del pueblo inicial
    cordDestino = buscarCoordMunicipio(destino, matriz)
    puebloInicial = buscarMunicipio(origen, arreglo_pueblos)

    # Calcular heurística inicial
    heuristica_inicial = calculaHeristica(puebloInicial, arreglo_pueblos, destino, 0)

    # Crear nodo inicial
    start = Nodo(
        puebloInicial,
        None,
        buscarCoordMunicipio(origen, matriz),
        heuristica_inicial,
    )

    # Inicializar la frontera (cola de prioridad) y el conjunto explorado
    frontera = []
    heapq.heapify(frontera)
    heapq.heappush(frontera, start)
    conjuntoExplorado = set()

    while True:
        if not frontera:
            raise Exception("No solution")

        nodo = heapq.heappop(frontera)

        if comprobarDestino((nodo.estado.x, nodo.estado.y), cordDestino):
            return construir_ruta(nodo, start)

        conjuntoExplorado.add(nodo.estado)

        cordsPueblosAdy = buscarPueblosPosibles(matriz, nodo.estado.x)
        pueblosAdyacentes = []

        for cordPueblo in cordsPueblosAdy:
            pueblo = buscarMunicipio(matriz[0][cordPueblo], arreglo_pueblos)

            # Calcular heurística y costo según el método
            if metodo == 'A*':
                gn = nodo.estado.g + float(matriz[nodo.estado.x][pueblo.y])
                heuristica = calculaHeristica(pueblo, arreglo_pueblos, destino, gn)
            else:  # GBFS
                gn = 0
                heuristica = calculaHeristica(pueblo, arreglo_pueblos, destino, 0)

            pueblo.heuristica = heuristica
            pueblo.h = calculaHeristica(pueblo, arreglo_pueblos, destino, 0)
            pueblo.g = gn
            pueblosAdyacentes.append(pueblo)

        for pueblo in pueblosAdyacentes:
            if pueblo not in conjuntoExplorado and not estado_en_frontera(frontera, pueblo):
                nodo_hijo = Nodo(
                    pueblo,
                    nodo,
                    (pueblo.x, pueblo.y),
                    pueblo.heuristica,
                )
                heapq.heappush(frontera, nodo_hijo)

def crearMatriz(f):
    matriz_adyacencia = [linea.split() for linea in f if linea.strip()]
    return matriz_adyacencia


def buscarCoordMunicipio(nombre, matriz_adyacencia):
    try:
        i = matriz_adyacencia[0].index(nombre)
    except ValueError:
        raise ValueError(
            f"Municipio '{nombre}' no encontrado en la cabecera de columnas."
        )

    for index, fila in enumerate(matriz_adyacencia[1:], start=1):
        if fila[0] == nombre:
            return (index, i)


def comprobarDestino(cordOrigen, cordsDestino):
    return cordOrigen == cordsDestino


def crearArregloPueblos(matrizAdyacencia):
    archivo_municipios = open("Municipios.txt", "r")
    arreglo_pueblos = []
    for linea in archivo_municipios:
        atributos_pueblo = linea.split(", ")
        pueblo = Pueblo(
            atributos_pueblo[0].strip(),
            float(atributos_pueblo[1]),
            float(atributos_pueblo[2]),
            0,0,
            buscarCoordMunicipio(atributos_pueblo[0].strip(), matrizAdyacencia),
        )

        arreglo_pueblos.append(pueblo)
    return arreglo_pueblos

def calculaHeristica(
    pueblo,
    arregloPueblos,
    destino,
    gn
):
    puebloDestino = buscarMunicipio(destino, arregloPueblos)
    latD = puebloDestino.latitud
    longD = puebloDestino.longitud

    return distance(pueblo.latitud, latD, pueblo.longitud, longD)+gn

def distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


def buscarMunicipio(nombre, arregloPueblos):
    return next((pueblo for pueblo in arregloPueblos if pueblo.nombre == nombre), None)


def buscarPueblosPosibles(matrizAdyacencia, fila):
    linea = matrizAdyacencia[fila]
    pueblosAdyacentes = [i for i,elemento in enumerate(linea[1:],1) if elemento != '0']
    return pueblosAdyacentes


def estado_en_frontera(frontera, estado):
    return any(nodo.estado == estado for nodo in frontera)

def construir_ruta(nodo,start):
    nodos = []
    while nodo.padre is not None:
        nodos.append(nodo.estado)
        nodo = nodo.padre
    nodos.append(start.estado)
    nodos.reverse()

    distancia_total = 0
    for i in range(0, len(nodos) - 1):
        distancia_total += distance(nodos[i].latitud, nodos[i + 1].latitud, nodos[i].longitud, nodos[i + 1].longitud)

    nombres_municipios = [municipio.nombre for municipio in nodos]

    return nombres_municipios, distancia_total



# Municipios, Distancia = busqueda("Cucuta", "Puerto_Trujillo","GBFS")
# for x in Municipios:
#     print(x)
# print(Distancia)
