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
        self.controles()
        self.tabla_lista()()
        self.desabilitar_campos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill='both', expand=True, ipadx=10)

    def controles(self):
        # Titulo
        self.tituloPage=tk.Label(self.framePrincipal, text="Tipos de Equipos")
        self.tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        self.tituloPage.grid(row=0, column=0, padx=10, pady=6, columnspan=4)

        # Labels

        # Nombre
        self.label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        self.label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_nombre.grid(row=1, column=0, padx=10, pady=6)

        # Marca
        self.label_marca = tk.Label(self.framePrincipal, text="Marca:")
        self.label_marca.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_marca.grid(row=2, column=0, padx=10, pady=6)

        # Modelo
        self.label_modelo = tk.Label(self.framePrincipal, text="Modelo:")
        self.label_modelo.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_modelo.grid(row=3, column=0, padx=10, pady=6)

        # Clase de Registro
        self.label_TypeRegistro = tk.Label(self.framePrincipal, text="Escoja el tipo de Registro:")
        self.label_TypeRegistro.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_TypeRegistro.grid(row=4, column=0, padx=10, pady=6, columnspan=4)

        # Descripción
        self.label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
        self.label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_descripcion.grid(row=6, column=0, padx=10, pady=6)
    

        # Campos de entrada
        self.mi_nombre=tk.StringVar()
        self.mi_marca=tk.StringVar()
        self.mi_modelo=tk.StringVar()
        self.componente_equipo=tk.IntVar()


        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=80, font=FONT_LABEL)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=6, columnspan=2)

        self.entry_marca = tk.Entry(self.framePrincipal, textvariable=self.mi_marca)
        self.entry_marca.config(width=80, font=FONT_LABEL)
        self.entry_marca.grid(row=2, column=1, padx=10, pady=6, columnspan=2)

        self.entry_modelo = tk.Entry(self.framePrincipal, textvariable=self.mi_modelo)
        self.entry_modelo.config(width=80, font=FONT_LABEL)
        self.entry_modelo.grid(row=3, column=1, padx=10, pady=6, columnspan=2)

        self.Boolean_Equipos = tk.Radiobutton(self.framePrincipal, variable=self.componente_equipo, text="Equipo", value=1)
        self.Boolean_Equipos.config(width=10, font=FONT_LABEL, bg=COLOR_BASE)
        self.Boolean_Equipos.grid(row=5, column=1, padx=10, pady=2)

        self.Boolean_Componente = tk.Radiobutton(self.framePrincipal, variable=self.componente_equipo, text="Componente", value=0)
        self.Boolean_Componente.config(width=10, font=FONT_LABEL, bg=COLOR_BASE)
        self.Boolean_Componente.grid(row=5, column=2, padx=10, pady=2)


        self.entry_descripcion = tk.Text(self.framePrincipal)
        self.entry_descripcion.grid(row=6, column=1, padx=10, pady=6, columnspan=2)

        scroll=tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
        scroll.config(width=10)
        scroll.grid(row=6, column=3, sticky="nsew")
        self.entry_descripcion.config(width=80, height=8, font=FONT_LABEL, yscrollcommand=scroll.set)

        # Botones

        self.boton_nuevo = tk.Button(self. framePrincipal, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_VERDE, cursor="hand2", activebackground=ACTIVE_VERDE)
        self.boton_nuevo.grid(row=7, column=0, padx=8, pady=6)

        self.boton_guardar = tk.Button(self. framePrincipal, text="Guardar", command=self.guardar_campos)
        self.boton_guardar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground=ACTIVE_AZUL)
        self.boton_guardar.grid(row=7, column=1, padx=8, pady=6)

        self.boton_cancelar = tk.Button(self. framePrincipal, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_ROJO, cursor="hand2", activebackground=ACTIVE_ROJO)
        self.boton_cancelar.grid(row=7, column=2, padx=8, pady=6)

    def tabla_lista(self):

        # la lista de pelicular
        self.lista_equipos=TipoEquipos.list()
        self.lista_equipos.reverse()
        # la tabla de los datos

        self.tabla = ttk.Treeview(self.framePrincipal, columns=("Nombre", "Marca", "Modelo", "Tipo","Descripcion"), height=18)
        self.tabla.grid(row=8, column=0, columnspan=4, sticky="NSEW")

        # Scroll bar
        scroll=ttk.Scrollbar(self.framePrincipal, orient="vertical", command=self.tabla.yview)
        scroll.grid(row=8, column=3, sticky="nsew")
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.column("#0", width=20)
        self.tabla.heading("#0", text="ID")
        self.tabla.column("#1", width=30)
        self.tabla.heading("#1", text="NOMBRE")
        self.tabla.column("#2", width=30)
        self.tabla.heading("#2", text="MARCA")
        self.tabla.column("#3", width=30)
        self.tabla.heading("#3", text="MODELO")
        self.tabla.column("#4", width=20)
        self.tabla.heading("#4", text="TIPO")
        self.tabla.column("#5", width=50)
        self.tabla.heading("#5", text="DESCRIPCIÓN")

        # iterar la lista d epeliculas

        for item in self.lista_equipos:

            if(item[4]):
                tipo="Equipo"
            else:
                tipo="Componente"

            self.tabla.insert("", 0, text=item[0], 
            values=(item[1], item[2], item[3], tipo, item[5]))

        # botones finales

        # editar
        self.boton_editar = tk.Button(self.framePrincipal, text="Editar")
        self.boton_editar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground=ACTIVE_AZUL, command=self.editar_datos)
        self.boton_editar.grid(row=9, column=0, padx=10, pady=6)
        
        # eliminar
        self.boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar")
        self.boton_eliminar.config(width=20, font=FONT_LABEL, fg="white", bg=COLOR_ROJO, cursor="hand2", activebackground=ACTIVE_ROJO, command=self.eliminar_datos)
        self.boton_eliminar.grid(row=9, column=1, padx=10, pady=6)

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
            "nombre" : self.mi_nombre.get(),
            "marca" : self.mi_marca.get(),
            "modelo" : self.mi_modelo.get(),
            "equipo_componente":self.componente_equipo.get(),
            "descripcion":self.entry_descripcion.get(1.0, tk.END)
        }
        if(self.id_tipo_equipo==None):
            TipoEquipos.create(nombre=tipo_equipo["nombre"], marca=tipo_equipo["marca"], modelo=tipo_equipo["modelo"], descripcion=tipo_equipo["descripcion"], equipo_componente=tipo_equipo["equipo_componente"])
        else:
            TipoEquipos.update(id=self.id_tipo_equipo, nombre=tipo_equipo["nombre"], marca=tipo_equipo["marca"], modelo=tipo_equipo["modelo"], descripcion=tipo_equipo["descripcion"], equipo_componente=tipo_equipo["equipo_componente"])
        
        self.desabilitar_campos()
        self.tabla_lista()()

    def desabilitar_campos(self):
        self.mi_nombre.set("")
        self.mi_marca.set("")
        self.mi_modelo.set("")
        self.componente_equipo.set(None)
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_tipo_equipo=None

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
            self.id_tipo_equipo=self.tabla.item(self.tabla.selection())["text"]
            nombre_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][0]
            marca_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][1]
            modelo_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][2]
            tipo_equipo=self.tabla.item(self.tabla.selection())["values"][3]
            descripcion_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][4]

            if(tipo_equipo=="Equipo"):
                tipo_equipo=1
            elif(tipo_equipo=="Componente"):
                tipo_equipo=0


            self.habilitar_campos()

            self.entry_nombre.insert(0, nombre_tipo_equipo)
            self.entry_marca.insert(0, marca_tipo_equipo)
            self.entry_modelo.insert(0, modelo_tipo_equipo)
            self.componente_equipo.set(int(tipo_equipo))
            self.entry_descripcion.insert(1.0, descripcion_tipo_equipo)

        except Exception as es:
            print(es)
            titulo = "Edicion de datos"
            message= "No ha seleccionado ningun registro"
            messagebox.showerror(titulo, message)

    def eliminar_datos(self):

        try:
            self.id_tipo_equipo=self.tabla.item(self.tabla.selection())["text"]
            TipoEquipos.delete(self.id_tipo_equipo)
            self.tabla_lista()()
            self.desabilitar_campos()
        except :
            titulo = "Eliminar de Registro"
            message= "No ha seleccionado ningun registro"
            messagebox.showerror(titulo, message)