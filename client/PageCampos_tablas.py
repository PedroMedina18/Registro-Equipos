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
from models.campos_tablas import Campos_Tabla
from util.util_error import controlError

class PageCampos_tablas:

    def __init__(self, root):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_campos_tabla = None
        self.order="ASC"
        self.crearCuerpo()
        self.controles()
        self.tabla_lista()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        # Titulo
        self.framePrincipal.columnconfigure(1, weight=1)
        tituloPage = tk.Label(self.framePrincipal, text="Nombre de los campos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Labels
        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Caracteres
        label_caracteres = tk.Label(self.framePrincipal, text="Caracteres:")
        label_caracteres.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_caracteres.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Descripción
        label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_descripcion.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Campos de entrada
        self.mi_nombre = tk.StringVar()
        self.caracteres = tk.IntVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, pady=10, columnspan=2, sticky="ew")

        self.entry_caracteres = tk.Entry(self.framePrincipal, textvariable=self.caracteres)
        self.entry_caracteres.config(font=FONT_LABEL)
        self.entry_caracteres.grid(row=2, column=1, pady=10, columnspan=2, sticky="ew")

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.config(height=10, font=FONT_LABEL)
        self.entry_descripcion.grid(row=3, column=1, pady=10, columnspan=2, sticky="ew")

        scroll = tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.grid(row=3, column=3, sticky="nsew", pady=10)
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
        self.boton_nuevo.grid(row=4, column=0, padx=8, pady=10)

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
        self.boton_guardar.grid(row=4, column=1, padx=8, pady=10)

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
        self.boton_cancelar.grid(row=4, column=2, padx=8, pady=10)

    def tabla_lista(self, list=True):

        if list:
            self.lista_campos = Campos_Tabla.list()
            self.lista_campos.reverse()

        self.tabla = ttk.Treeview(
            self.framePrincipal,
            columns=("ID","Nombre", "Caracteres", "Descripcion"),
            height=20,
            show='headings'
        )
        self.tabla.grid(row=5, column=0, columnspan=4, sticky="NSEW", padx=10)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla.yview
        )
        scroll.grid(row=5, column=3, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading("ID", text="ID", anchor=tk.W)
        self.tabla.heading("Nombre", text="NOMBRE", anchor=tk.W)
        self.tabla.heading("Caracteres", text="CARACTERES", anchor=tk.W)
        self.tabla.heading("Descripcion", text="DESCRIPCIÓN", anchor=tk.W)

        self.tabla.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla.column("Nombre", stretch=tk.NO, minwidth="50", width="200")
        self.tabla.column("Caracteres", stretch=tk.NO, minwidth="25", width="80")
        self.tabla.column("Descripcion", stretch=tk.YES, minwidth="25")
        self.tabla.bind("<ButtonPress-1>", self.on_treeview_click)
        self.tabla.bind('<Double-Button-1>', self.handle_double_click)

        # iterar la lista d epeliculas
        for index, item in enumerate(self.lista_campos, start=1):
            id=item[0]
            tupla=(index, item[1], item[2], item[3])
            self.tabla.insert("", tk.END, text=id, values=tupla)

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
        self.boton_editar.grid(row=6, column=0, padx=10, pady=10)

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
        self.boton_eliminar.grid(row=6, column=1, padx=10, pady=10)

    def on_treeview_click(self, event):
        if self.order=="ASC":
            self.order="DESC"
        else:
            self.order="ASC"
        region = self.tabla.identify_region(event.x ,event.y)
        column = self.tabla.identify_column(event.x)
        item = self.tabla.identify_row(event.y)

        if item=="" and region=="heading":
            if column == "#1":
                self.lista_campos = Campos_Tabla.list(ordenador={"campo":"id", "order":self.order})
            elif column == "#2":
                self.lista_campos = Campos_Tabla.list(ordenador={"campo":"nombre", "order":self.order})
            elif column == "#3":
                self.lista_campos = Campos_Tabla.list(ordenador={"campo":"numero_caracteres", "order":self.order})
            elif column == "#4":
                self.lista_campos = Campos_Tabla.list(ordenador={"campo":"descripcion", "order":self.order})

            self.tabla_lista(False)

    def handle_double_click(self, event):
        region = self.tabla.identify_region(event.x ,event.y)
        if region == "cell":
            self.editar_datos()

    def habilitar_campos(self):
        self.entry_nombre.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.entry_caracteres.config(state="normal")
        self.caracteres.set(0)

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def guardar_campos(self):
        try:
            campo = {
                "nombre": self.mi_nombre.get(),
                "caracteres": self.caracteres.get(),
                "descripcion": self.entry_descripcion.get(1.0, tk.END),
            }

            if self.id_campos_tabla == None:
                valor = messagebox.askquestion(
                "Registro Nuevo", "Desea ingresar nuevo registro"
                )
                if valor == "yes":
                    respuesta = Campos_Tabla.create(
                        nombre=campo["nombre"],
                        descripcion=campo["descripcion"],
                        caracteres=campo["caracteres"],
                    )
                    if respuesta:
                        messagebox.showinfo("Exito", "Registro Completado")
                        self.tabla_lista()
            else:
                valor = messagebox.askquestion(
                    "Editar Registro", "Desea editar este registro"
                )
                if valor == "yes":
                    respuesta = Campos_Tabla.update(
                        id=self.id_campos_tabla,
                        nombre=campo["nombre"],
                        descripcion=campo["descripcion"],
                        caracteres=campo["caracteres"],
                    )
                    if respuesta:
                        messagebox.showinfo("Exito", "Registro Editado")
                        self.tabla_lista()
        except Exception as error:
            controlError(
                error,
                messageNumber="Campo Caracteres. Solo se permiten numeros"
            )
            return
        finally:
            self.desabilitar_campos()
            
    def desabilitar_campos(self):
        self.mi_nombre.set("")
        self.caracteres.set("")
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_campos_tabla = None

        self.entry_nombre.config(state="disabled")
        self.entry_descripcion.config(state="disabled")
        self.entry_caracteres.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def editar_datos(self):
        try:
            self.desabilitar_campos()
            self.id_campos_tabla = self.tabla.item(self.tabla.selection())["text"]
            nombre_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][0]
            descripcion_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][1]

            self.habilitar_campos()

            self.entry_nombre.insert(0, nombre_tipo_equipo)
            self.entry_descripcion.insert(1.0, descripcion_tipo_equipo)

        except Exception as error:
            controlError(
                error,
                titleSelection="Edición de Registro"
            )

    def eliminar_datos(self):
        try:
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el registro seleccionado"
            )
            if valor == "yes":
                self.id_campos_tabla = self.tabla.item(self.tabla.selection())["text"]

                if self.id_campos_tabla=="":
                    titulo="Eliminación de Registro"
                    message="No ha seleccionado ningun registro"
                    messagebox.showwarning(titulo, message)
                else:
                    respuesta = Campos_Tabla.delete(self.id_campos_tabla)
                    if respuesta:
                        messagebox.showinfo("Exito", "Registro Eliminado")
                self.tabla_lista()
                self.desabilitar_campos()
        except Exception as error:
             controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )
