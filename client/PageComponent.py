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
    ACTIVE_ROJO,
    TAMAÑO_BOTON,
    TAMAÑO_ENTRYS,
    COLOR_ROJO,
    LETRA_OSCURA,
    TAMAÑO_MEDIUN_ENTRYS
    
)
from models.equipos import Equipos
from models.tipos_equipos import TipoEquipos
from models.caracteristicas import Caracteristicas
from util.util_img import leer_imagen
from util.list_values import list_values, verificacion_campos, determinar_campo

class   PageComponent:
    def __init__(self, root):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_componente = None
        self.crearCuerpo()
        self.controles()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        self.icon_papelera = leer_imagen("./img/trash.png", (30, 30))
        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Componentes")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=1, column=0, padx=10, pady=10)

        # Componente
        label_componente = tk.Label(self.framePrincipal, text="Componente:")
        label_componente.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_componente.grid(row=2, column=0, padx=10, pady=10)

        # usados
        label_usados = tk.Label(self.framePrincipal, text="Usados:")
        label_usados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_usados.grid(row=4, column=0, padx=10, pady=10)
        
        # almacen
        label_almacen = tk.Label(self.framePrincipal, text="Almacen:")
        label_almacen.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_almacen.grid(row=5, column=0, padx=10, pady=10)

        # dañados
        label_dañados = tk.Label(self.framePrincipal, text="Dañados:")
        label_dañados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_dañados.grid(row=6, column=0, padx=10, pady=10)

        # Caracteristicas
        label_caracteristicas = tk.Label(self.framePrincipal, text="Caracteristicas")
        label_caracteristicas.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_caracteristicas.grid(row=7, column=0, padx=10, pady=10)

        # Frame

        self.frameData = tk.Frame(self.framePrincipal, height=20, bg=COLOR_BASE)
        self.frameData.grid(row=3, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")
        self.dataComponente()

        self.frameCaracteristicas = tk.Frame(self.framePrincipal, bg=COLOR_BASE, height=30)
        self.frameCaracteristicas.grid(row=8, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")
        self.caracteristicas=[]
        self.contador_caracteristicas=0

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

        self.list_caracteristicas = Caracteristicas.list()
        self.list_values_caracteristicas=list_values(self.list_caracteristicas)
        self.select_caracteristicas = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=self.list_values_caracteristicas
        )
        self.select_caracteristicas.grid(row=7, column=1, padx=10, pady=7)
        boton_agregar = tk.Button(self.framePrincipal, text="Agregar", command=self.agregarCaracteristica)
        boton_agregar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL)
        boton_agregar.grid(row=7, column=2, padx=10, pady=10)

        # Botones
        self.boton_nuevo = tk.Button(
            self.framePrincipal, text="Nuevo"
        )
        self.boton_nuevo.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        self.boton_nuevo.grid(row=9, column=0, padx=8, pady=10)

        self.boton_guardar = tk.Button(
            self.framePrincipal, text="Guardar"
        )
        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_guardar.grid(row=9, column=1, padx=8, pady=10)

        self.boton_cancelar = tk.Button(
            self.framePrincipal, text="Cancelar"
        )
        self.boton_cancelar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_cancelar.grid(row=9, column=2, padx=8, pady=10)


    def dataComponente(self, data=None):
        label_nombre = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Nombre:")
        label_marca = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Marca:")
        label_modelo = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Modelo:")
        label_descripcion = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Descripción:")

        self.label_value_nombre = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_marca = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_modelo = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_descripcion = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="", justify="left", wraplength=3*200)
        
        label_nombre.grid(row=0, column=0, padx=60, pady=10, sticky="w")
        label_marca.grid(row=0, column=1, padx=40, pady=10, sticky="w")
        label_modelo.grid(row=0, column=2, padx=50, pady=10, sticky="w")
        label_descripcion.grid(row=2, column=0, padx=60, pady=10, sticky="w")

        self.label_value_nombre.grid(row=1, column=0, padx=60, sticky="w")
        self.label_value_marca.grid(row=1, column=1, padx=40, sticky="w")
        self.label_value_modelo.grid(row=1, column=2, padx=50, sticky="w")
        self.label_value_descripcion.grid(row=3, column=0, padx=60, sticky="w", columnspan=3)

    def selectComponent(self, event):
        valores=self.list_componentes[self.select_componente.current()]
        self.label_value_nombre.config(text=f"{valores[1]}")
        self.label_value_marca.config(text=f"{valores[2]}")
        self.label_value_modelo.config(text=f"{valores[3]}")
        self.label_value_descripcion.config(text=f"{valores[5]}")

    def agregarCaracteristica(self):
        
        seleccionado=self.select_caracteristicas.current()
        caracteristica_seleccionada=determinar_campo(self.list_caracteristicas, self.list_values_caracteristicas[seleccionado])
        
        frame=tk.Frame(self.frameCaracteristicas, bg="red")
        frame.pack(side=tk.TOP, fill=tk.BOTH, ipady=10, ipadx=10)
        mi_caracteristica = tk.StringVar()
        caracteristica=[
            caracteristica_seleccionada[0],
            caracteristica_seleccionada[1],
            caracteristica_seleccionada[2],
            mi_caracteristica,
            frame
        ]


        label = tk.Label(frame, text=f"{caracteristica_seleccionada[1]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
        label.pack(side=tk.LEFT, padx=10)

        buton_eliminar = tk.Button(frame, image=self.icon_papelera,  bg=COLOR_ROJO, width=40, pady=10, cursor="hand2", activebackground=COLOR_ROJO, command=lambda:self.eliminarCaracteristica(caracteristica))
        buton_eliminar.pack(side=tk.RIGHT, padx=10)

        entry_nombre = tk.Entry(frame, textvariable=mi_caracteristica, width=TAMAÑO_MEDIUN_ENTRYS, font=FONT_LABEL)
        entry_nombre.pack(side=tk.RIGHT, padx=10)
        
        self.caracteristicas.append(caracteristica)

        new_list=verificacion_campos([self.list_caracteristicas, 0], [self.caracteristicas, 0])
        self.select_caracteristicas.config(values=new_list)
    
    def eliminarCaracteristica(self, caracteristica):
        caracteristica[4].destroy()
        for index, campo in enumerate(self.select_caracteristicas):
            if campo[0] == caracteristica[0]:
                self.select_caracteristicas.pop(index)
            



    
    
