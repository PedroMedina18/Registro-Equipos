import tkinter as tk
from tkinter import ttk, messagebox
from util.comprobacionCampos import comprobacionString
from config import (
    FONT_LABEL,
    FONT_LABEL_TITULO,
    COLOR_BASE,
    COLOR_AZUL,
    COLOR_VERDE,
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    ACTIVE_ROJO,
    TAMAÑO_BOTON,
    TAMAÑO_ENTRYS,
    COLOR_ROJO,
    LETRA_OSCURA,
    TAMAÑO_MEDIUN_ENTRYS,
    TITULO_CAMPOS
)
from models.tipos_equipos import TipoEquipos
from models.caracteristicas import Caracteristicas
from models.componentes_has_caracteristicas import Componentes_has_Caracteristicas
from models.componentes import Componentes
from util.util_img import leer_imagen
from util.list_values import list_values, verificacion_campos, determinar_campo, determinar_indice
from util.util_error import controlError

class PageComponent:
    def __init__(self, root, cambio_cuerpo):
        self.root = root
        self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
        self.id_componente = None
        self.cambio_cuerpo = cambio_cuerpo
        self.data_component = None
        self.order = "ASC"
        self.crearCuerpo()
        self.listComponentes()

    def crearCuerpo(self):
        if self.framePrincipal:
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)
        else:
            self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=10)

    def listComponentes(self, lista=True):
        self.framePrincipal.columnconfigure(0, weight=1)
        self.data_component=None
        self.id_componente = None

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Lista de componentes")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        if lista:
            self.list_componentes = Componentes.list()
            self.list_componentes.reverse()

        self.tabla_listComponentes = ttk.Treeview(
            self.framePrincipal, columns=("ID","Nombre", "Almacen",  "Dañados", "Usados"), height=30, show='headings'
        )
        self.tabla_listComponentes.grid(row=1, column=0, sticky="NSEW", padx=10, columnspan=4)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_listComponentes.yview
        )
        scroll.grid(row=1, column=3, sticky="nsew")
        self.tabla_listComponentes.configure(yscrollcommand=scroll.set)

        self.tabla_listComponentes.heading("ID", text="ID", anchor=tk.W)
        self.tabla_listComponentes.heading("Nombre", text="NOMBRE", anchor=tk.W)
        self.tabla_listComponentes.heading("Almacen", text="ALMACEN", anchor=tk.W)
        self.tabla_listComponentes.heading("Dañados", text="DAÑADOS", anchor=tk.W)
        self.tabla_listComponentes.heading("Usados", text="USADOS", anchor=tk.W)

        self.tabla_listComponentes.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla_listComponentes.column("Nombre", stretch=tk.NO, minwidth="25", width="200")
        self.tabla_listComponentes.column("Almacen", stretch=tk.NO, minwidth="25", width="200")
        self.tabla_listComponentes.column("Dañados", stretch=tk.NO, minwidth="25", width="200")
        self.tabla_listComponentes.column("Usados", stretch=tk.YES, minwidth="25", width="200")
        self.tabla_listComponentes.bind("<ButtonPress-1>", self.on_treeview_click)
        # edit column

        # iterar la lista de campos
        for index, item in enumerate(self.list_componentes, start=1):
            id_component=item[0]
            items=list(item)
            items[0]=index
            self.tabla_listComponentes.insert("", tk.END, text=id_component, values=tuple(items))

        # botones finales

        # Buscar
        boton_buscar = tk.Button(self.framePrincipal, text="Buscar", command=self.buscarComponente)
        boton_buscar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        boton_buscar.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Crear
        boton_crear = tk.Button(self.framePrincipal, text="Registrar", command=lambda:self.cambioInterfaz(self.controlComponent))
        boton_crear.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        boton_crear.grid(row=2, column=1, padx=10, pady=10)

    def on_treeview_click(self, event):
        if self.order=="ASC":
            self.order="DESC"
        else:
            self.order="ASC"

        column = self.tabla_listComponentes.identify_column(event.x)
        item = self.tabla_listComponentes.identify_row(event.y)
        region = self.tabla_listComponentes.identify_region(event.x ,event.y)

        if item=="" and region=="heading":
            if column == "#1":
                self.list_componentes = Componentes.list(ordenador={"campo":"com.id", "order":self.order})
            elif column == "#2":
                self.list_componentes = Componentes.list(ordenador={"campo":"com.nombre", "order":self.order})
            elif column == "#3":
                self.list_componentes = Componentes.list(ordenador={"campo":"com.almacen", "order":self.order})
            elif column == "#4":
                self.list_componentes = Componentes.list(ordenador={"campo":"com.dañados", "order":self.order})
            elif column == "#5":
                self.list_componentes = Componentes.list(ordenador={"campo":"com.uso", "order":self.order})
        
            self.listComponentes(False)

    # *la que destrulle y crea una nueva interfaz
    def cambioInterfaz(self, interfaz):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        interfaz()

    def buscarComponente(self):
        id_componente = self.tabla_listComponentes.item(self.tabla_listComponentes.selection())["text"]
        if id_componente == "":
            respuesta=messagebox.showwarning("Buscar Componente", "No ha seleccionado ningun registro")
            if respuesta=="ok":
                return
        
        self.data_component = Componentes.list(id_componente=int(id_componente))
        self.cambioInterfaz(self.controlComponent)

    def controlComponent(self):
        self.icon_papelera = leer_imagen("img/trash.png", (30, 30))
        self.framePrincipal.columnconfigure(1, weight=1)

        buttonRegresar = tk.Button(self.framePrincipal, text="Regresar")
        buttonRegresar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
            command=lambda:self.cambioInterfaz(self.listComponentes),
        )
        buttonRegresar.grid(row=0, column=0, padx=10, pady=10)

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Componentes")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        # Nombre
        label_nombre = tk.Label(self.framePrincipal, text="Nombre:")
        label_nombre.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_nombre.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Componente
        label_componente = tk.Label(self.framePrincipal, text="Componente:")
        label_componente.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_componente.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # usados
        label_usados = tk.Label(self.framePrincipal, text="Usados:")
        label_usados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_usados.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        # almacen
        label_almacen = tk.Label(self.framePrincipal, text="Almacen:")
        label_almacen.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_almacen.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        # dañados
        label_dañados = tk.Label(self.framePrincipal, text="Dañados:")
        label_dañados.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_dañados.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        # Caracteristicas
        label_caracteristicas = tk.Label(self.framePrincipal, text="Caracteristicas")
        label_caracteristicas.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_caracteristicas.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        # Frame
        self.frameData = tk.Frame(self.framePrincipal, bg=COLOR_BASE)
        self.frameData.grid(row=4, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")

        self.frameCaracteristicas = tk.Frame(self.framePrincipal, bg=COLOR_BASE, height=30)
        self.frameCaracteristicas.grid(row=9, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")
        self.caracteristicas=[]
        self.contador_caracteristicas=0

        # # CAMPOS
        self.mi_nombre = tk.StringVar()
        self.usados = tk.IntVar()
        self.almacen = tk.IntVar()
        self.dañados = tk.IntVar()
        
        self.entry_nombre = tk.Entry(self.framePrincipal, textvariable=self.mi_nombre)
        self.entry_nombre.config(font=FONT_LABEL)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=7, columnspan=2, sticky="ew")

        self.list_componentes = TipoEquipos.list(equipo_componente=False, ordenador={"campo":"nombre", "order":"ASC"})
        self.select_componente = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=list_values(self.list_componentes), width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_componente.grid(row=3, column=1, padx=10, pady=7, columnspan=2)
        self.select_componente.config(style="Combobox.TCombobox")
        self.select_componente.bind("<<ComboboxSelected>>", self.selectComponent)

        self.entry_usados = tk.Entry(self.framePrincipal, textvariable=self.usados)
        self.entry_usados.config(font=FONT_LABEL, state="disabled")
        self.entry_usados.grid(row=5, column=1, padx=10, pady=7, columnspan=2, sticky="ew")

        self.entry_almacen = tk.Entry(self.framePrincipal, textvariable=self.almacen)
        self.entry_almacen.config(font=FONT_LABEL)
        self.entry_almacen.grid(row=6, column=1, padx=10, pady=7, columnspan=2, sticky="ew")

        self.entry_dañados = tk.Entry(self.framePrincipal, textvariable=self.dañados)
        self.entry_dañados.config(font=FONT_LABEL)
        self.entry_dañados.grid(row=7, column=1, padx=10, pady=7, columnspan=2, sticky="ew")

        self.list_caracteristicas = Caracteristicas.list(ordenador={"campo":"nombre", "order":"ASC"})
        self.list_values_caracteristicas=list_values(self.list_caracteristicas)
        self.select_caracteristicas = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=self.list_values_caracteristicas, width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_caracteristicas.grid(row=8, column=1, padx=10, pady=7)
        self.select_caracteristicas.config(style="Combobox.TCombobox")
        self.boton_agregar = tk.Button(self.framePrincipal, text="Agregar", command=self.agregarCaracteristica)
        self.boton_agregar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL)
        self.boton_agregar.grid(row=8, column=2, padx=10, pady=10)
        self.boton_guardar = tk.Button(
            self.framePrincipal, text="Guardar", command=self.guardar
        )
        if self.data_component:
            self.mi_nombre.set(f"{self.data_component[1]}")
            self.usados.set(f"{self.data_component[4]}")
            self.dañados.set(f"{self.data_component[3]}")
            self.almacen.set(f"{self.data_component[2]}")
            indice_data=determinar_indice(self.list_componentes, self.data_component[5])
            self.select_componente.current(indice_data)
            self.dataComponente()
            valores=self.list_componentes[self.select_componente.current()]
            self.label_value_nombre.config(text=f"{valores[1]}")
            self.label_value_marca.config(text=f"{valores[2]}")
            self.label_value_modelo.config(text=f"{valores[3]}")
            self.label_value_descripcion.config(text=f"{valores[5]}")

            for caracteristicas in self.data_component[10]:
                frame=tk.Frame(self.frameCaracteristicas, bg=COLOR_BASE)
                frame.pack(side=tk.TOP, fill=tk.BOTH, ipady=10, ipadx=10)
                mi_caracteristica = tk.StringVar()
                mi_caracteristica.set(f"{caracteristicas[4]}")
                entry_nombre = tk.Entry(frame, textvariable=mi_caracteristica, width=TAMAÑO_MEDIUN_ENTRYS, font=FONT_LABEL)
                buton_eliminar = tk.Button(frame, image=self.icon_papelera,  bg=COLOR_ROJO, width=40, pady=10, cursor="hand2", activebackground=COLOR_ROJO)
                
                caracteristica=[
                    caracteristicas[2], #id caracteristica
                    caracteristicas[3], #nombre
                    caracteristicas[0], #id tabla componetens_has_caracteristicas
                    mi_caracteristica,  #Strinvar
                    frame,              #Frame
                    "update",           #Tipo
                    entry_nombre,       #Entry
                    buton_eliminar      #Button
                ]

                label = tk.Label(frame, text=f"{caracteristicas[3]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
                label.pack(side=tk.LEFT, padx=10)

                buton_eliminar.config(command=lambda:self.deleteTableCaracteristica(caracteristica))
                buton_eliminar.pack(side=tk.RIGHT, padx=10)

                entry_nombre.pack(side=tk.RIGHT, padx=10)

                self.caracteristicas.append(caracteristica)

            self.list_values_caracteristicas=verificacion_campos([self.list_caracteristicas, 0], [self.caracteristicas, 0])
            self.select_caracteristicas.config(values=self.list_values_caracteristicas)
            
            # Botones
            self.boton_nuevo = tk.Button(
                self.framePrincipal, text="Editar", command=self.habilitar_campos
            )
            self.boton_cancelar = tk.Button(
            self.framePrincipal, text="Eliminar", command=self.deleteComponent
            )
            self.desabilitar_campos()
        
        else:
            # Botones
            self.boton_nuevo = tk.Button(
                self.framePrincipal, text="Nuevo", command=self.habilitar_campos
            )
            
            self.boton_cancelar = tk.Button(
            self.framePrincipal, text="Cancelar", command=self.desabilitar_campos
            )
        
        self.boton_nuevo.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        self.boton_nuevo.grid(row=10, column=0, padx=8, pady=10)

        
        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_guardar.grid(row=10, column=1, padx=8, pady=10)

        self.boton_cancelar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_cancelar.grid(row=10, column=2, padx=8, pady=10)

    def dataComponente(self):
        label_nombre = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Nombre:")
        label_marca = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Marca:")
        label_modelo = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Modelo:")
        label_descripcion = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, text="Descripción:")

        self.label_value_nombre = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_marca = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_modelo = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="")
        self.label_value_descripcion = tk.Label(self.frameData, font=FONT_LABEL, bg=COLOR_BASE, fg=LETRA_OSCURA, text="", justify="left", wraplength=3*200)
        
        label_nombre.grid(row=0, column=0, padx=60, pady=10, sticky="w")
        label_marca.grid(row=0, column=1, padx=40, pady=10, sticky="w")
        label_modelo.grid(row=0, column=2, padx=50, pady=10, sticky="w")
        label_descripcion.grid(row=2, column=0, padx=60, pady=10, sticky="w")

        self.label_value_nombre.grid(row=1, column=0, padx=60, sticky="w")
        self.label_value_marca.grid(row=1, column=1, padx=40, sticky="w")
        self.label_value_modelo.grid(row=1, column=2, padx=50, sticky="w")
        self.label_value_descripcion.grid(row=3, column=0, padx=60, sticky="w", columnspan=3)

    def selectComponent(self, event):
        self.frameData.destroy()
        self.frameData = tk.Frame(self.framePrincipal, bg=COLOR_BASE)
        self.frameData.grid(row=4, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")
        self.dataComponente()
        valores=self.list_componentes[self.select_componente.current()]
        self.label_value_nombre.config(text=f"{valores[1]}")
        self.label_value_marca.config(text=f"{valores[2]}")
        self.label_value_modelo.config(text=f"{valores[3]}")
        self.label_value_descripcion.config(text=f"{valores[5]}")

    def agregarCaracteristica(self):
        try:
            seleccionado=self.select_caracteristicas.current()
            caracteristica_seleccionada=determinar_campo(self.list_caracteristicas, self.list_values_caracteristicas[seleccionado])
        
            frame=tk.Frame(self.frameCaracteristicas, bg=COLOR_BASE)
            frame.pack(side=tk.TOP, fill=tk.BOTH, ipady=10, ipadx=10)
            mi_caracteristica = tk.StringVar()
            buton_eliminar = tk.Button(frame, image=self.icon_papelera,  bg=COLOR_ROJO, width=40, pady=10, cursor="hand2", activebackground=COLOR_ROJO)
            entry_nombre = tk.Entry(frame, textvariable=mi_caracteristica, width=TAMAÑO_MEDIUN_ENTRYS, font=FONT_LABEL)
            caracteristica=[
                caracteristica_seleccionada[0], #id
                caracteristica_seleccionada[1], #nombre
                caracteristica_seleccionada[2], #descripcion
                mi_caracteristica,              #strinvar
                frame,                          #frame
                "new",                          #tipo
                entry_nombre,                   #Entry
                buton_eliminar,                 #boton
            ]

            label = tk.Label(frame, text=f"{caracteristica_seleccionada[1]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
            label.pack(side=tk.LEFT, padx=10)

            buton_eliminar.config(command=lambda:self.eliminarCaracteristica(caracteristica))
            buton_eliminar.pack(side=tk.RIGHT, padx=10)

            entry_nombre.pack(side=tk.RIGHT, padx=10)

            self.caracteristicas.append(caracteristica)

            self.list_values_caracteristicas=verificacion_campos([self.list_caracteristicas, 0], [self.caracteristicas, 0])
            self.select_caracteristicas.config(values=self.list_values_caracteristicas)
        
        except Exception as error:
            controlError(
                error, 
                messageRange="No hay mas caracteristicas para agregar"
            )

    def eliminarCaracteristica(self, caracteristica):

        caracteristica[4].destroy()
        for index, campo in enumerate(self.caracteristicas):
            if campo[0] == caracteristica[0]:
                self.caracteristicas.pop(index)

        self.list_values_caracteristicas=verificacion_campos([self.list_caracteristicas, 0], [self.caracteristicas, 0])
        self.select_caracteristicas.config(values=self.list_values_caracteristicas)

    def deleteTableCaracteristica(self, caracteristica):
        try:
            valor = messagebox.askquestion(
                "Eliminar Caracteristica", "Desea eliminar la caracteristica seleccionada"
            )
            if valor == "yes":
                Componentes_has_Caracteristicas.delete(caracteristica[2])
                caracteristica[4].destroy()
                for index, campo in enumerate(self.caracteristicas):
                    if campo[0] == caracteristica[0]:
                        self.caracteristicas.pop(index)

                self.list_values_caracteristicas=verificacion_campos([self.list_caracteristicas, 0], [self.caracteristicas, 0])
                self.select_caracteristicas.config(values=self.list_values_caracteristicas)

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )

    def desabilitar_campos(self):
        self.entry_nombre.config(state="disabled")
        self.entry_usados.config(state="disabled")
        self.entry_almacen.config(state="disabled")
        self.entry_dañados.config(state="disabled")
        self.select_caracteristicas.config(state="disabled")
        self.select_componente.config(state="disabled")
        self.boton_guardar.config(state="disabled")
        self.boton_agregar.config(state="disabled")

        if self.data_component: 
            for campo in self.caracteristicas:
                campo[6].config(state="disabled")
                campo[7].config(state="disabled")
        else:
            self.frameData.destroy()
            self.mi_nombre.set("")
            self.almacen.set("")
            self.dañados.set("")
            self.select_caracteristicas.set("")
            self.select_componente.set("")
            self.boton_cancelar.config(state="disabled")

            for campo in self.caracteristicas:
                campo[4].destroy()
            self.caracteristicas.clear()
    
    def habilitar_campos(self):
        self.entry_nombre.config(state="normal")
        self.entry_almacen.config(state="normal")
        self.entry_dañados.config(state="normal")
        self.select_caracteristicas.config(state="readonly")
        self.select_componente.config(state="readonly")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")
        self.boton_agregar.config(state="normal")
        
        if self.data_component: 
            for campo in self.caracteristicas:
                campo[6].config(state="normal")
                campo[7].config(state="normal")
        else:
            self.frameData = tk.Frame(self.framePrincipal, height=20, bg=COLOR_BASE)
            self.frameData.grid(row=4, column=0, padx=10, pady=5, columnspan=3, sticky="NSEW")

    def guardar(self):
        try:
            tipo_componente=self.select_componente.current()
            if tipo_componente < 0:
                titulo = "Campos"
                message = "Seleccione un componente"
                messagebox.showwarning(titulo, message)
                return

            almacen=self.almacen.get()
            id_componente=self.list_componentes[tipo_componente][0]
            dañados = self.dañados.get()
            nombre=self.mi_nombre.get()

            caracteristicas=[]
            for caracteristica in self.caracteristicas:
                comprobacion=comprobacionString(caracteristica[3].get(), 200)
                if not comprobacion["status"]:
                    messagebox.showwarning(
                    TITULO_CAMPOS, f'Las caracteristicas {comprobacion["message"]}'
                    )
                    return None
                if caracteristica[5]=="new":
                    caracteristicas.append({
                        "id_caracteristica":caracteristica[0], 
                        "value":str(caracteristica[3].get()), 
                        "tipo":"new"})
                
                if caracteristica[5]=="update":
                    caracteristicas.append({
                        "id_caracteristica":caracteristica[0], 
                        "value":str(caracteristica[3].get()), 
                        "id_caracteristica_component":caracteristica[2], 
                        "tipo":"update"})

            if self.data_component:
                valor = messagebox.askquestion(
                    "Editar Registro", "Desea editar este registro"
                )
                if valor == "yes":
                    componente=Componentes.update(nombre=nombre, dañados=dañados, almacen=almacen, componente_id=id_componente, caracteristicas=caracteristicas, id=self.data_component[0])
                    if componente:
                        titulo="Exito"
                        message="Registro Editado"
                        valor=messagebox.showinfo(titulo, message)
                        if valor == "ok":
                            self.cambioInterfaz(self.listComponentes)
            else:
                valor = messagebox.askquestion(
                    "Registro Nuevo", "Desea ingresar nuevo registro"
                )
                if valor == "yes":
                    componente=Componentes.create(nombre=nombre, dañados=dañados, almacen=almacen, componente_id=id_componente, caracteristicas=caracteristicas)
                    if componente:
                        titulo="Exito"
                        message="Desea crear otro registro"
                        valor=messagebox.askquestion(titulo, message)
                        if valor == "yes":
                            self.reset()
                        else:
                            self.cambioInterfaz(self.listComponentes)

        except Exception as error:
            controlError(
                error, 
                messageNumber="Solo se permiten números en los campos de almacen y dañados"
            )

    def reset(self):
        self.almacen.set("")
        self.dañados.set("")
        self.mi_nombre.set("")
        self.select_componente.set("")
        self.select_caracteristicas.set("")
        self.frameData.destroy()

        for caracteristica in self.caracteristicas:
            caracteristica[5].destroy()

    def deleteComponent(self):
        try:
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el componente"
            )
            if valor == "yes":
                detele=Componentes.delete(self.data_component[0])
                if detele:
                    valor=messagebox.showinfo("Exito", "Registro Eliminado")
                    if valor == "ok":
                        self.cambioInterfaz(self.listComponentes)

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )