import pandas as pd
from Producto import Producto
import time


def busqueda_binaria(elemento, arreglo, key):
    inicio, final = 0, len(arreglo) - 1
    while inicio <= final:
        medio = (inicio + final) // 2
        medio_elemento = key(arreglo[medio])
        if elemento == medio_elemento:
            return medio
        elif elemento > medio_elemento:
            inicio = medio + 1
        else:
            final = medio - 1
    return -1


def busqueda_secuencial(elemento, arreglo, key):
    for indice, a in enumerate(arreglo):
        if elemento == key(a):
            return indice
        else:
            if elemento == a:
                return indice
    return -1


def menu_obtener_producto(item_buscar, productos, key):
    print(
        "Por que metodo desea buscar el producto:\n1. Busqueda Binaria\n2. Busqueda Secuencial"
    )
    op_busqueda = int(input())

    if op_busqueda == 1:
        producto, tiempo = obtener_producto(
            item_buscar, busqueda_binaria, productos, key
        )
    elif op_busqueda == 2:
        producto, tiempo = obtener_producto(
            item_buscar, busqueda_secuencial, productos, key
        )
    else:
        print("Opción inválida")
        return

    print("Producto encontrado:" if producto else "Producto no encontrado")
    imprimir_producto(producto) if producto else None
    print(f"Tiempo de búsqueda: {tiempo:.4f} segundos")


def obtener_producto(item_buscar, busqueda, productos, key):
    start = time.perf_counter()
    indice = busqueda(item_buscar, productos, key)
    end = time.perf_counter()

    # Verifica si se encontró el índice
    if indice != -1:
        producto = productos[indice]
    else:
        producto = None

    tiempo = end - start
    return producto, tiempo


def imprimir_producto(producto):
    print(
        f"id: {producto.get_id()}\nNombre: {producto.get_name()}\nPrecio: {producto.get_price()}\nDescripcion: {producto.get_description()}"
    )


def cargar_productos():
    df = pd.read_csv("Amazon-Products.csv")

    productos = []
    indice = 0
    for index, row in df.iterrows():
        productos.append(
            Producto(indice, row["name"], row["actual_price"], row["main_category"])
        )
        indice += 1
    return productos


def main():
    productos = cargar_productos()
    op = 0
    while op != 3:
        print("\nPor que item desea buscar el producto:\n1. Id\n2. Nombre\n3. Salir")
        op = int(input())
        item_buscar = ""

        if op == 1:
            item_buscar = int(input("Ingresa el id: "))
            productos.sort(key=lambda p: p.get_id())
            menu_obtener_producto(item_buscar, productos, key=lambda p: p.get_id())

        elif op == 2:
            item_buscar = input("Ingresa el nombre: ")
            productos.sort(key=lambda p: p.get_name())
            menu_obtener_producto(item_buscar, productos, key=lambda p: p.get_name())


main()
