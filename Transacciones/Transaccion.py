class Transaccion:
    def __init__(
        self, id: str, date, product, customer, seller, transaccionAnterior: str
    ):
        self.id = id
        self.date = date
        self.product = product
        self.price = product.get_price()
        self.customer = customer
        self.seller = seller
        self.transaccionAnterior = transaccionAnterior
        self.siguienteTransaccion = None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_product(self):
        return self.product

    def set_product(self, product):
        self.product = product
        self.price = product.get_price()  # Update price when product is set

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_seller(self):
        return self.seller

    def set_seller(self, seller):
        self.seller = seller

    def get_transaccionAnterior(self):
        return self.transaccionAnterior

    def set_transaccionAnterior(self, transaccionAnterior):
        self.transaccionAnterior = transaccionAnterior

    def imprimirTransaccion(self):
        print(
            f"Transaccion Anterior: {self.transaccionAnterior}\nTransaccion: {self.id}\nFecha: {self.date}\nProducto:{self.product.get_id()}: {self.product.get_name()}\nPrecio: {self.price}\nCliente: {self.customer}\nVendedor: {self.seller}"
            , '\n---'
        )
        if not (self.siguienteTransaccion == None): self.siguienteTransaccion.imprimirTransaccion() 

    def set_SiguienteTransaccion(self, siguienteTransaccion):
        if self.siguienteTransaccion is None:
            self.siguienteTransaccion = siguienteTransaccion
        else:
            self.siguienteTransaccion.set_SiguienteTransaccion(siguienteTransaccion)
