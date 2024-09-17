import heapq
import sys
from Algoritmos.Nodo import Pueblo, Nodo
from math import radians, cos, sin, asin, sqrt


#  * Implementación de los algoritmos de búsqueda A* y GBFS
def busqueda(origen, destino, metodo="GBFS"):
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
            if metodo == "A*":
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
            if pueblo not in conjuntoExplorado and not estado_en_frontera(
                frontera, pueblo
            ):
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
            0,
            0,
            buscarCoordMunicipio(atributos_pueblo[0].strip(), matrizAdyacencia),
        )

        arreglo_pueblos.append(pueblo)
    return arreglo_pueblos


def calculaHeristica(pueblo, arregloPueblos, destino, gn):
    puebloDestino = buscarMunicipio(destino, arregloPueblos)
    latD = puebloDestino.latitud
    longD = puebloDestino.longitud

    return distance(pueblo.latitud, latD, pueblo.longitud, longD) + gn


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
    pueblosAdyacentes = [
        i for i, elemento in enumerate(linea[1:], 1) if elemento != "0"
    ]
    return pueblosAdyacentes


def estado_en_frontera(frontera, estado):
    return any(nodo.estado == estado for nodo in frontera)


def construir_ruta(nodo, start):
    nodos = []
    while nodo.padre is not None:
        nodos.append(nodo.estado)
        nodo = nodo.padre
    nodos.append(start.estado)
    nodos.reverse()

    distancia_total = 0
    for i in range(0, len(nodos) - 1):
        distancia_total += distance(
            nodos[i].latitud,
            nodos[i + 1].latitud,
            nodos[i].longitud,
            nodos[i + 1].longitud,
        )

    nombres_municipios = [municipio.nombre for municipio in nodos]

    return nombres_municipios, round(distancia_total, 2)


# * Implementacion del algoritmo de Kruskal
def algoritmo_Kruskal():
    grafo = crear_grafo()
    grafo = sorted(grafo, key=lambda t: t[2])
    municipios = set()

    i = 0

    for u in grafo:
        municipios.add(u[0])
        municipios.add(u[1])

    padres = {}
    rangos = {}

    for municipio in municipios:
        padres[municipio] = municipio
        rangos[municipio] = 0

    aristas, vertices = 0, len(municipios)

    resultado = []
    while aristas < vertices - 1:
        u, v, peso = grafo[i]
        i += 1

        padre_u = encontrar_padre(padres, u)
        padre_v = encontrar_padre(padres, v)

        if padre_u != padre_v:
            aristas += 1
            resultado.append([u, v, peso])
            union(padres, rangos, padre_u, padre_v)

    return resultado


# Se encarga de crear el grafo
def crear_grafo():
    with open("Matriz.txt", "r") as f:
        matriz = crearMatriz(f)

    grafo = []
    elementos_grafo = set()
    for i, fila in enumerate(matriz[1:], 1):
        for j, elemento in enumerate(fila[1:], 1):
            if elemento != "0":
                nodos = tuple(sorted((matriz[i][0], matriz[0][j])))
                elementos_grafo.add((nodos, float(elemento)))

    for elemento in elementos_grafo:
        lista = list(elemento[0])
        lista.append(elemento[1])
        grafo.append(lista)

    return grafo


# Busca al padre del conjunto disjunto
def encontrar_padre(padre, nombre):
    if padre[nombre] != nombre:
        padre[nombre] = encontrar_padre(padre, padre[nombre])
    return padre[nombre]


# La función se encarga de unir conjuntos disjuntos
# "padre" aquí se refiere al representante del conjunto, no necesariamente al nodo anterior.
def union(padres, rangos, u, v):
    if rangos[u] < rangos[v]:
        padres[u] = v
    elif rangos[u] > rangos[v]:
        padres[v] = u
    else:
        padres[v] = u
        rangos[u] = +1


#  * Implementacion del algoritmo de Prim
def algoritmo_Prim():
    grafo = crear_grafo_prim()
    municipios = list(grafo.keys())


    # Nodo inicial: seleccionamos el primero de la lista
    nodo_inicial = municipios[0]
    # Inicializamos los conjuntos de nodos incluidos y no incluidos en el MST
    nodos_MST = set([nodo_inicial])
    nodos_no_incluidos = set(municipios[0:])

    # Lista para almacenar las aristas que forman el MST
    mst = []

    # Diccionario para guardar las distancias mínimas de cada nodo
    distancias = {nodo: sys.maxsize for nodo in municipios}
    distancias[nodo_inicial] = 0

    # Diccionario para rastrear el predecesor de cada nodo
    predecesores = {nodo: None for nodo in municipios}

    while nodos_no_incluidos:
        # Buscar el nodo con la distancia mínima al MST actual
        u = min(nodos_no_incluidos, key=lambda nodo: distancias[nodo])

        # Añadir el nodo al MST
        nodos_MST.add(u)
        nodos_no_incluidos.remove(u)

        # Si el nodo tiene predecesor, añadimos la arista correspondiente al MST
        if predecesores[u] is not None:
            mst.append((predecesores[u], u, distancias[u]))

        # Actualizamos las distancias de los vecinos de u
        for v, peso in grafo[u]:
            if v in nodos_no_incluidos and peso < distancias[v]:
                distancias[v] = peso
                predecesores[v] = u

    return mst


def crear_grafo_prim():
    with open("Matriz.txt", "r") as f:
        matriz = crearMatriz(f)

    grafo = {}

    for i, fila in enumerate(matriz[1:], 1):
        nodo_origen = matriz[i][0]
        grafo[nodo_origen] = []
        for j, peso in enumerate(fila[1:], 1):
            if peso != "0":
                nodo_destino = matriz[0][j]
                grafo[nodo_origen].append((nodo_destino, float(peso)))

    return grafo


#  * Implementacion del algoritmo de Dijkstra
def Dijkstra(origen, destino, diccionarioPosiciones):
    with open("Matriz.txt", "r") as f:
        matriz = crearMatriz(f)
        matriz_adyacencia = [fila[1:] for fila in matriz[1:]]
        matriz_adyacencia = [
            [float(peso) for peso in fila] for fila in matriz_adyacencia
        ]
    # Número de nodos
    n = len(matriz_adyacencia)
    for clave, valor in diccionarioPosiciones.items():
        if valor == origen.replace("_", " "):
            origen = clave
            break
    for clave, valor in diccionarioPosiciones.items():
        if valor == destino.replace("_", " "):
            destino = clave
            break
    # Inicialización
    distancia = [sys.maxsize] * n  # Inicializa las distancias a infinito
    predecesor = [-1] * n  # Inicializa los predecesores
    distancia[origen] = 0  # La distancia al nodo origen es 0
    visitado = [False] * n  # Inicializa todos los nodos como no visitados

    for _ in range(n):
        # Encuentra el nodo con la distancia mínima entre los no visitados
        min_distancia = sys.maxsize
        nodo_actual = -1

        for i in range(n):
            if not visitado[i] and distancia[i] < min_distancia:
                min_distancia = distancia[i]
                nodo_actual = i

        # Si el nodo actual es el destino, terminamos
        if nodo_actual == destino:
            break

        # Marca el nodo seleccionado como visitado
        visitado[nodo_actual] = True

        # Actualiza las distancias a los vecinos del nodo actual
        for vecino in range(n):
            if (
                matriz_adyacencia[nodo_actual][vecino] > 0 and not visitado[vecino]
            ):  # Solo consideramos aristas con peso mayor a 0
                nueva_distancia = (
                    distancia[nodo_actual] + matriz_adyacencia[nodo_actual][vecino]
                )
                if nueva_distancia < distancia[vecino]:
                    distancia[vecino] = nueva_distancia
                    predecesor[vecino] = nodo_actual  # Guardamos el predecesor

    # Reconstruir el camino más corto
    camino = []
    nodo = destino
    while nodo != -1:
        camino.insert(
            0, nodo
        )  # Insertar al principio para construir el camino de atrás hacia adelante
        nodo = predecesor[nodo]

    for municipio in camino:
        camino[camino.index(municipio)] = diccionarioPosiciones[municipio]
    # Devuelve la distancia más corta desde el nodo origen al nodo destino y el camino
    return camino, distancia[destino]


#  * Implementacion del algoritmo de Bellman-Ford
def Bellman_Ford(origen, destino, diccionarioPosiciones):
    with open("Matriz.txt", "r") as f:
        matriz = crearMatriz(f)
        matriz_adyacencia = [fila[1:] for fila in matriz[1:]]
        matriz_adyacencia = [
            [float(peso) for peso in fila] for fila in matriz_adyacencia
        ]
    # Número de nodos
    n = len(matriz_adyacencia)

    for clave, valor in diccionarioPosiciones.items():
        if valor == origen.replace("_", " "):
            origen = clave
            break
    for clave, valor in diccionarioPosiciones.items():
        if valor == destino.replace("_", " "):
            destino = clave
            break

    # Inicialización
    distancia = [sys.maxsize] * n  # Inicializa las distancias a infinito
    predecesor = [-1] * n  # Inicializa los predecesores
    distancia[origen] = 0  # La distancia al nodo origen es 0

    # Relajación: se repite n-1 veces
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if matriz_adyacencia[u][v] != 0:  # Hay una arista de u a v
                    nueva_distancia = distancia[u] + matriz_adyacencia[u][v]
                    if nueva_distancia < distancia[v]:
                        distancia[v] = nueva_distancia
                        predecesor[v] = u  # Actualizamos el predecesor

    # Verificación de ciclos negativos
    for u in range(n):
        for v in range(n):
            if matriz_adyacencia[u][v] != 0:  # Hay una arista de u a v
                if distancia[u] + matriz_adyacencia[u][v] < distancia[v]:
                    print("El grafo contiene un ciclo de peso negativo.")
                    return None, None

    # Reconstruir el camino desde el origen hasta el destino
    camino = []
    actual = destino
    while actual != -1:
        camino.insert(
            0, actual
        )  # Insertar al principio para construir el camino de atrás hacia adelante
        actual = predecesor[actual]

    # Si no hay un camino al destino, distancia[destino] será infinito
    if distancia[destino] == sys.maxsize:
        print(f"No existe un camino del nodo {origen} al nodo {destino}.")
        return None, None

    for municipio in camino:
        camino[camino.index(municipio)] = diccionarioPosiciones[municipio]

    # Devuelve la distancia más corta desde el nodo origen al nodo destino y el camino
    return camino, distancia[destino]


# for municipio in algoritmo_Kruskal():
#     print(municipio)
# print("\n ---------------- \n")
# for municipio in algoritmo_Prim():
#     print(municipio)



# Municipios, Distancia = busqueda("Cucuta", "Puerto_Trujillo","GBFS")
# for x in Municipios:
#     print(x)
# print(Distancia)

# diccionarioPosiciones = {
#     0: "Leticia",
#     1: "Medellin",
#     2: "Arauca",
#     3: "Barranquilla",
#     4: "Bogota",
#     5: "Cartagena",
#     6: "Tunja",
#     7: "Manizales",
#     8: "Mitu",
#     9: "Yopal",
#     10: "Popayan",
#     11: "Valledupar",
#     12: "Quibdo",
#     13: "Monteria",
#     14: "Inirida",
#     15: "Riohacha",
#     16: "San Jose del Guaviare",
#     17: "Neiva",
#     18: "Santa Marta",
#     19: "Villavicencio",
#     20: "Pasto",
#     21: "Cucuta",
#     22: "Santa Rita",
#     23: "Armenia",
#     24: "Union",
#     25: "Bucaramanga",
#     26: "Sincelejo",
#     27: "Puerto Trujillo",
#     28: "Cali",
#     29: "Puerto Carreno",
# }
# distancia, recorrido = Dijkstra("Bogota", "Tunja",diccionarioPosiciones)
# for municipio in recorrido:
#     print(diccionarioPosiciones[municipio])
# print(distancia)
