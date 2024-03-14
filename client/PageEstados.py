import tkinter as tk

fontLabel=("Arial", 12, "bold")

class PageEstados():

    def __init__(self, root):
        self.root = root
        self.framePrincipal=tk.Frame(self.root, bg="red")
        self.crearCuerpo()
        self.controles()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles(self):
        # Labels

        # Nombre
        self.label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        self.label_nombre.config(font=fontLabel)
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        # Marca
        self.label_marca = tk.Label(self.framePrincipal, text="Marca:")
        self.label_marca.config(font=fontLabel)
        self.label_marca.grid(row=1, column=0, padx=10, pady=10)

        # Descripción
        self.label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        self.label_descripcion.config(font=fontLabel)
        self.label_descripcion.grid(row=2, column=0, padx=10, pady=10)
    

        # Campos de entrada

        self.mi_nombre=tk.StringVar()
        self.mi_duracion=tk.StringVar()
        self.mi_genero=tk.StringVar()

        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=50, font=("Arial", 12, "bold"))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.entry_marca = tk.Entry(self.framePrincipal, textvariable=self.mi_duracion)
        self.entry_marca.config(width=50, font=("Arial", 12, "bold"))
        self.entry_marca.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.entry_descripcion = tk.Entry(self.framePrincipal, textvariable=self.mi_genero)
        self.entry_descripcion.config(width=50, font=("Arial", 12, "bold"))
        self.entry_descripcion.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
