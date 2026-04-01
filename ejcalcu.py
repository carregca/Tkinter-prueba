import tkinter as tk
from tkinter import messagebox
import math

def agregar(valor):
    pantalla.insert(tk.END, valor)

def limpiar():
    pantalla.delete(0, tk.END)

def calcular():
    try:
        expresion = pantalla.get()

        for c in expresion:
            if c.isalpha():
                raise ValueError("No se permiten letras")

        resultado = eval(expresion)
        limpiar()
        pantalla.insert(0, str(resultado))

    except ZeroDivisionError:
        messagebox.showerror("Error", "No se puede dividir por cero")
        limpiar()
    except Exception:
        messagebox.showerror("Error", "Expresión inválida")
        limpiar()

def potencia():
    try:
        valor = float(pantalla.get())
        limpiar()
        pantalla.insert(0, str(valor ** 2))
    except:
        messagebox.showerror("Error", "Valor inválido")
        limpiar()

def raiz():
    try:
        valor = float(pantalla.get())
        if valor < 0:
            raise ValueError
        limpiar()
        pantalla.insert(0, str(math.sqrt(valor)))
    except:
        messagebox.showerror("Error", "No se puede calcular la raíz")
        limpiar()

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("300x400")

pantalla = tk.Entry(ventana, font=("Arial", 18), bd=10, relief="sunken", justify="right")
pantalla.pack(fill="both", padx=5, pady=5)

frame = tk.Frame(ventana)
frame.pack()

botones = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('.',4,1), ('=',4,2), ('+',4,3),
]

for (texto, fila, col) in botones:
    if texto == "=":
        tk.Button(frame, text=texto, width=5, height=2, command=calcular)\
            .grid(row=fila, column=col)
    else:
        tk.Button(frame, text=texto, width=5, height=2,
                  command=lambda t=texto: agregar(t))\
            .grid(row=fila, column=col)

tk.Button(frame, text="C", width=5, height=2, command=limpiar)\
    .grid(row=5, column=0)

tk.Button(frame, text="x²", width=5, height=2, command=potencia)\
    .grid(row=5, column=1)

tk.Button(frame, text="√", width=5, height=2, command=raiz)\
    .grid(row=5, column=2)

ventana.mainloop()