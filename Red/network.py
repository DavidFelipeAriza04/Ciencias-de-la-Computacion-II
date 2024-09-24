import random as rd


ROUTER_COUNT = 20
# genera matriz de adyacencias con probabilidades de caída de enlace
def genMatrix(n: int):
    prob = lambda p: p if (p <= 0.4) else 1
    return [ [prob(rd.uniform(0,1)) for i in range(0,n)] 
        for j in range(0,n)]

# genera una lista que asocia a cada router (enumerado) con una banda ancha
def genBandwidths(n: int, minim: float, maxim: float):
    return [rd.uniform(minim,maxim) for i in range(0,n)]

# dada la probabilidad de caída y la banda ancha, calcula la heurística de
# dos nodos conectados

node_count = 12 # total de routers asumido
minW, maxW = 0.4, 9; # rango de banda ancha asumido
network = genMatrix(node_count)
bandwiths = genBandwidths(node_count, minW, maxW)
H = lambda n,m: heuristic(network, bandwiths, n, m) # H(n,m)

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

nombresRouters = ["Router" + str(i+1) for i in range(0,ROUTER_COUNT)]
diccionario_conexiones = {
    nombresRouters[i] : ["Router"+str(j+1) for j in adjacent(matriz[i])]
    for i in range(0,ROUTER_COUNT)
}

def dijkstra(graph, node1, node2):
	visited = [node1]