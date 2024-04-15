import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    FONT_LABEL,
    FONT_LABEL_TITULO,
    COLOR_BASE,
    COLOR_AZUL,
    COLOR_VERDE,
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    TAMAÑO_BOTON,
    TAMAÑO_ENTRYS
)
from  models.equipos import Equipos

class PageEquipos:
    def __init__(self, root, cambio_cuerpo):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = cambio_cuerpo
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

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Lista de Equipos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=5)


        ## SELECT
        label_equipo = tk.Label(self.framePrincipal, text="Equipo")
        label_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_equipo.grid(row=1, column=0, padx=10, pady=10)

        select_tipo_equipo = ttk.Combobox(
            self.framePrincipal, state="readonly"
        )
        select_tipo_equipo.grid(row=2, column=0, padx=10, pady=10)


        label_ubicacion = tk.Label(self.framePrincipal, text="Ubicación")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=1, column=1, padx=10, pady=10)

        select_ubicacion = ttk.Combobox(
            self.framePrincipal, state="readonly"
        )
        select_ubicacion.grid(row=2, column=1, padx=10, pady=10)


        label_estado = tk.Label(self.framePrincipal, text="Estado")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=1, column=2, padx=10, pady=10)

        select_estado = ttk.Combobox(
            self.framePrincipal, state="readonly"
        )
        select_estado.grid(row=2, column=2, padx=10, pady=10)


        label_area = tk.Label(self.framePrincipal, text="Are de Trabajo")
        label_area.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area.grid(row=1, column=3, padx=10, pady=10)

        select_area_trabajo = ttk.Combobox(
            self.framePrincipal, state="readonly"
        )
        select_area_trabajo.grid(row=2, column=3, padx=10, pady=10)



        # TABLA
        self.list_tabla=[]
        # self.list_tabla = Equipos.list()
        # self.list_tabla.reverse()

        self.tabla_listEquipos = ttk.Treeview(
            self.framePrincipal, columns=("Serial", "Equipo", "Ubicación", "Estado", "Area"), height=30
        )
        self.tabla_listEquipos.grid(row=3, column=0, sticky="NSEW", padx=10, columnspan=8)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_listEquipos.yview
        )
        scroll.grid(row=3, column=7, sticky="ns")
        self.tabla_listEquipos.configure(yscrollcommand=scroll.set)

        self.tabla_listEquipos.heading("#0", text="ID", anchor=tk.W)
        self.tabla_listEquipos.heading("#1", text="SERIAL", anchor=tk.W)
        self.tabla_listEquipos.heading("#2", text="EQUIPO", anchor=tk.W)
        self.tabla_listEquipos.heading("#3", text="UBICACIÓN", anchor=tk.W)
        self.tabla_listEquipos.heading("#4", text="ESTADO", anchor=tk.W)
        self.tabla_listEquipos.heading("#5", text="AREA DE TRABAJO", anchor=tk.W)


        # edit column
        self.tabla_listEquipos.column("#0", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#1", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#2", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#3", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#4", stretch=tk.NO, minwidth="25", width="150" )
        self.tabla_listEquipos.column("#5", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        # for item in self.list_tabla:
        #     self.tabla_listEquipos.insert("", 0, text=item[0], values=(item[1], item[2]))

        # botones finales

        # Buscar
        boton_buscar = tk.Button(self.framePrincipal, text="Buscar")
        boton_buscar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        boton_buscar.grid(row=4, column=0, padx=10, pady=10)

        # Crear
        boton_crear = tk.Button(self.framePrincipal, text="Registrar", command=self.crearEquipos)
        boton_crear.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        boton_crear.grid(row=4, column=3, padx=10, pady=10)

     # *la que destrulle y crea el para registrar equipos
    def crearEquipos(self):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        self.frameRegisterEquipos()

    def frameRegisterEquipos(self):
        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Registrar Nuevo Equipo")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # LABELS
        label_serial = tk.Label(self.framePrincipal, text="Serial:")
        label_serial.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_serial.grid(row=1, column=0, padx=10, pady=10)

        label_tipo_equipo = tk.Label(self.framePrincipal, text="Tipo de Equipo:")
        label_tipo_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_tipo_equipo.grid(row=2, column=0, padx=10, pady=10)

        label_ubicacion = tk.Label(self.framePrincipal, text="Ubicacion:")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=3, column=0, padx=10, pady=10)

        label_estado = tk.Label(self.framePrincipal, text="Estado:")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=4, column=0, padx=10, pady=10)

        label_area_trabajo = tk.Label(self.framePrincipal, text="Area de Trabajo:")
        label_area_trabajo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area_trabajo.grid(row=5, column=0, padx=10, pady=10)

        # SELECTS
        self.mi_serial = tk.StringVar()
        entry_serial = tk.Entry(self.framePrincipal, textvariable=self.mi_serial)
        entry_serial.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        entry_serial.grid(row=1, column=1, pady=10, padx=10, columnspan=2)

        select_tipo_equipo = ttk.Combobox(self.framePrincipal, state="readonly")
        select_tipo_equipo.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        select_ubicacion = ttk.Combobox(self.framePrincipal, state="readonly")
        select_ubicacion.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

        select_estado = ttk.Combobox(self.framePrincipal, state="readonly")
        select_estado.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        select_area_trabajo = ttk.Combobox(self.framePrincipal, state="readonly")
        select_area_trabajo.grid(row=5, column=1, padx=10, pady=10, columnspan=2)