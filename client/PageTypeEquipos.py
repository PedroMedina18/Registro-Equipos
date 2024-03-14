import tkinter as tk
from config import FONT_LABEL, COLOR_BASE, COLOR_AZUL, COLOR_ROJO, COLOR_VERDE, ACTIVE_VERDE, ACTIVE_AZUL, ACTIVE_ROJO


class PageTypeEquipos():

    def __init__(self, root):
        self.root = root
        self.framePrincipal=tk.Frame(self.root, bg=COLOR_BASE)
        self.crearCuerpo()
        self.controles()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill='both', expand=True, ipadx=10)

    def controles(self):
        # Labels

        # Nombre
        self.label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        self.label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        # Marca
        self.label_marca = tk.Label(self.framePrincipal, text="Marca:")
        self.label_marca.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_marca.grid(row=1, column=0, padx=10, pady=10)

        # Descripción
        self.label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        self.label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_descripcion.grid(row=2, column=0, padx=10, pady=10)
    

        # Campos de entrada
        self.mi_nombre=tk.StringVar()
        self.mi_marca=tk.StringVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=80, font=FONT_LABEL)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.entry_marca = tk.Entry(self.framePrincipal, textvariable=self.mi_marca)
        self.entry_marca.config(width=80, font=FONT_LABEL)
        self.entry_marca.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        scroll=tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.config(width=10)
        scroll.grid(row=2, column=3, sticky="nsew")
        self.entry_descripcion.config(width=80, height=10, font=FONT_LABEL, yscrollcommand=scroll.set)

        # Botones

        self.boton_nuevo = tk.Button(self. framePrincipal, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_VERDE, cursor="hand2", activebackground=ACTIVE_VERDE)
        self.boton_nuevo.grid(row=3, column=0, padx=8, pady=10)

        self.boton_guardar = tk.Button(self. framePrincipal, text="Guardar", command=self.guardar_campos)
        self.boton_guardar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground=ACTIVE_AZUL)
        self.boton_guardar.grid(row=3, column=1, padx=8, pady=10)

        self.boton_cancelar = tk.Button(self. framePrincipal, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_ROJO, cursor="hand2", activebackground=ACTIVE_ROJO)
        self.boton_cancelar.grid(row=3, column=2, padx=8, pady=10)


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
            pass
        # self.mi_nombre.set("")
        # self.mi_genero.set("")
        # self.mi_duracion.set("")
        # self.id_pelicula=None

        # self.entry_nombre.config(state="disabled")
        # self.entry_genero.config(state="disabled")
        # self.entry_duracion.config(state="disabled")

        # self.boton_guardar.config(state="disabled")
        # self.boton_cancelar.config(state="disabled")