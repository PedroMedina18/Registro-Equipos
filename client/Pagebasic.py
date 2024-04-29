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
from util.util_error import controlError

# Pagina basica de registros con solo el nombre, la descripcion
class PageBasic:

    def __init__(self, root, tituloPage, modelo):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.titulo = tituloPage
        self.model = modelo
        self.id_model = None
        self.crearCuerpo()
        self.controles()
        self.tabla_lista()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text=f"{self.titulo}")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Labels
        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Descripción
        label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_descripcion.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Campos de entrada
        self.mi_nombre = tk.StringVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, pady=10, columnspan=2)

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.config(width=TAMAÑO_ENTRYS, height=10, font=FONT_LABEL)
        self.entry_descripcion.grid(row=2, column=1, pady=10, columnspan=2)

        scroll = tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.grid(row=2, column=3, sticky="nsew", pady=10)
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
        self.boton_nuevo.grid(row=3, column=0, padx=8, pady=10)

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
        self.boton_guardar.grid(row=3, column=1, padx=8, pady=10)

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
        self.boton_cancelar.grid(row=3, column=2, padx=8, pady=10)

    def tabla_lista(self):
        # la lista de areas de trabao

        lista_areas_trabajo = self.model.list()
        lista_areas_trabajo.reverse()

        self.tabla = ttk.Treeview(
            self.framePrincipal, 
            columns=("ID", "Nombre", "Descripcion"), 
            height=20,
            show='headings'
        )
        self.tabla.grid(row=4, column=0, columnspan=4, sticky="NSEW", padx=10)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla.yview
        )
        scroll.grid(row=4, column=3, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="NOMBRE")
        self.tabla.heading("Descripcion", text="DESCRIPCIÓN")

        # iterar la lista de areas de trabao
        for index, item in enumerate(lista_areas_trabajo, start=1):
            id_registro=item[0]
            tupla=(index, item[1], item[2])
            self.tabla.insert("", tk.END, text=id_registro, values=tupla)

        # botones finales
        # editar
        boton_editar = tk.Button(self.framePrincipal, text="Editar")
        boton_editar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
            command=self.editar_datos,
        )
        boton_editar.grid(row=5, column=0, padx=10, pady=10)

        # eliminar
        boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar")
        boton_eliminar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
            command=self.eliminar_datos,
        )
        boton_eliminar.grid(row=5, column=1, padx=10, pady=10)

    def habilitar_campos(self):
        self.entry_nombre.config(state="normal")
        self.entry_descripcion.config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def guardar_campos(self):

        tipo_equipo = {
            "nombre": self.mi_nombre.get(),
            "descripcion": self.entry_descripcion.get(1.0, tk.END),
        }
        if self.id_model == None:
            valor = messagebox.askquestion(
                "Registro Nuevo", "Desea ingresar nuevo registro"
            )
            if valor == "yes":
                self.model.create(
                    nombre=tipo_equipo["nombre"], descripcion=tipo_equipo["descripcion"]
                )
        else:
            valor = messagebox.askquestion(
                "Editar Registro", "Desea editar este registro"
            )
            if valor == "yes":
                self.model.update(
                    id=self.id_model,
                    nombre=tipo_equipo["nombre"],
                    descripcion=tipo_equipo["descripcion"],
                )
        self.desabilitar_campos()
        self.tabla_lista()

    def desabilitar_campos(self):
        self.mi_nombre.set("")
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_model = None

        self.entry_nombre.config(state="disabled")
        self.entry_descripcion.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def editar_datos(self):
        try:
            self.desabilitar_campos()
            self.id_model = self.tabla.item(self.tabla.selection())["text"]
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
                self.id_model = self.tabla.item(self.tabla.selection())["text"]
                if self.id_model=="":
                    titulo="Eliminación de Registro"
                    message="No a seleccionado el registro que desea eliminar"
                    messagebox.showwarning(titulo, message)
                else:
                    self.model.delete(self.id_model)
                self.desabilitar_campos()
                self.tabla_lista()

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )
