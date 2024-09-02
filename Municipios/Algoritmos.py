import heapq
from Nodo import Pueblo,Nodo
from math import radians, cos, sin, asin, sqrt

def crearMatriz(f):
    matriz_adyacencia = [linea.split() for linea in f if linea.strip()]
    return matriz_adyacencia

def buscarCoordMunicipio(nombre, matriz_adyacencia):
    try:
        i = matriz_adyacencia[0].index(nombre)
    except ValueError:
        raise ValueError(f"Municipio '{nombre}' no encontrado en la cabecera de columnas.")

    for index,fila in enumerate(matriz_adyacencia[1:],start=1):
        if fila[0] == nombre:
            return(index,i)

def comprobarDestino(cordOrigen, cordsDestino):
    return cordOrigen == cordsDestino

def crearArregloPueblos(matrizAdyacencia):
    archivo_municipios = open("Municipios.txt","r")
    arreglo_pueblos = []
    for linea in archivo_municipios:
        atributos_pueblo = linea.split(",")
        pueblo = Pueblo(
                        atributos_pueblo[0].strip(),
                        float(atributos_pueblo[1]),
                        float(atributos_pueblo[2]),
                        None,
                        buscarCoordMunicipio(atributos_pueblo[0].strip(),matrizAdyacencia))
        
        arreglo_pueblos.append(pueblo)
    return arreglo_pueblos

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
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a)) 
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def buscarMunicipio(nombre,arregloPueblos):
    return next((pueblo for pueblo in arregloPueblos if pueblo.nombre == nombre), None)

def calculaHeristica(pueblo,arregloPueblos,destino,):
    puebloDestino =  buscarMunicipio(destino,arregloPueblos)
    latD = puebloDestino.latitud 
    longD = puebloDestino.longitud
    
    pueblo.heuristica = distance(pueblo.latitud,latD,pueblo.longitud,longD)

def calculaHeristicaA(pueblo,arregloPueblos,destino,costoActual):
    puebloDestino =  buscarMunicipio(destino,arregloPueblos)
    latD = puebloDestino.latitud 
    longD = puebloDestino.longitud

    pueblo.heuristica = distance(pueblo.latitud,latD,pueblo.longitud,longD)+costoActual

    
def buscarPueblosPosibles(matrizAdyacencia,fila):
    linea = matrizAdyacencia[fila]
    pueblosAdyacentes = []

    for i, elemento in enumerate(linea[1:], start=1):
        if elemento: 
            if float(elemento) != 0:
                pueblosAdyacentes.append(i)

    return pueblosAdyacentes

def estado_en_frontera(frontera, estado):
    return any(nodo.estado == estado for nodo in frontera)


def GBFS(origen,destino):
    f = open("Matriz.txt","r")
    matriz = crearMatriz(f)
    arreglo_pueblos = crearArregloPueblos(matriz)

    cordDestino = buscarCoordMunicipio(destino,matriz)

    puebloInicial = buscarMunicipio(origen,arreglo_pueblos)
    calculaHeristica(puebloInicial,arreglo_pueblos,destino)

    start = Nodo(puebloInicial,None,buscarCoordMunicipio(origen,matriz),puebloInicial.heuristica)
    frontera = []
    heapq.heapify(frontera)
    heapq.heappush(frontera, start)
    conjuntoExplorado = set()

    while True:
        if not frontera:
            raise Exception("No solution")
        
        nodo = heapq.heappop(frontera)

        if comprobarDestino((nodo.estado.x, nodo.estado.y),cordDestino):
            nodos = [] 
            while nodo.padre is not None:
                nodos.append(nodo.estado)
                nodo = nodo.padre
            
            nodos.append(start.estado)
            nodos.reverse()
            
            return nodos
        
        conjuntoExplorado.add(nodo.estado)

        cordsPueblosAdy = buscarPueblosPosibles(matriz,nodo.estado.x)
        pueblosAdyacentes = []

        for cordPueblo in cordsPueblosAdy:
            pueblo = buscarMunicipio(matriz[0][cordPueblo],arreglo_pueblos)
            calculaHeristica(pueblo,arreglo_pueblos,destino)
            pueblosAdyacentes.append(pueblo)

        for pueblo in pueblosAdyacentes:
            if pueblo not in conjuntoExplorado and not estado_en_frontera(frontera,pueblo):
                nodo_hijo = Nodo(pueblo,nodo,buscarCoordMunicipio(pueblo.nombre,matriz),pueblo.heuristica)
                heapq.heappush(frontera, nodo_hijo)

def A(origen,destino):
    f = open("Matriz.txt","r")
    matriz = crearMatriz(f)
    arreglo_pueblos = crearArregloPueblos(matriz)

    cordDestino = buscarCoordMunicipio(destino,matriz)
    costoActual = 0

    puebloInicial = buscarMunicipio(origen,arreglo_pueblos)
    calculaHeristicaA(puebloInicial,arreglo_pueblos,destino,costoActual)

    start = Nodo(puebloInicial,None,buscarCoordMunicipio(origen,matriz),puebloInicial.heuristica)
    frontera = []
    heapq.heapify(frontera)
    heapq.heappush(frontera, start)
    conjuntoExplorado = set()

    while True:
        if not frontera:
            raise Exception("No solution")
        
        nodo = heapq.heappop(frontera)

        if comprobarDestino((nodo.estado.x, nodo.estado.y),cordDestino):
            nodos = [] 
            while nodo.padre is not None:
                nodos.append(nodo.estado)
                nodo = nodo.padre
            
            nodos.append(start.estado)
            nodos.reverse()
            
            return nodos
        
        conjuntoExplorado.add(nodo.estado)

        cordsPueblosAdy = buscarPueblosPosibles(matriz,nodo.estado.x)
        pueblosAdyacentes = []

        for cordPueblo in cordsPueblosAdy:
            pueblo = buscarMunicipio(matriz[0][cordPueblo],arreglo_pueblos)
            calculaHeristicaA(pueblo,arreglo_pueblos,destino,costoActual+float(matriz[pueblo.x][nodo.estado.y]))
            pueblosAdyacentes.append(pueblo)

        for pueblo in pueblosAdyacentes:
            if pueblo not in conjuntoExplorado and not estado_en_frontera(frontera,pueblo):
                nodo_hijo = Nodo(pueblo,nodo,buscarCoordMunicipio(pueblo.nombre,matriz),pueblo.heuristica)
                heapq.heappush(frontera, nodo_hijo)
                costoActual+=float(matriz[nodo.estado.x][nodo_hijo.estado.y])

xd = (A("Leticia","Monteria"))

sum = 0 
for i in range(0,len(xd)-1):
    sum+=distance(xd[i].x,xd[i+1].x,xd[i].y,xd[i+1].y)

for x in xd:
    print(x.nombre)
print(sum)