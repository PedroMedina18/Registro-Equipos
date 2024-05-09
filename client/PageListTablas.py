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
from models.tablas import Tablas
from models.tablas_has_campos import Tablas_has_Campos
from models.registros import Registros
from util.util_error import controlError

# la pagina en donde se encuentran todas las tablas
class PageListTablas:

    def __init__(self, root, cambio_cuerpo):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = cambio_cuerpo
        self.id_table = None
        self.numero_registro = 0
        self.crearCuerpo()
        self.lista_tablas()

    # *para crear el cuerpo principal
    def crearCuerpo(self):
        if self.framePrincipal:
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)
        else:
            self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)

    # *la primera lista en donde se ven todas las tablas
    def lista_tablas(self):
        self.framePrincipal.columnconfigure(0, weight=1)

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Lista de tablas")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10)

        self.list_tabla = Tablas.list(order=True)

        self.tabla_listTablas = ttk.Treeview(
            self.framePrincipal, columns=("ID", "Nombre", "Descripcion"), height=30, show='headings'
        )
        self.tabla_listTablas.grid(row=1, column=0, sticky="NSEW", padx=10, columnspan=2)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_listTablas.yview
        )
        scroll.grid(row=1, column=1, sticky="nsew")
        self.tabla_listTablas.configure(yscrollcommand=scroll.set)

        self.tabla_listTablas.heading("ID", text="ID", anchor=tk.W)
        self.tabla_listTablas.heading("Nombre", text="NOMBRE", anchor=tk.W)
        self.tabla_listTablas.heading("Descripcion", text="DESCRIPCIÓN", anchor=tk.W)


        # edit column
        self.tabla_listTablas.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla_listTablas.column("Nombre", stretch=tk.NO, minwidth="25", width="250")
        self.tabla_listTablas.column("Descripcion", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        for index, item in enumerate(self.list_tabla, start=1):
            id=item[0]
            tupla=(index, item[1], item[2])
            self.tabla_listTablas.insert("", tk.END, text=id, values=tupla)

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

    # *la que destrulle y crea el nuevo frame
    def buscarDataTabla(self):
        try:
            self.id_table = self.tabla_listTablas.item(self.tabla_listTablas.selection())["text"]
            name_tabla = self.tabla_listTablas.item(self.tabla_listTablas.selection())["values"][1]
            self.list_campos = Tablas_has_Campos.list(id_tabla=self.id_table)
            if len(self.list_campos) == 0:
                respuesta=messagebox.showwarning(f"Tabla {name_tabla}", "No hay ningun campo agregado a esta tabla")
                if respuesta=="ok":
                    return
                
            self.framePrincipal.destroy()
            self.framePrincipal = None
            self.crearCuerpo()
            self.cambio_cuerpo(self.framePrincipal)
            self.frameTableData(id_table=int(self.id_table), name_tabla=name_tabla)
        except Exception as error:
            controlError(
                error,
                titleSelection="Buscar Registro"
            )
    
    def frameTableData(self, id_table=0, name_tabla=""):
        self.list_campos = Tablas_has_Campos.list(id_tabla=id_table)
        self.framePrincipal.columnconfigure(1, weight=1)

        # # Button Regresar
        buttonRegresar = tk.Button(self.framePrincipal, text="Regresar")
        buttonRegresar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
            command=self.regresar,
        )
        buttonRegresar.grid(row=0, column=0, padx=10, pady=10)

        # # Titulo
        tituloPage = tk.Label(self.framePrincipal, text=f"{name_tabla}")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=1, column=0, padx=10, pady=5, columnspan=3)

        self.LIST_CAMPOS = []
        self.CONTADOR = 0
        for campos in self.list_campos:
            # # EL LABEL

            label_nombre = tk.Label(self.framePrincipal, text=f"{campos[1]}:")
            label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
            label_nombre.grid(row=2 + self.CONTADOR, column=0, padx=10, pady=10, sticky="w")

            object_campos={}

            if campos[2] >= 150:
                # # TEXTARE
                entry_descripcion = tk.Text(self.framePrincipal)
                entry_descripcion.grid(row=2 + self.CONTADOR, column=1, pady=10, columnspan=3, sticky="ew")

                scroll = tk.Scrollbar(self.framePrincipal, command=entry_descripcion.yview)
                scroll.grid(row=2 + self.CONTADOR, column=4, sticky="nsw", pady=10)
                entry_descripcion.config(
                    height=10,
                    font=FONT_LABEL,
                    yscrollcommand=scroll.set,
                )

                self.LIST_CAMPOS.append(
                    {
                        "type": "textarea",
                        "entrada": entry_descripcion,
                        "id": campos[0],
                        "caracteres": campos[2],
                        "nombre": campos[1],
                        "type_registro":None
                    }
                )
            else:
                # # ENTRY
                string = tk.StringVar()
                entry_nombre = tk.Entry(self.framePrincipal, textvariable=string)
                entry_nombre.config(font=FONT_LABEL)
                entry_nombre.grid(row=2 + self.CONTADOR, column=1, pady=10, columnspan=3, sticky="ew")

                self.LIST_CAMPOS.append(
                    {
                        "type": "input",
                        "entrada": entry_nombre,
                        "id": campos[0],
                        "caracteres": campos[2],
                        "nombre": campos[1],
                        "variable": string,
                        "type_registro":"create"
                    }
                )

            self.CONTADOR = self.CONTADOR + 1

        # Botones
        self.boton_nuevo = tk.Button(self.framePrincipal, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        self.boton_nuevo.grid(row=2 + self.CONTADOR, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self.framePrincipal, text="Guardar", command=self.guardar_campos)
        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_guardar.grid(row=2 + self.CONTADOR, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self.framePrincipal, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_cancelar.grid(row=2 + self.CONTADOR, column=2, padx=10, pady=10)

        self.desabilitar_campos()
        self.tabla_lista()

    def tabla_lista(self):
        self.framePrincipal.columnconfigure(3, weight=1)
        columns = ("id",)
        columns += tuple(element["nombre"] for element in self.LIST_CAMPOS)
        columns += ("fecha_creacion", "fecha_actualizacion")
        self.lista_registros = Registros.list(id_tabla=self.id_table, campos=columns)
        
        frameTable=tk.Frame(self.framePrincipal, height=350, bg=COLOR_BASE, width=200)
        frameTable.grid(row=3 + self.CONTADOR, column=0, columnspan=5, sticky="NSEW", padx=10)

        self.tabla_registros = ttk.Treeview(
            frameTable,
            columns=columns,
            show="headings",
        )
        self.tabla_registros.place(relwidth=1, height=350)

        # Scroll bar
        scrollVertical = ttk.Scrollbar(
            self.framePrincipal,
            orient="vertical", 
            command=self.tabla_registros.yview
        )
        scrollVertical.grid(row=3 + self.CONTADOR, column=4, sticky="NS")

        scrollHorizontal = ttk.Scrollbar(
            self.framePrincipal, 
            orient="horizontal",
            command=self.tabla_registros.xview
        )
        scrollHorizontal.grid(row=4 + self.CONTADOR, column=0, columnspan=4, sticky="EW", padx=10)

        self.tabla_registros.configure(
            selectmode="extended", 
            yscrollcommand=scrollVertical.set, 
            xscrollcommand=scrollHorizontal.set
        )

        # Para insertar todas las columnas de la tabla
        for object in columns:
            self.tabla_registros.heading(f"{object}", text=object.replace("_", " ").upper(), anchor=tk.W)
            if object=="id":
                self.tabla_registros.column(f"{object}", stretch=tk.NO, minwidth="25", width="50")
            if object=="fecha_creacion" or object=="fecha_actualizacion":
                self.tabla_registros.column(f"{object}", stretch=tk.NO, minwidth="50", width="180")
        
        # Para insertar los registros en al tabla
        for index, registros in enumerate(self.lista_registros):
            values = list(values for keys, values in registros.items())
            idRegistro = values[0]
            values[0] = index + 1
            values=tuple(values)
            self.tabla_registros.insert("", tk.END, text=idRegistro, values=values)

        # botones finales
        # editar
        self.boton_editar = tk.Button(self.framePrincipal, text="Editar", command=self.editar_datos)
        self.boton_editar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_editar.grid(row=5 + self.CONTADOR, column=0, padx=10, pady=10)

        # eliminar
        self.boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_eliminar.grid(row=5 + self.CONTADOR, column=1, padx=10, pady=10)

    def desabilitar_campos(self):

        for campos in self.LIST_CAMPOS:
            if campos["type"] == "input":
                campos["variable"].set("")
                campos["entrada"].config(state="disabled")

            if campos["type"] == "textarea":
                campos["entrada"].delete(1.0, tk.END)
                campos["entrada"].config(state="disabled")

        self.numero_registro = None
        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def guardar_campos(self):

        list_campos = []
        for element in self.LIST_CAMPOS:
            if element["type"] == "input":
                list_campos.append(
                    {
                        "id": element["id"],
                        "value": element["variable"].get(),
                        "caracteres": element["caracteres"],
                        "nombre": element["nombre"],
                        "type":element["type_registro"]
                    }
                )
            else:
                list_campos.append(
                    {
                        "id": element["id"],
                        "value": element["entrada"].get(1.0, tk.END),
                        "caracteres": element["caracteres"],
                        "nombre": element["nombre"],
                        "type":element["type_registro"]
                    }
                )
            element["type_registro"]="create"
        
        if self.numero_registro == None:
            valor = messagebox.askquestion(
                "Registro Nuevo", "Desea ingresar nuevo registro"
            )
            if valor == "yes":
                Registros.create(campos=list_campos)
        else:
            valor = messagebox.askquestion(
                "Editar Registro", "Desea editar este registro"
            )
            if valor == "yes":
                Registros.update(campos=list_campos, numero_registro=self.numero_registro)

        self.desabilitar_campos()
        self.tabla_lista()

    def habilitar_campos(self):
        for campos in self.LIST_CAMPOS:
            campos["entrada"].config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def regresar(self):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        self.lista_tablas()

    def eliminar_datos(self):
        try:
            self.numero_registro = self.tabla_registros.item(self.tabla_registros.selection())["text"]
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el registro seleccionado"
            )
            if valor == "yes":
                Registros.delete(self.numero_registro)
                self.tabla_lista()
                self.desabilitar_campos()
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )

    def editar_datos(self):
        try:
            self.desabilitar_campos()
            self.numero_registro = self.tabla_registros.item(self.tabla_registros.selection())["text"]
            
            dataSeleccionada = self.tabla_registros.item(self.tabla_registros.selection())
            self.habilitar_campos()

            for index, campo in enumerate(self.LIST_CAMPOS, start = 1):
                if not (dataSeleccionada["values"][index] == ""):
                    campo["type_registro"]="update"
                    
                if campo["caracteres"] >= 150:
                    campo["entrada"].insert(1.0, dataSeleccionada["values"][index])
                else:
                    campo["entrada"].insert(0, dataSeleccionada["values"][index])
        except Exception as error:
            controlError(
                error,
                titleSelection="Edicion de Registro"
            )