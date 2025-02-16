from Router import Router
import random
import sys
import time

ROUTER_COUNT = 20  # se asume por ahora un total de 20 routers
BIG_NUM = 1000000
diccionario_conexiones = {
    "Router1": ["Router3"],
    "Router2": ["Router3", "Router9"],
    "Router3": ["Router1", "Router2", "Router4", "Router5"],
    "Router4": ["Router3", "Router5", "Router6"],
    "Router5": ["Router3", "Router4", "Router6", "Router9"],
    "Router6": ["Router4", "Router5", "Router7", "Router13"],
    "Router7": ["Router6", "Router8", "Router13"],
    "Router8": ["Router7", "Router9", "Router11"],
    "Router9": ["Router2", "Router5", "Router8", "Router10"],
    "Router10": ["Router9", "Router11", "Router16"],
    "Router11": ["Router8", "Router10", "Router12", "Router16"],
    "Router12": ["Router11", "Router13", "Router14"],
    "Router13": ["Router6", "Router7", "Router12", "Router15"],
    "Router14": ["Router12", "Router15", "Router16"],
    "Router15": ["Router13", "Router14", "Router18"],
    "Router16": ["Router10", "Router11", "Router14", "Router18", "Router19"],
    "Router17": ["Router18", "Router19"],
    "Router18": ["Router15", "Router16", "Router17", "Router20"],
    "Router19": ["Router16", "Router17"],
    "Router20": ["Router18"],
}

# genera matriz de adyacencias con probabilidades de caída de enlace
# def genMatrix(n: int):
#     higher_prob_indices = [2, 9, 10, 16, 19, 17, 4, 6, 13, 15]
#     def prob(p, index):
#         if index in higher_prob_indices:
#             # Para estos índices, aumentamos la probabilidad de fallo
#             return random.uniform(0.5, 1)  # Probabilidad mayor entre 0.5 y 1
#         else:
#             # Para los otros índices, mantenemos la lógica original
#             return random.uniform(0, 0.20) if p <= 0.8 else 1
#     probabilidad = lambda p: random.uniform(0,0.25) if p <= 0.8 else 1
#     return [ [probabilidad(random.uniform(0,1)) for i in range(0,n)]
#         for j in range(0,n)]


def genMatrix(n: int):
    # Lista de índices donde la probabilidad será mayor
    higher_prob_indices = [2, 9, 10, 16, 19, 17, 4, 6, 13, 15]

    # Función para asignar la probabilidad
    def prob(p, index):
        if index in higher_prob_indices:
            return random.uniform(0, 0.20) if p <= 0.7 else 1
        else:
            return random.uniform(0, 0.10) if p <= 0.9 else 1

    # Generar la matriz de adyacencias
    return [[prob(random.uniform(0, 1), j * n + i) for i in range(n)] for j in range(n)]


def adjacent(xs):
    out = []
    for i in range(0, len(xs)):
        if xs[i] < 1:
            out.append(i)
    return out


conexiones_revisadas = []


def crear_matriz(probCaidas):
    conexiones_revisadas.clear()
    for i in range(20):
        for j in range(20):
            if [Routers[i].name, Routers[j].name] in conexiones_revisadas or [
                Routers[j].name,
                Routers[i].name,
            ] in conexiones_revisadas:
                if matriz[i][j] == 0:
                    pass
                continue
            if Routers[j].name in diccionario_conexiones[Routers[i].name]:
                h = heuristica(Routers[i], Routers[j], probCaidas)
                matriz[i][j] = h
                matriz[j][i] = h
                conexiones_revisadas.append([Routers[i].name, Routers[j].name])
    return matriz


def heuristica(RouterInicial: Router, RouterFinal: Router, probCaidas=[[0] * 20] * 20):
    i, j = RouterInicial.id(), RouterFinal.id()
    Ai, Af = RouterInicial.ancho_banda, RouterFinal.ancho_banda
    Pc = probCaidas[i][j]
    C = RouterInicial.caido(Pc)
    if C == 0 or Pc == 1:
        return 0
    return round((Ai + Af) / (1 - Pc), 4)


def enviar_paquete(paquete, routers, probCaidas):
    print(f"Enviando paquete {paquete}...")
    rutas = []
    matriz = crear_matriz(probCaidas)
    for parte in paquete:
        print(f"Enviando parte {parte}...")
        camino = Dijkstra(0, 19, matriz, routers, probCaidas)
        rutas.append(camino)
        time.sleep(1)
    return rutas


def dividir(texto, tamano):
    return [texto[i : i + tamano] for i in range(0, len(texto), tamano)]


def Dijkstra(origen, destino, matriz_adyacencia, routers, probCaidas):
    n = len(matriz_adyacencia)
    # Inicialización
    distancia = [sys.maxsize] * n  # Inicializa las distancias a infinito
    predecesor = [-1] * n  # Inicializa los predecesores
    distancia[origen] = 0  # La distancia al nodo origen es 0
    visitado = [False] * n  # Inicializa todos los nodos como no visitados

    for _ in range(n):
        if _ != origen:
            matriz_adyacencia = crear_matriz(probCaidas)
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
    for router in camino:
        if len(camino) != 1:
            if camino.index(router) + 1 < len(camino):
                # print(camino[camino.index(router) + 1] + 1)
                if (
                    routers[camino[camino.index(router) + 1]].name
                    in diccionario_conexiones[routers[router].name]
                ):
                    # EXISTE CONEXION ENTRE LOS ROUTERS
                    pass
                else:
                    # NO EXISTE CONEXION ENTRE LOS ROUTERS
                    return None
    if len(camino) == 1:
        return None
    # Devuelve la distancia más corta desde el nodo origen al nodo destino y el camino
    return camino


Routers = [None] * 20

for i in range(len(Routers)):
    Routers[i] = Router(
        f"Router{i+1}", random.randint(1, 100), diccionario_conexiones[f"Router{i+1}"]
    )

probCaidas = genMatrix(ROUTER_COUNT)
matriz = [[0 for i in range(20)] for j in range(20)]
matriz = crear_matriz(probCaidas)

paquete = input("Ingrese la frase a enviar: ")
paquete = dividir(paquete, 4)

caminos = enviar_paquete(paquete, Routers, probCaidas)

for i in range(len(caminos)):
    print("\n")
    if caminos[i] == None:
        print(f"No se pudo enviar el paquete {paquete[i]}")
    else:
        print(f"Paquete {paquete[i]} enviado exitosamente por el camino: ")
        for j in range(len(caminos[i])):
            if j == len(caminos[i]) - 1:
                print(caminos[i][j] + 1, end=".")
                break
            print(caminos[i][j] + 1, end=" -> ")
