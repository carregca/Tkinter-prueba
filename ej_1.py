import tkinter as tk
from PIL import Image, ImageTk

class FutbolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alineación de Fútbol")
        self.root.geometry("600x770")
        self.root.resizable(False, False)
        
        img_cancha = Image.open("assets/cancha.png")
        img_cancha = img_cancha.resize((600, 770))
        self.cancha_img = ImageTk.PhotoImage(img_cancha)

        img_jugador = Image.open("assets/jugador.png")
        img_jugador = img_jugador.resize((100, 106))
        self.jugador_img = ImageTk.PhotoImage(img_jugador)

        self.fondo = tk.Label(root, image=self.cancha_img)
        self.fondo.place(x=0, y=0)

        self.jugadores = []

        posiciones = [
            (250, 650),
            (100, 500), (200, 500), (300, 500), (400, 500),
            (150, 350), (250, 350), (350, 350),
            (150, 150), (250, 100), (350, 150)
        ]

        for x, y in posiciones:
            lbl = tk.Label(root, image=self.jugador_img, bd=0)
            lbl.place(x=x, y=y)

            lbl.bind("<Button-1>", self.iniciar_arrastre)
            lbl.bind("<B1-Motion>", self.arrastrar)
            lbl.bind("<ButtonRelease-1>", self.soltar)

            self.jugadores.append(lbl)

    def iniciar_arrastre(self, event):
        widget = event.widget
        widget.lift()
        widget.startX = event.x
        widget.startY = event.y

    def arrastrar(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        widget.place(x=x, y=y)

    def soltar(self, event):
        widget = event.widget
        x1, y1 = widget.winfo_x(), widget.winfo_y()

        for otro in self.jugadores:
            if otro != widget:
                x2, y2 = otro.winfo_x(), otro.winfo_y()

                if abs(x1 - x2) < 50 and abs(y1 - y2) < 50:
                    widget.place(x=x2, y=y2)
                    otro.place(x=x1, y=y1)
                    break


if __name__ == "__main__":
    root = tk.Tk()
    app = FutbolApp(root)
    root.mainloop()