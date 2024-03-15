import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_LABEL,FONT_LABEL_TITULO, COLOR_BASE, COLOR_AZUL, COLOR_ROJO, COLOR_VERDE, ACTIVE_VERDE, ACTIVE_AZUL, ACTIVE_ROJO
from models.tipos_equipos import TipoEquipos

class PageTypeEquipos():

    def __init__(self, root):
        self.root = root
        self.framePrincipal=tk.Frame(self.root, bg=COLOR_BASE)
        self.id_tipo_equipo=None
        self.crearCuerpo()
        self.tabla_equipos()
        self.controles()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill='both', expand=True, ipadx=10)

    def controles(self):
        # Titulo
        self.tituloPage=tk.Label(self.framePrincipal, text="Tipos de Equipos")
        self.tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        self.tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # Labels

        # Nombre
        self.label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        self.label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_nombre.grid(row=1, column=0, padx=10, pady=10)

        # Marca
        self.label_marca = tk.Label(self.framePrincipal, text="Marca:")
        self.label_marca.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_marca.grid(row=2, column=0, padx=10, pady=10)

        # Descripción
        self.label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        self.label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_descripcion.grid(row=3, column=0, padx=10, pady=10)
    

        # Campos de entrada
        self.mi_nombre=tk.StringVar()
        self.mi_marca=tk.StringVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=80, font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.entry_marca = tk.Entry(self.framePrincipal, textvariable=self.mi_marca)
        self.entry_marca.config(width=80, font=FONT_LABEL)
        self.entry_marca.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

        scroll=tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.config(width=10)
        scroll.grid(row=3, column=3, sticky="nsew")
        self.entry_descripcion.config(width=80, height=10, font=FONT_LABEL, yscrollcommand=scroll.set)

        # Botones

        self.boton_nuevo = tk.Button(self. framePrincipal, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_VERDE, cursor="hand2", activebackground=ACTIVE_VERDE)
        self.boton_nuevo.grid(row=4, column=0, padx=8, pady=10)

        self.boton_guardar = tk.Button(self. framePrincipal, text="Guardar", command=self.guardar_campos)
        self.boton_guardar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground=ACTIVE_AZUL)
        self.boton_guardar.grid(row=4, column=1, padx=8, pady=10)

        self.boton_cancelar = tk.Button(self. framePrincipal, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_ROJO, cursor="hand2", activebackground=ACTIVE_ROJO)
        self.boton_cancelar.grid(row=4, column=2, padx=8, pady=10)

    def tabla_equipos(self):

        # la lista de pelicular
        self.lista_equipos=[]
        self.lista_equipos.reverse()

        # la tabla de los datos
        # style = ttk.Style()
        # style.configure("tabla.TTreeview", background="black")

        self.tabla = ttk.Treeview(self.framePrincipal, columns=("Nombre", "Marca", "Descripcion"))
        # self.tabla.config(style="tabla.TTreeview")
        self.tabla.grid(row=5, column=0, columnspan=4, sticky="EW")

        # Scroll bar
        scroll=ttk.Scrollbar(self.framePrincipal, orient="vertical", command=self.tabla.yview)
        scroll.grid(row=5, column=4, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)


        self.tabla.heading("#0", text="ID")
        self.tabla.heading("#1", text="NOMBRE")
        self.tabla.heading("#2", text="MARCA")
        self.tabla.heading("#3", text="DESCRIPCIÓN")

        # iterar la lista d epeliculas

        for item in self.lista_equipos:
            self.tabla.insert("", 0, text=item[0], 
            values=(item[1], item[2], item[3]))

        # botones finales

        # editar
        self.boton_editar = tk.Button(self.framePrincipal, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground="#35BD6F")
        self.boton_editar.grid(row=6, column=0, padx=10, pady=10)
        
        # eliminar
        self.boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_ROJO, cursor="hand2", activebackground="#E15370")
        self.boton_eliminar.grid(row=6, column=1, padx=10, pady=10)


    def habilitar_campos(self):
            pass
        # self.entry_nombre.config(state="normal")
        # self.entry_genero.config(state="normal")
        # self.entry_duracion.config(state="normal")

        # self.boton_guardar.config(state="normal")
        # self.boton_cancelar.config(state="normal")

    def guardar_campos(self):
            pass
        # pelicula = Pelicula(
        #     self.mi_nombre.get(),
        #     self.mi_duracion.get(),
        #     self.mi_genero.get(),
        # )
        # if(self.id_pelicula==None):
        #     guardar(pelicula)
        # else:
        #     editar(pelicula, self.id_pelicula)
        
        # self.desabilitar_campos()
        # self.tabla_peliculas()

    def desabilitar_campos(self):
        self.mi_nombre.set("")
        self.mi_marca.set("")
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_tipo_equipo=None

        self.entry_nombre.config(state="disabled")
        self.entry_marca.config(state="disabled")
        self.entry_descripcion.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")