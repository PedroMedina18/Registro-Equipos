import tkinter as tk
from client.MainFrame import MainFrame
import util.util_ventana as util_ventana


def main():
    root = tk.Tk()
    root.title("Sistema de Control de Equipos de Sistemas")
    width=root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    # w, h = 1024, 600        
    # util_ventana.centrar_ventana(root, w, h)   
    MainFrame(root = root)


    root.mainloop()


if __name__ == "__main__":
    main()