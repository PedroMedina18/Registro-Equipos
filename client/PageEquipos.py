import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    FONT_LABEL,
    FONT_LABEL_TITULO,
    COLOR_BASE,
    COLOR_AZUL,
    TITULO_CAMPOS,
    COLOR_ROJO,
    COLOR_VERDE,
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    TAMAÑO_BOTON,
    ACTIVE_ROJO,
    TAMAÑO_ENTRYS,
)

class PageEquipos:

    def __init__(self, root, *args):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = args[0]
        self.id_equipo = None
        self.crearCuerpo()
        self.lista_Equipos()

    # *para crear el cuerpo principal
    def crearCuerpo(self):
        if self.framePrincipal:
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)
        else:
            self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)

    # *la primera lista en donde se ven todas las tablas
    def lista_Equipos(self):
        self.framePrincipal.columnconfigure(0, weight=1)

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Lista de Equipos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10)

        self.list_tabla = Tablas.list()
        self.list_tabla.reverse()

        self.tabla_listTablas = ttk.Treeview(
            self.framePrincipal, columns=("Nombre", "Descripcion"), height=30
        )
        self.tabla_listTablas.grid(row=1, column=0, sticky="NSEW", padx=10, columnspan=2)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_listTablas.yview
        )
        scroll.grid(row=1, column=1, sticky="nsew")
        self.tabla_listTablas.configure(yscrollcommand=scroll.set)

        self.tabla_listTablas.heading("#0", text="ID", anchor=tk.W)
        self.tabla_listTablas.heading("#1", text="NOMBRE", anchor=tk.W)
        self.tabla_listTablas.heading("#2", text="DESCRIPCIÓN", anchor=tk.W)


        # edit column
        self.tabla_listTablas.column("#0", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listTablas.column("#1", stretch=tk.NO, minwidth="25", width="250")
        self.tabla_listTablas.column("#2", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        for item in self.list_tabla:
            self.tabla_listTablas.insert("", 0, text=item[0], values=(item[1], item[2]))

        # botones finales

        # Ir
        self.boton_buscar = tk.Button(self.framePrincipal, text="Buscar")
        self.boton_buscar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
            command=self.buscarDataTabla,
        )
        self.boton_buscar.grid(row=2, column=0, padx=10, pady=10)