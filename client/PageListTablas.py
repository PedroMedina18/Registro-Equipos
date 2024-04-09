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


# la pagina en donde se encuentran todas las tablas
class PageListTablas:

    def __init__(self, root, *args):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = args[0]
        self.numero_registro = None
        self.id_table = None
        self.crearCuerpo()
        self.lista_tablas()

    # para crear el cuerpo principal
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

        self.list_tabla = Tablas.list()
        self.list_tabla.reverse()

        self.tabla = ttk.Treeview(
            self.framePrincipal, columns=("Nombre", "Descripcion"), height=30
        )
        self.tabla.grid(row=1, column=0, sticky="NSEW", padx=10, columnspan=2)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla.yview
        )
        scroll.grid(row=1, column=1, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading("#0", text="ID", anchor=tk.W)
        self.tabla.heading("#1", text="NOMBRE", anchor=tk.W)
        self.tabla.heading("#2", text="DESCRIPCIÓN", anchor=tk.W)


        # edit column
        self.tabla.column("#0", stretch=tk.NO, minwidth="25", width="150")
        self.tabla.column("#1", stretch=tk.NO, minwidth="25", width="250")
        self.tabla.column("#2", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        for item in self.list_tabla:
            self.tabla.insert("", 0, text=item[0], values=(item[1], item[2]))

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
            self.id_table = self.tabla.item(self.tabla.selection())["text"]
            name_tabla = self.tabla.item(self.tabla.selection())["values"][0]
            self.framePrincipal.destroy()
            self.framePrincipal = None
            self.crearCuerpo()
            self.cambio_cuerpo(self.framePrincipal)
            self.frameTableData(id_table=int(self.id_table), name_tabla=name_tabla)
        except Exception as error:
            print(error)
            titulo = "Buscar tabla"
            message = "No ha seleccionado ningun registro"
            messagebox.showerror(titulo, message)

    def frameTableData(self, id_table=0, name_tabla=""):
        list_campos = Tablas_has_Campos.list(id_tabla=id_table)

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
        for campos in list_campos:
            # EL LABEL

            label_nombre = tk.Label(self.framePrincipal, text=f"{campos[1]}:")
            label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
            label_nombre.grid(row=2 + self.CONTADOR, column=0, padx=10, pady=10)

            if campos[2] > 150:
                # TEXTARE
                entry_descripcion = tk.Text(self.framePrincipal)
                entry_descripcion.grid(
                    row=2 + self.CONTADOR, column=1, pady=10, columnspan=2
                )

                scroll = tk.Scrollbar(
                    self.framePrincipal, command=entry_descripcion.yview
                )
                scroll.grid(row=2 + self.CONTADOR, column=3, sticky="nsew")
                entry_descripcion.config(
                    width=TAMAÑO_ENTRYS,
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
                    }
                )
            else:
                # ENTRY
                string = tk.StringVar()
                entry_nombre = tk.Entry(self.framePrincipal, textvariable=string)
                entry_nombre.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
                entry_nombre.grid(
                    row=2 + self.CONTADOR, column=1, pady=10, columnspan=2
                )

                self.LIST_CAMPOS.append(
                    {
                        "type": "input",
                        "entrada": entry_nombre,
                        "variable": string,
                        "id": campos[0],
                        "caracteres": campos[2],
                        "nombre": campos[1],
                    }
                )

            self.CONTADOR = self.CONTADOR + 1

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
        self.boton_nuevo.grid(row=2 + self.CONTADOR, column=0, padx=8, pady=10)

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
        self.boton_guardar.grid(row=2 + self.CONTADOR, column=1, padx=8, pady=10)

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
        self.boton_cancelar.grid(row=2 + self.CONTADOR, column=2, padx=8, pady=10)

        self.desabilitar_campos()
        self.tabla_lista()

    def tabla_lista(self):
        pass
        columns = ("id",)
        columns += tuple(element["nombre"] for element in self.LIST_CAMPOS)
        columns += ("fecha_creacion", "fecha_actualizacion")

        frameTable=tk.Frame(self.framePrincipal, height=250, bg="red")
        frameTable.grid(row=3 + self.CONTADOR, column=0, columnspan=4, sticky="NSEW", padx=10)
        self.lista_registros = Registros.list(id_tabla=self.id_table, campos=columns)

        tabla = ttk.Treeview(
            frameTable,
            columns=columns,
            show="headings",
        )
        tabla.place(width=950, height=250)

        # Scroll bar
        scrollVertical = ttk.Scrollbar(
            self.framePrincipal,
            orient="vertical", 
            command=tabla.yview
        )
        scrollVertical.grid(row=3 + self.CONTADOR, column=3, sticky="NS")

        scrollHorizontal = ttk.Scrollbar(
            self.framePrincipal, 
            orient="horizontal",
            command=tabla.xview
        )
        scrollHorizontal.grid(row=4 + self.CONTADOR, column=0, columnspan=4, sticky="EW", padx=10)

        tabla.configure(
            selectmode="extended", 
            yscrollcommand=scrollVertical.set, 
            xscrollcommand=scrollHorizontal.set
        )

        # Para insertar todas las columnas de la tabla
        for object in columns:
            tabla.heading(f"{object}", text=object.replace("_", " ").upper())

        for index, registros in enumerate(self.lista_registros):
            values = tuple(values for keys, values in registros.items())
            tabla.insert("", tk.END, values=values)

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
        )
        self.boton_editar.grid(row=5 + self.CONTADOR, column=0, padx=10, pady=10)

        # eliminar
        self.boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar")
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

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def guardar_campos(self):

        list_campos = []
        for element in self.LIST_CAMPOS:
            if element["type"] == "input":
                list_campos.append(
                    {
                        "value": element["variable"].get(),
                        "caracteres": element["caracteres"],
                        "nombre": element["nombre"],
                        "id": element["id"],
                    }
                )
            else:
                list_campos.append(
                    {
                        "value": element["entrada"].get(1.0, tk.END),
                        "caracteres": element["caracteres"],
                        "nombre": element["nombre"],
                        "id": element["id"],
                    }
                )
        if self.numero_registro == None:
            Registros.create(campos=list_campos)
        else:
            Registros.update(campos=list_campos)

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
