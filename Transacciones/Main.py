from Transaccion import Transaccion
import Busqueda
from Producto import Producto
from Persona import Persona
from datetime import datetime
import random as rnd


def hash(arr_size, query: str):
    xor = ord(query[0])
    for c in query:
        xor <<= ord(c)
    rnd.seed(xor)
    return rnd.randint(0, arr_size)


def main():
    # Crear productos
    array1 = [None] * 600000
    array2 = [None] * 600000
    array3 = [None] * 600000
    array4 = [None] * 600000
    array5 = [None] * 600000
    productos = Busqueda.cargar_productos()
    print("Productos cargados")
    op = 0
    item_buscar = ""
    trasnsaccionAnterior = None
    while op != 4:
        print("\nTransacciones")
        print("1. Agregar transaccion")
        print("2. Buscar transaccion")
        print("3. Intentar modificar transaccion")
        print("4. Salir")
        op = int(input())
        if op == 1:
            print(
                "\nPor que item desea agregar el producto a la transaccion:\n1. Id\n2. Nombre"
            )
            op_buscar = int(input())
            if op_buscar == 1:
                item_buscar = int(input("Ingresa el id: "))
                productos.sort(key=lambda p: p.get_id())
                producto = None
                while producto is None:
                    producto = Busqueda.obtener_producto(
                        item_buscar,
                        Busqueda.busqueda_binaria,
                        productos,
                        key=lambda p: p.get_id(),
                    )

            elif op_buscar == 2:
                item_buscar = input("Ingresa el nombre: ")
                productos.sort(key=lambda p: p.get_name())
                producto = None
                while producto is None:
                    producto = Busqueda.obtener_producto(
                        item_buscar,
                        Busqueda.busqueda_binaria,
                        productos,
                        key=lambda p: p.get_name(),
                    )
            Busqueda.imprimir_producto(producto)
            cliente = Persona(
                input("Nombre del cliente: "), int(input("Id del cliente: "))
            )
            vendedor = Persona(
                input("Nombre del vendedor: "), int(input("Id del vendedor: "))
            )
            # print(hash(len(productos),producto.get_name()))
            hash_value = hash(len(productos), producto.get_name())
            transaccion = Transaccion(
                hash_value,
                datetime.now(),
                producto,
                cliente,
                vendedor,
                trasnsaccionAnterior,
            )

            trasnsaccionAnterior = hash_value
            transaccion.imprimirTransaccion()
            num_array = rnd.randint(1, 5)
            if num_array == 1:
                if array1[hash_value] is not None:
                    print("Se genero una colision")
                    array1[hash_value].set_SiguienteTransaccion(transaccion)
                else:
                    array1[hash_value] = transaccion
                array2[hash_value] = array1[hash_value]
                array3[hash_value] = array1[hash_value]
                array4[hash_value] = array1[hash_value]
                array5[hash_value] = array1[hash_value]
            elif num_array == 2:
                if array2[hash_value] is not None:
                    print("Se genero una colision")
                    array2[hash_value].set_SiguienteTransaccion(transaccion)
                else:
                    array2[hash_value] = transaccion
                array1[hash_value] = array2[hash_value]
                array3[hash_value] = array2[hash_value]
                array4[hash_value] = array2[hash_value]
                array5[hash_value] = array2[hash_value]
            elif num_array == 3:
                if array3[hash_value] is not None:
                    print("Se genero una colision")
                    array3[hash_value].set_SiguienteTransaccion(transaccion)
                else:
                    array3[hash_value] = transaccion
                array1[hash_value] = array3[hash_value]
                array2[hash_value] = array3[hash_value]
                array4[hash_value] = array3[hash_value]
                array5[hash_value] = array3[hash_value]
            elif num_array == 4:
                if array4[hash_value] is not None:
                    print("Se genero una colision")
                    array4[hash_value].set_SiguienteTransaccion(transaccion)
                else:
                    array4[hash_value] = transaccion
                array1[hash_value] = array4[hash_value]
                array2[hash_value] = array4[hash_value]
                array3[hash_value] = array4[hash_value]
                array5[hash_value] = array4[hash_value]
            elif num_array == 5:
                if array5[hash_value] is not None:
                    print("Se genero una colision")
                    array5[hash_value].set_SiguienteTransaccion(transaccion)
                else:
                    array5[hash_value] = transaccion
                array1[hash_value] = array5[hash_value]
                array2[hash_value] = array5[hash_value]
                array3[hash_value] = array5[hash_value]
                array4[hash_value] = array5[hash_value]
            print("Transaccion guardada en el array: ", num_array)
        if op == 2:
            print("Ingrese el id de la transaccion a buscar: ")
            id_transaccion = int(input())
            if array1[id_transaccion] is not None:
                array1[id_transaccion].imprimirTransaccion()
            else:
                print("Transaccion no encontrada")
        if op == 3:
            print("Ingrese el id de la transaccion a modificar: ")
            id_transaccion = int(input())
            if array1[id_transaccion] is not None:
                producto = None
                while producto is None:
                    producto = Busqueda.obtener_producto(
                        int(input("Ingrese el id del nuevo producto: ")),
                        Busqueda.busqueda_binaria,
                        productos,
                        key=lambda p: p.get_id(),
                    )
                Busqueda.imprimir_producto(producto)
                cliente = Persona(
                    input("Nombre del cliente: "), int(input("Id del cliente: "))
                )
                vendedor = Persona(
                    input("Nombre del vendedor: "), int(input("Id del vendedor: "))
                )
                hash_value = hash(len(productos), producto.get_name())
                if not array1[id_transaccion].get_id() == hash_value:
                    print("\n!!!!Intento de fraude!!!!")
            else:
                print("Transaccion no encontrada")


if __name__ == "__main__":
    main()
