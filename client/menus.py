import tkinter as tk


# *Funcion para crear la barra de menus
def menus(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width=300, heigh=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)

    menu_inicio.add_command(label="Crear Base de Datos")
    menu_inicio.add_command(label="Salir", command= root.destroy)


    barra_menu.add_cascade(label="Inicio", menu = menu_inicio)


