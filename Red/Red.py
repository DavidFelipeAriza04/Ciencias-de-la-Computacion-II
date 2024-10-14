from Router import Router
import random
import sys
import time

ROUTER_COUNT = 20 # se asume por ahora un total de 20 routers
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
def genMatrix(n: int):
    prob = lambda p: random.uniform(0,0.25) if p <= 0.8 else 1
    return [ [prob(random.uniform(0,1)) for i in range(0,n)] 
        for j in range(0,n)]

def adjacent(xs):
    out = []
    for i in range(0,len(xs)): 
        if xs[i]<1: out.append(i)
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
                    # print(f"No hay conexion {Routers[i].name} - {Routers[j].name}")
                # else:
                #     print(
                #         f"{Routers[i].name}  conectado con {Routers[j].name} con {matriz[i][j]}"
                #     )
                continue
            if Routers[j].name in diccionario_conexiones[Routers[i].name]:
                h = heuristica(Routers[i], Routers[j], probCaidas)
                # print(f"{Routers[i].name}  conectado con {Routers[j].name} con {h}")
                matriz[i][j] = h
                matriz[j][i] = h
                conexiones_revisadas.append([Routers[i].name, Routers[j].name])
    # print("Matriz de adyacencia creada:\n ")
    return matriz

def heuristica(RouterInicial: Router, RouterFinal: Router, probCaidas=[[0]*20]*20):
    i, j = RouterInicial.id(), RouterFinal.id()
    Ai, Af = RouterInicial.ancho_banda, RouterFinal.ancho_banda
    Pc = probCaidas[i][j]
    C = RouterInicial.caido(Pc)
    if C == 0 or Pc == 1: return 0
    return round((Ai + Af) / (1 - Pc), 4)
#    h = 0
#    router_final_caido = RouterFinal.caido(Pc)
#    if router_final_caido != 0:
#        h = (RouterInicial.ancho_banda + RouterFinal.ancho_banda) / router_final_caido
#    return h

def enviar_paquete(paquete, routers, probCaidas):
    print(f"Enviando paquete {paquete}...")
    rutas = []
    matriz = crear_matriz(probCaidas)
    for row in matriz: print(row)
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
    # for i in range(len(camino)):
    #     print(camino[i] + 1, end=", ")
    # print("\n")
    for router in camino:
        # print(routers[router].name)
        # print(router2)
        # print(router + 1)
        if len(camino) != 1:
            if camino.index(router) + 1 < len(camino):
                # print(camino[camino.index(router) + 1] + 1)
                if (
                    routers[camino[camino.index(router) + 1]].name
                    in diccionario_conexiones[routers[router].name]
                ):
                    # print(
                    #     f"{routers[router].name} conectado con {routers[camino[camino.index(router)+1]].name}"
                    # )
                    pass
                else:
                    # print(
                    #     f"No hay conexion {routers[router].name} - {routers[camino[camino.index(router)+1]].name}"
                    # )
                    return None
    if len(camino) == 1:
        return None
    # Devuelve la distancia más corta desde el nodo origen al nodo destino y el camino
    return camino

#matriz = crear_matriz()

#nombresRouters = ["Router" + str(i+1) for i in range(0,ROUTER_COUNT)]

Routers = [None] * 20

for i in range(len(Routers)):
    Routers[i] = Router(
        f"Router{i+1}", random.randint(1, 100), diccionario_conexiones[f"Router{i+1}"]
    )

probCaidas = genMatrix(ROUTER_COUNT)
matriz = [[0 for i in range(20)] for j in range(20)]
matriz = crear_matriz(probCaidas)

# for Router in Routers:
#     print(Router.name)


# for i in range(20):
#     for j in range(20):
#         print(str(matriz[i][j]).ljust(4) ,end=" ")
#     print("\n")

# print(matriz[0])

paquete = input("Ingrese la frase a enviar: ")
paquete = dividir(paquete, 4)
# print(f"\n + {paquete}")
# for i in range(len(paquete)):
#     print(paquete[i], end="")

caminos = enviar_paquete(paquete, Routers, probCaidas)
# if caminos == None:
#     print("No se pudo enviar el paquete")
#     exit()
# print("\n")
# print(caminos)
for i in range(len(caminos)):
    print("\n")
    if caminos[i] == None:
        print(f"No se pudo enviar el paquete {paquete[i]}")
    else:
        print(
            f"Paquete {paquete[i]} enviado exitosamente por el camino: "
        )
        for j in range(len(caminos[i])):
            if j == len(caminos[i]) - 1:
                print(caminos[i][j]+1, end=".")
                break
            print(caminos[i][j]+1, end=" -> ")