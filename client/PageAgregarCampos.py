import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_LABEL,FONT_LABEL_TITULO, COLOR_BASE, COLOR_AZUL, COLOR_ROJO, COLOR_VERDE, ACTIVE_VERDE, ACTIVE_AZUL, FONT_LABEL_ELEMENT_LIST
from models.tablas import Tablas
from models.campos_tablas import Campos_Tabla
from models.tablas_has_campos import Tablas_has_Campos
from util.util_img import leer_imagen
from util.list_values import list_values

class PageAgregarCampos():

    def __init__(self, root):
        self.root = root
        self.framePrincipal=tk.Frame(self.root, bg=COLOR_BASE)
        self.id_tabla=None
        self.crearCuerpo()
        self.controles()
        self.desabilitar_campos()
        self.frameCampos()

    def crearCuerpo(self):
        self.framePrincipal.pack(side=tk.RIGHT, fill='both', expand=True, ipadx=10)
        self.framePrincipal.columnconfigure(3, weight=1)

    def controles(self):
        self.tablas=Tablas.list()
        self.campos=Campos_Tabla.list()

        self.list_values_tablas=list_values(Tablas.list())   
        self.list_values_campos=list_values(Campos_Tabla.list())
        

        # Titulo
        tituloPage=tk.Label(self.framePrincipal, text="Agregar Campos a la Tabla")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # # Labels
        # Tablas
        self.label_tabla = tk.Label(self.framePrincipal, text="Tablas:")
        self.label_tabla.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_tabla.grid(row=1, column=0, padx=10, pady=10)

        # Campos
        self.label_campos = tk.Label(self.framePrincipal, text="Campos:")
        self.label_campos.config(font=FONT_LABEL, bg=COLOR_BASE)
        self.label_campos.grid(row=2, column=0, padx=10, pady=10)


        # # Select
        self.select_tabla=ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_values_tablas)
        self.select_tabla.grid(row=1, column=2, padx=5, pady=10)

        self.select_campos=ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_values_campos)
        self.select_campos.grid(row=2, column=2, padx=5, pady=10)

        # Button
        self.boton_buscar = tk.Button(self.framePrincipal, text="Buscar", command=self.buscar_campos)
        self.boton_buscar.config(width=10, font=FONT_LABEL, fg="white", bg=COLOR_VERDE, cursor="hand2", activebackground=ACTIVE_VERDE)
        self.boton_buscar.grid(row=1, column=3, padx=5, pady=10)
        
        # eliminar
        self.boton_agregar = tk.Button(self.framePrincipal, text="Agregar", command=self.agregar_campo)
        self.boton_agregar.config(width=10, font=FONT_LABEL, fg="white", bg=COLOR_AZUL, cursor="hand2", activebackground=ACTIVE_AZUL)
        self.boton_agregar.grid(row=2, column=3, padx=5, pady=10)
    

    def frameCampos(self):
        self.icon_papelera=leer_imagen("./img/trash.png", (30, 30))
        self.frame_campos=tk.Frame(self.framePrincipal, bg=COLOR_BASE, height=80)
        self.frame_campos.grid(row=3, column=0, padx=5, columnspan=4, pady=10, sticky="NSEW")
        self.frame_campos.columnconfigure(4, weight=1)

        # # # Titulo
        titulo=tk.Label(self.frame_campos, text="Lista de Campos")
        titulo.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # # # labels
        # Nombre
        label_campos = tk.Label(self.frame_campos, text="Nombre")
        label_campos.config(font=FONT_LABEL, bg=COLOR_BASE, width=50, anchor="w")
        label_campos.grid(row=1, column=1, padx=10, pady=10)

        # Caracteres
        label_caracteres = tk.Label(self.frame_campos, text="Caracteres")
        label_caracteres.config(font=FONT_LABEL, bg=COLOR_BASE, width=10, anchor="w")
        label_caracteres.grid(row=1, column=2, padx=10, pady=10)

        # Opciones
        label_Opciones = tk.Label(self.frame_campos, text="Opciones")
        label_Opciones.config(font=FONT_LABEL, bg=COLOR_BASE, width=20, anchor="w")
        label_Opciones.grid(row=1, column=3, padx=10, pady=10)
        

        if(self.id_tabla):
            lista_campos=Tablas_has_Campos.list(self.id_tabla)
            print(lista_campos)
        else:
            lista_campos=[]
        
        CONTADOR=1
        for campo in lista_campos:
            label = tk.Label(self.frame_campos, text=f"{campo[1]}")
            label.config(font=FONT_LABEL_ELEMENT_LIST, bg=COLOR_BASE, width=50, anchor="w")
            label.grid(row=1+CONTADOR, column=1, padx=10, pady=10)

            caracteres = tk.Label(self.frame_campos, text=f"{campo[2]}")
            caracteres.config(font=FONT_LABEL_ELEMENT_LIST, bg=COLOR_BASE, width=10, anchor="w")
            caracteres.grid(row=1+CONTADOR, column=2, padx=10, pady=10)

            buton_eliminar = tk.Button(self.frame_campos, image=self.icon_papelera, command=lambda:self.eliminar_campo(id_campo=int(campo[0])))
            buton_eliminar.config(width=40, bg=COLOR_ROJO, cursor="hand2", activebackground=COLOR_ROJO)
            buton_eliminar.grid(row=1+CONTADOR, column=3, padx=5, pady=10)

            CONTADOR=CONTADOR+1
            


    def buscar_campos(self):
        value=self.select_tabla.current()
        if(value<0):
            self.id_tabla=None
            titulo = "Tablas"
            message= "Seleccione alguna tabla"
            messagebox.showwarning(titulo, message)
            return
        
        self.habilitar_campos()
        self.id_tabla=int(self.tablas[value][0])
        self.frame_campos.destroy()
        self.frameCampos()
    
    def agregar_campo(self):
        value_tabla=self.select_tabla.current()
        value_campo=self.select_campos.current()

        if(value_campo<0):
            self.id_tabla=None
            titulo = "Campos"
            message= "Seleccione algun campo"
            messagebox.showwarning(titulo, message)
            return
        
        if(value_tabla<0):
            self.id_tabla=None
            titulo = "Tabla"
            message= "Seleccione alguna tabla"
            messagebox.showwarning(titulo, message)
            return

        Tablas_has_Campos.create(tablas=int(self.tablas[value_tabla][0]), campos=int(self.campos[value_campo][0]))
        self.frame_campos.destroy()
        self.frameCampos()


    def habilitar_campos(self):
        self.select_campos.config(state="readonly")
        self.boton_agregar.config(state="normal")
        self.select_campos.set("")

    # def guardar_campos(self):
        
    #     tipo_equipo = {
    #         "nombre" : self.mi_nombre.get(),
    #         "descripcion":self.entry_descripcion.get(1.0, tk.END)
    #     }
    #     if(self.id_estados==None):
    #         AreasTrabajo.create(nombre=tipo_equipo["nombre"], descripcion=tipo_equipo["descripcion"])
    #     else:
    #         AreasTrabajo.update(id=self.id_estados, nombre=tipo_equipo["nombre"], descripcion=tipo_equipo["descripcion"])
        
    #     self.desabilitar_campos()
    #     self.tabla_equipos()

    def desabilitar_campos(self):
        self.select_campos.set("")
        self.id_tabla=None

        
        self.select_campos.config(state="disabled")
        self.boton_agregar.config(state="disabled")
    
    def eliminar_campo(self, id_campo=0):
        pass
    # def editar_datos(self):
    #     try:
    #         self.id_estados=self.tabla.item(self.tabla.selection())["text"]
    #         nombre_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][0]
    #         descripcion_tipo_equipo=self.tabla.item(self.tabla.selection())["values"][1]

    #         self.habilitar_campos()

    #         self.entry_nombre.insert(0, nombre_tipo_equipo)
    #         self.entry_descripcion.insert(1.0, descripcion_tipo_equipo)

    #     except :
    #         titulo = "Edicion de datos"
    #         message= "No ha seleccionado ningun registro"
    #         messagebox.showerror(titulo, message)

    # def eliminar_datos(self):
        # try:
        #     self.id_estados=self.tabla.item(self.tabla.selection())["text"]
        #     AreasTrabajo.delete(self.id_estados)
        #     self.tabla_equipos()
        #     self.desabilitar_campos()
        # except :
        #     titulo = "Eliminar de Registro"
        #     message= "No ha seleccionado ningun registro"
        #     messagebox.showerror(titulo, message)