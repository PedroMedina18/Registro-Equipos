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
from models.equipos import Equipos
from models.tipos_equipos import TipoEquipos
from util.list_values import list_values, verificacion_campos, determinar_campo

class PageEquipos:
    def __init__(self, root):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_componente = None
        self.crearCuerpo()
        self.controles()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Componentes")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=7, pady=10, columnspan=3)

        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=1, column=0, padx=7, pady=10)

        # Componente
        label_componente = tk.Label(self.framePrincipal, text="Componente:")
        label_componente.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_componente.grid(row=2, column=0, padx=7, pady=10)

        # usados
        label_usados = tk.Label(self.framePrincipal, text="Usados:")
        label_usados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_usados.grid(row=4, column=0, padx=7, pady=10)
        
        # almacen
        label_almacen = tk.Label(self.framePrincipal, text="Almacen:")
        label_almacen.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_almacen.grid(row=5, column=0, padx=7, pady=10)

        # dañados
        label_dañados = tk.Label(self.framePrincipal, text="Dañados:")
        label_dañados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_dañados.grid(row=6, column=0, padx=7, pady=10)

        # Caracteristicas
        label_caracteristicas = tk.Label(self.framePrincipal, text="Caracteristicas")
        label_caracteristicas.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_caracteristicas.grid(row=7, column=0, padx=7, pady=10)

        # Frame

        self.frameData = tk.Frame(self.framePrincipal, height=20, bg="red")
        self.frameData.grid(row=3, column=0, padx=7, pady=5, columnspan=3, sticky="NSEW")
        self.dataComponente()

        frameCaracteristicas = tk.Frame(self.framePrincipal)
        frameCaracteristicas.grid(row=8, column=0, padx=7, pady=5)


        # # CAMPOS
        self.mi_nombre = tk.StringVar()
        self.usados = tk.IntVar()
        self.almacen = tk.IntVar()
        self.dañados = tk.IntVar()
        

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=7, columnspan=2)

        self.list_componentes = TipoEquipos.list(equipo_componente=False)
        self.select_componente = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=list_values(self.list_componentes)
        )
        self.select_componente.grid(row=2, column=1, padx=10, pady=7, columnspan=2)
        self.select_componente.bind("<<ComboboxSelected>>", self.selectComponent)

        self.entry_usados = tk.Entry(self.framePrincipal, textvariable=self.usados)
        self.entry_usados.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_usados.grid(row=4, column=1, padx=10, pady=7, columnspan=2)

        self.entry_almacen = tk.Entry(self.framePrincipal, textvariable=self.almacen)
        self.entry_almacen.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_almacen.grid(row=5, column=1, padx=10, pady=7, columnspan=2)

        self.entry_dañados = tk.Entry(self.framePrincipal, textvariable=self.dañados)
        self.entry_dañados.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_dañados.grid(row=6, column=1, padx=10, pady=7, columnspan=2)

    def selectComponent(self, event):
        print(self.list_componentes)
        print(self.select_componente.current())

    def dataComponente(self, data=None):
        label_nombre = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Nombre:")
        label_marca = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Marca:")
        label_modelo = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Modelo:")
        label_descripcion = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Descripción")

        label_nombre.grid(row=0, column=0, padx=20, pady=5)
        label_marca.grid(row=0, column=1, padx=20, pady=5)
        label_modelo.grid(row=0, column=2, padx=20, pady=5)
        label_descripcion.grid(row=3, column=0, padx=5, pady=5)
        
        if data:
            pass
            # label_nombre = tk.Label(self.frameData, text="Nombre:")
            # label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
            # label_nombre.grid(row=6, column=0, padx=7, pady=10)
        else :
            pass
            # label_nombre = tk.Label(self.frameData, text="Nombre:")
            # label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
            # label_nombre.grid(row=6, column=0, padx=7, pady=10)
