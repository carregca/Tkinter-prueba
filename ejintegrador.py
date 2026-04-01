import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ARCHIVO = "inventario.json"

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("900x500")

        self.datos = []
        self.cargar_datos()

        panel_izq = ttk.LabelFrame(root, text="Panel de Operaciones")
        panel_izq.pack(side="left", fill="y", padx=10, pady=10)

        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_cantidad = tk.IntVar()

        ttk.Label(panel_izq, text="Código").pack()
        ttk.Entry(panel_izq, textvariable=self.var_codigo).pack()

        ttk.Label(panel_izq, text="Descripción").pack()
        ttk.Entry(panel_izq, textvariable=self.var_nombre).pack()

        ttk.Label(panel_izq, text="Precio").pack()
        ttk.Entry(panel_izq, textvariable=self.var_precio).pack()

        ttk.Label(panel_izq, text="Categoría").pack()
        ttk.Entry(panel_izq, textvariable=self.var_categoria).pack()

        ttk.Label(panel_izq, text="Cantidad").pack()
        ttk.Spinbox(panel_izq, from_=0, to=10000, textvariable=self.var_cantidad).pack()

        ttk.Button(panel_izq, text="Guardar", command=self.crear).pack(pady=5)
        ttk.Button(panel_izq, text="Modificar", command=self.modificar).pack(pady=5)
        ttk.Button(panel_izq, text="Borrar", command=self.borrar).pack(pady=5)

        panel_der = ttk.LabelFrame(root, text="Inventario")
        panel_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columnas = ("codigo", "descripcion", "precio", "categoria", "cantidad")

        self.tree = ttk.Treeview(panel_der, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(panel_der, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar)

        self.refrescar()

    def cargar_datos(self):
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r") as f:
                self.datos = json.load(f)

    def guardar_datos(self):
        with open(ARCHIVO, "w") as f:
            json.dump(self.datos, f, indent=4)

    def refrescar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto in self.datos:
            self.tree.insert("", tk.END, values=(
                producto["codigo"],
                producto["descripcion"],
                producto["precio"],
                producto["categoria"],
                producto["cantidad"]
            ))

    def limpiar(self):
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_categoria.set("")
        self.var_cantidad.set(0)

    def crear(self):
        try:
            codigo = self.var_codigo.get()
            descripcion = self.var_nombre.get()
            precio = float(self.var_precio.get())
            categoria = self.var_categoria.get()
            cantidad = int(self.var_cantidad.get())

            if not codigo or not descripcion:
                raise ValueError

            for p in self.datos:
                if p["codigo"] == codigo:
                    messagebox.showerror("Error", "El código ya existe")
                    return

            nuevo = {
                "codigo": codigo,
                "descripcion": descripcion,
                "precio": precio,
                "categoria": categoria,
                "cantidad": cantidad
            }

            self.datos.append(nuevo)
            self.guardar_datos()
            self.refrescar()
            self.limpiar()

        except:
            messagebox.showerror("Error", "Datos inválidos")

    def seleccionar(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion)["values"]

            self.var_codigo.set(valores[0])
            self.var_nombre.set(valores[1])
            self.var_precio.set(valores[2])
            self.var_categoria.set(valores[3])
            self.var_cantidad.set(valores[4])

    def modificar(self):
        codigo = self.var_codigo.get()

        for producto in self.datos:
            if producto["codigo"] == codigo:
                try:
                    producto["descripcion"] = self.var_nombre.get()
                    producto["precio"] = float(self.var_precio.get())
                    producto["categoria"] = self.var_categoria.get()
                    producto["cantidad"] = int(self.var_cantidad.get())

                    self.guardar_datos()
                    self.refrescar()
                    self.limpiar()
                    return
                except:
                    messagebox.showerror("Error", "Datos inválidos")
                    return

        messagebox.showerror("Error", "Producto no encontrado")

    def borrar(self):
        codigo = self.var_codigo.get()

        for i, producto in enumerate(self.datos):
            if producto["codigo"] == codigo:
                del self.datos[i]
                self.guardar_datos()
                self.refrescar()
                self.limpiar()
                return

        messagebox.showerror("Error", "Producto no encontrado")



if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()