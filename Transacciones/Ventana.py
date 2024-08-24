from tkinter import ttk
import tkinter as tk

width = 800
height = 400


class Ventana(ttk.Frame):
    
    def CambiarTexto(self):
        self.nombre_id_producto.set("Producto: " + self.entrada.get())
    
    def __init__(self, ventana_principal):
        self.nombre_id_producto = tk.StringVar(ventana_principal, value="Producto: ")
        self.entrada = tk.StringVar(ventana_principal)
        super().__init__(ventana_principal)
        ventana_principal.configure(width=width, height=height)
        ventana_principal.title("Transacciones")
        self.place(x=width / 4, y=height / 4, width=width / 2, height=height / 2)
        self.configure(borderwidth=2, relief="solid")
        self.button = ttk.Button(self, text="Agregar Transacción", command=self.CambiarTexto)
        self.button.place(x=((width / 2)-120)/2, y=90, width=120, height=30)
        self.entry = ttk.Entry(self, textvariable=self.entrada)
        self.entry.place(x=((width / 2)-120)/2, y=30, width=120, height=30)
        # self.entry.state(["disabled"])
        # self.radiobutton = ttk.Radiobutton(self)
        # self.radiobutton.place(x=250, y=30, width=50, height=30)
        self.label = ttk.Label(
            self,
            textvariable=self.nombre_id_producto,
        )
        self.label.place(x=((width / 2)-120)/2, y=0, width=120, height=30)

    def DevolverNombreId(self):
        return self.nombre_id_producto.get()
