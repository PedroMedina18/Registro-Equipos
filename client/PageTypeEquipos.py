import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    FONT_LABEL,
    FONT_LABEL_TITULO,
    COLOR_BASE,
    COLOR_AZUL,
    COLOR_ROJO,
    COLOR_VERDE,
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    TAMAÑO_BOTON,
    ACTIVE_ROJO,
    TAMAÑO_ENTRYS,
)
from models.tipos_equipos import TipoEquipos
from util.util_error import controlError

class PageTypeEquipos:

    def __init__(self, root):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_tipo_equipo = None
        self.crearCuerpo()
        self.controles()
        self.tabla_lista()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        self.framePrincipal.columnconfigure(1, weight=1)
        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Tipos de Equipos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=7, columnspan=3)

        # Labels

        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=1, column=0, padx=10, pady=7, sticky="w")

        # Marca
        label_marca = tk.Label(self.framePrincipal, text="Marca:")
        label_marca.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_marca.grid(row=2, column=0, padx=10, pady=7, sticky="w")

        # Modelo
        label_modelo = tk.Label(self.framePrincipal, text="Modelo:")
        label_modelo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_modelo.grid(row=3, column=0, padx=10, pady=7, sticky="w")

        # Clase de Registro
        label_TypeRegistro = tk.Label(self.framePrincipal, text="Escoja el tipo de Registro:")
        label_TypeRegistro.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_TypeRegistro.grid(row=4, column=0, padx=10, pady=7, columnspan=4)

        # Descripción
        label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_descripcion.grid(row=6, column=0, padx=10, pady=7, sticky="w")

        # Campos de entrada
        self.mi_nombre = tk.StringVar()
        self.mi_marca = tk.StringVar()
        self.mi_modelo = tk.StringVar()
        self.componente_equipo = tk.IntVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, pady=7, columnspan=2, sticky="ew")

        self.entry_marca = tk.Entry(self.framePrincipal, textvariable=self.mi_marca)
        self.entry_marca.config(font=FONT_LABEL)
        self.entry_marca.grid(row=2, column=1, pady=7, columnspan=2, sticky="ew")

        self.entry_modelo = tk.Entry(self.framePrincipal, textvariable=self.mi_modelo)
        self.entry_modelo.config(font=FONT_LABEL)
        self.entry_modelo.grid(row=3, column=1, pady=7, columnspan=2, sticky="ew")

        self.Boolean_Equipos = tk.Radiobutton(
            self.framePrincipal, 
            variable=self.componente_equipo, 
            text="Equipo", 
            value=1
        )
        self.Boolean_Equipos.config(width=10, font=FONT_LABEL, bg=COLOR_BASE)
        self.Boolean_Equipos.grid(row=5, column=1, pady=2)

        self.Boolean_Componente = tk.Radiobutton(
            self.framePrincipal,
            variable=self.componente_equipo,
            text="Componente",
            value=0,
        )
        self.Boolean_Componente.config(width=10, font=FONT_LABEL, bg=COLOR_BASE)
        self.Boolean_Componente.grid(row=5, column=2, pady=2)

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.config( height=10, font=FONT_LABEL)
        self.entry_descripcion.grid(row=6, column=1, pady=10, columnspan=4, sticky="ew")

        scroll = tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.grid(row=6, column=3, sticky="nse", pady=10)
        self.entry_descripcion.config(yscrollcommand=scroll.set)

        # Botones

        self.boton_nuevo = tk.Button(
            self.framePrincipal, text="Nuevo", command=self.habilitar_campos
        )
        self.boton_nuevo.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        self.boton_nuevo.grid(row=7, column=0, padx=8, pady=7)

        self.boton_guardar = tk.Button(
            self.framePrincipal, text="Guardar", command=self.guardar_campos
        )
        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_guardar.grid(row=7, column=1, padx=8, pady=7)

        self.boton_cancelar = tk.Button(
            self.framePrincipal, text="Cancelar", command=self.desabilitar_campos
        )
        self.boton_cancelar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_cancelar.grid(row=7, column=2, padx=8, pady=7)

    def tabla_lista(self):
        pass
        # la lista de tipos de equipo
        self.lista_equipos = TipoEquipos.list()
        self.lista_equipos.reverse()
        # la tabla de los datos

        self.tabla = ttk.Treeview(
            self.framePrincipal,
            columns=("ID", "Nombre", "Marca", "Modelo", "Tipo", "Descripcion"),
            height=16,
            show='headings'
        )
        self.tabla.grid(row=8, column=0, columnspan=4, sticky="NSEW", padx=10)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla.yview
        )
        scroll.grid(row=8, column=3, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading("ID", text="ID", anchor=tk.W)
        self.tabla.heading("Nombre", text="NOMBRE", anchor=tk.W)
        self.tabla.heading("Marca", text="MARCA", anchor=tk.W)
        self.tabla.heading("Modelo", text="MODELO", anchor=tk.W)
        self.tabla.heading("Tipo", text="TIPO", anchor=tk.W)
        self.tabla.heading("Descripcion", text="DESCRIPCIÓN", anchor=tk.W)

        self.tabla.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla.column("Nombre", stretch=tk.NO, minwidth="25", width="150")
        self.tabla.column("Marca", stretch=tk.NO, minwidth="25", width="150")
        self.tabla.column("Modelo", stretch=tk.NO, minwidth="25", width="150")
        self.tabla.column("Tipo", stretch=tk.NO, minwidth="25", width="150")
        self.tabla.column("Descripcion", stretch=tk.YES, minwidth="25", width="150")

        # iterar la lista de tipos de equipo

        for index, item in enumerate(self.lista_equipos, start=1):

            if item[4]:
                tipo = "Equipo"
            else:
                tipo = "Componente"
            id_registro=item[0]
            tupla=(index, item[1], item[2], item[3], tipo, item[5])
            self.tabla.insert(
                "", tk.END, text=id_registro, values=tupla
            )

        # botones finales

        # editar
        self.boton_editar = tk.Button(self.framePrincipal, text="Editar")
        self.boton_editar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
            command=self.editar_datos,
        )
        self.boton_editar.grid(row=9, column=0, padx=10, pady=7)

        # eliminar
        self.boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar")
        self.boton_eliminar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
            command=self.eliminar_datos,
        )
        self.boton_eliminar.grid(row=9, column=1, padx=10, pady=7)

    def habilitar_campos(self):
        self.entry_nombre.config(state="normal")
        self.entry_marca.config(state="normal")
        self.entry_modelo.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.Boolean_Componente.config(state="normal")
        self.Boolean_Equipos.config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def guardar_campos(self):

        tipo_equipo = {
            "nombre": self.mi_nombre.get(),
            "marca": self.mi_marca.get(),
            "modelo": self.mi_modelo.get(),
            "equipo_componente": self.componente_equipo.get(),
            "descripcion": self.entry_descripcion.get(1.0, tk.END),
        }
        if self.id_tipo_equipo == None:
            valor = messagebox.askquestion(
                "Registro Nuevo", "Desea ingresar nuevo registro"
            )
            if valor == "yes":
                TipoEquipos.create(
                    nombre=tipo_equipo["nombre"],
                    marca=tipo_equipo["marca"],
                    modelo=tipo_equipo["modelo"],
                    descripcion=tipo_equipo["descripcion"],
                    equipo_componente=tipo_equipo["equipo_componente"],
                )
        else:
            valor = messagebox.askquestion(
                    "Editar Registro", "Desea editar este registro"
            )
            if valor == "yes":
                TipoEquipos.update(
                    id=self.id_tipo_equipo,
                    nombre=tipo_equipo["nombre"],
                    marca=tipo_equipo["marca"],
                    modelo=tipo_equipo["modelo"],
                    descripcion=tipo_equipo["descripcion"],
                    equipo_componente=tipo_equipo["equipo_componente"],
                )

        self.desabilitar_campos()
        self.tabla_lista()

    def desabilitar_campos(self):
        self.mi_nombre.set("")
        self.mi_marca.set("")
        self.mi_modelo.set("")
        self.componente_equipo.set(None)
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_tipo_equipo = None

        self.entry_nombre.config(state="disabled")
        self.entry_marca.config(state="disabled")
        self.entry_modelo.config(state="disabled")
        self.entry_descripcion.config(state="disabled")
        self.Boolean_Componente.config(state="disabled")
        self.Boolean_Equipos.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def editar_datos(self):
        try:
            self.desabilitar_campos()
            self.id_tipo_equipo = self.tabla.item(self.tabla.selection())["text"]
            nombre_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][1]
            marca_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][2]
            modelo_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][3]
            tipo_equipo = self.tabla.item(self.tabla.selection())["values"][4]
            descripcion_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][5]

            if tipo_equipo == "Equipo":
                tipo_equipo = 1
            elif tipo_equipo == "Componente":
                tipo_equipo = 0

            self.habilitar_campos()

            self.entry_nombre.insert(0, nombre_tipo_equipo)
            self.entry_marca.insert(0, marca_tipo_equipo)
            self.entry_modelo.insert(0, modelo_tipo_equipo)
            self.componente_equipo.set(int(tipo_equipo))
            self.entry_descripcion.insert(1.0, descripcion_tipo_equipo)

        except Exception as error:
            controlError(
                error,
                titleSelection="Edicion de Registro"
            )

    def eliminar_datos(self):
        try:
            
            self.id_tipo_equipo = self.tabla.item(self.tabla.selection())["text"]
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el registro seleccionado"
            )
            if valor == "yes":
                TipoEquipos.delete(self.id_tipo_equipo)
                self.tabla_lista()
                self.desabilitar_campos()
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )
