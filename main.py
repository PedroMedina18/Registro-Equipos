import tkinter as tk
from client.MainFrame import MainFrame
import util.util_ventana as util_ventana
from  client.ScrollFrame import VerticalScrolledFrame


def main():
    # *se crea la ruta raiz
    root = tk.Tk()
    root.title("Sistema de Control de Equipos de Sistemas")
    root.resizable(0, 1)

    # *para agregar pantalla completa
    root.state("zoomed")

    # *tamaño de la ventana en caso de reducir
    width, height = 1250, 800   

    # *para que la ventana este centrada     
    util_ventana.centrar_ventana(root, width, height)   


    # *se invoca la ventana inicial
    MainFrame(root)

    root.mainloop()


if __name__ == "__main__":
    main()