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


class PageCampos_tablas:

    def __init__(self, root):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_campos_tabla = None
        self.crearCuerpo()
        self.controles()
        self.tabla_lista()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def controles(self):
        # Titulo
        self.tituloPage = tk.Label(self.framePrincipal, text="Nombre de los campos")
        self.tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        self.tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Labels
        # Nombre
        self.label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        self.label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_nombre.grid(row=1, column=0, padx=10, pady=10)

        # Caracteres
        self.label_caracteres = tk.Label(self.framePrincipal, text="Caracteres:")
        self.label_caracteres.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_caracteres.grid(row=2, column=0, padx=10, pady=10)

        # Descripción
        self.label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        self.label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_descripcion.grid(row=3, column=0, padx=10, pady=10)

        # Campos de entrada
        self.mi_nombre = tk.StringVar()
        self.caracteres = tk.IntVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, pady=10, columnspan=2)

        self.entry_caracteres = tk.Entry(self.framePrincipal, textvariable=self.caracteres)
        self.entry_caracteres.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_caracteres.grid(row=2, column=1, pady=10, columnspan=2)

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.config(width=TAMAÑO_ENTRYS, height=10, font=FONT_LABEL)
        self.entry_descripcion.grid(row=3, column=1, pady=10, columnspan=2)

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

    def tabla_lista(self):

        # la lista de pelicular
        self.lista_campos = Campos_Tabla.list()
        self.lista_campos.reverse()

        self.tabla = ttk.Treeview(
            self.framePrincipal,
            columns=("Nombre", "Caracteres", "Descripcion"),
            height=20,
        )
        self.tabla.grid(row=5, column=0, columnspan=4, sticky="NSEW", padx=10)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla.yview
        )
        scroll.grid(row=5, column=3, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.heading("#0", text="ID")
        self.tabla.heading("#1", text="NOMBRE")
        self.tabla.heading("#2", text="CARACTERES")
        self.tabla.heading("#3", text="DESCRIPCIÓN")

        # iterar la lista d epeliculas
        for item in self.lista_campos:
            self.tabla.insert("", 0, text=item[0], values=(item[1], item[2], item[3]))

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

    def habilitar_campos(self):
        self.entry_nombre.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.entry_caracteres.config(state="normal")
        self.caracteres.set(0)

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def guardar_campos(self):
        try:
            tipo_equipo = {
                "nombre": self.mi_nombre.get(),
                "caracteres": self.caracteres.get(),
                "descripcion": self.entry_descripcion.get(1.0, tk.END),
            }

            if self.id_campos_tabla == None:
                Campos_Tabla.create(
                    nombre=tipo_equipo["nombre"],
                    descripcion=tipo_equipo["descripcion"],
                    caracteres=tipo_equipo["caracteres"],
                )
            else:
                Campos_Tabla.update(
                    id=self.id_campos_tabla,
                    nombre=tipo_equipo["nombre"],
                    descripcion=tipo_equipo["descripcion"],
                    caracteres=tipo_equipo["caracteres"],
                )

        except:
            messagebox.showwarning(
                TITULO_CAMPOS, f"Campo Caracteres. Solo se permiten numeros"
            )
            return None
        finally:
            self.desabilitar_campos()
            self.tabla_lista()

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
            descripcion_tipo_equipo = self.tabla.item(self.tabla.selection())["values"][
                1
            ]

            self.habilitar_campos()

            self.entry_nombre.insert(0, nombre_tipo_equipo)
            self.entry_descripcion.insert(1.0, descripcion_tipo_equipo)

        except:
            titulo = "Edicion de datos"
            message = "No ha seleccionado ningun registro"
            messagebox.showerror(titulo, message)

    def eliminar_datos(self):
        try:
            self.id_campos_tabla = self.tabla.item(self.tabla.selection())["text"]
            Campos_Tabla.delete(self.id_campos_tabla)
            self.tabla_lista()
            self.desabilitar_campos()
        except:
            titulo = "Eliminar de Registro"
            message = "No ha seleccionado ningun registro"
            messagebox.showerror(titulo, message)
