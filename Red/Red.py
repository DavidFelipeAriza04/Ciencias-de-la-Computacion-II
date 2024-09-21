from Router import Router
import random
import sys
import time

ROUTER_COUNT = 20 # se asume por ahora un total de 20 routers

# genera matriz de adyacencias con probabilidades de caída de enlace
def genMatrix(n: int):
    rd = random
    prob = lambda p: p if (p <= 0.2) else 1
    return [ [prob(rd.uniform(0,1)) for i in range(0,n)] 
        for j in range(0,n)]

def adjacent(xs):
    out = []
    for i in range(0,len(xs)): 
        if xs[i]<1: out.append(i)
    return out

matriz = genMatrix(ROUTER_COUNT)
nombresRouters = ["Router" + str(i+1) for i in range(0,ROUTER_COUNT)]
diccionario_conexiones = {
    nombresRouters[i] : ["Router"+str(j+1) for j in adjacent(matriz[i])]
    for i in range(0,ROUTER_COUNT)
}

conexiones_revisadas = []


def crear_matriz():
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
                h = heuristica(Routers[i], Routers[j])
                # print(f"{Routers[i].name}  conectado con {Routers[j].name} con {h}")
                matriz[i][j] = h
                matriz[j][i] = h
                conexiones_revisadas.append([Routers[i].name, Routers[j].name])
    # print("Matriz de adyacencia creada:\n ")
    return matriz


def heuristic(matrix, bandwiths, n, m):
    prob = lambda p: 1 if (rd.uniform(0,1) >= p) else 0
    denominator = prob(matrix[n][m]) * (1 - matrix[n][m])
    if (denominator == 0): return BIG_NUM
    else: return (bandwiths[n] + bandwiths[m]) / denominator

def heuristica(RouterInicial, RouterFinal):
    h = 0
    router_final_caido = RouterFinal.caido()
    if router_final_caido != 0:
        h = (RouterInicial.ancho_banda + RouterFinal.ancho_banda) / router_final_caido
    return h


def enviar_paquete(paquete, routers):
    print(f"Enviando paquete {paquete}...")
    rutas = []
    for parte in paquete:
        print(f"Enviando parte {parte}...")
        matriz = crear_matriz()
        camino = Dijkstra(0, 19, matriz, routers)
        rutas.append(camino)
        time.sleep(2)
    return rutas


def dividir(texto, tamano):
    return [texto[i : i + tamano] for i in range(0, len(texto), tamano)]


def Dijkstra(origen, destino, matriz_adyacencia, routers):
    n = len(matriz_adyacencia)
    # Inicialización
    distancia = [sys.maxsize] * n  # Inicializa las distancias a infinito
    predecesor = [-1] * n  # Inicializa los predecesores
    distancia[origen] = 0  # La distancia al nodo origen es 0
    visitado = [False] * n  # Inicializa todos los nodos como no visitados

    for _ in range(n):
        if _ != origen:
            matriz_adyacencia = crear_matriz()
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

for nombre in nombresRouters:
    print(diccionario_conexiones[nombre])

Routers = [None] * 20


for i in range(len(Routers)):
    Routers[i] = Router(
        f"Router{i+1}", random.randint(1, 100), diccionario_conexiones[f"Router{i+1}"]
    )

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

caminos = enviar_paquete(paquete, Routers)
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
