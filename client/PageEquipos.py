import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    FONT_LABEL,
    FONT_LABEL_TITULO,
    COLOR_BASE,
    COLOR_AZUL,
    COLOR_VERDE,
    COLOR_ROJO,
    TAMAÑO_MEDIUN_ENTRYS,
    ACTIVE_ROJO,
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    TAMAÑO_BOTON,
    TAMAÑO_ENTRYS
)
from util.list_values import list_values, determinar_campo, verificacion_campos, determinar_indice, Fecha
from util.util_error import controlError
from util.util_img import leer_imagen
from models.equipos import Equipos
from models.historial import Historial
from models.tipos_registros import Tipos_registros
from models.estados import Estados
from models.tipos_equipos import TipoEquipos
from models.areas_trabajo import AreasTrabajo
from models.componentes import Componentes
from models.componentes_has_equipos import Componentes_has_Equipos

class PageEquipos:
    def __init__(self, root, cambio_cuerpo):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = cambio_cuerpo
        self.id_equipo = None
        self.id_historial = None
        self.dataEquipo=None
        self.crearCuerpo()
        self.lista_Equipos()

    # *para crear el cuerpo principal
    def crearCuerpo(self):

        # LISTA VALORES SELECTS
        self.list_tipos_equipos=TipoEquipos.list(equipo_componente=True, order=True)
        self.list_areas_trabajos=AreasTrabajo.list(order=True)
        self.list_estados=Estados.list(order=True)
        self.list_componentes=Componentes.list(almacen=True, order=True)
        self.list_ubicacion=["Plaza Bolivar", "La Marrón"]


        if self.framePrincipal:
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)
        else:
            self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)

    # *la primera lista en donde se ven todas las tablas
    def lista_Equipos(self):
        self.id_equipo = None
        self.dataEquipo=None
        # Titulo
        self.framePrincipal.columnconfigure(0, weight=1)
        tituloPage = tk.Label(self.framePrincipal, text="Lista de Equipos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=4)


        frameSelect=tk.Frame(self.framePrincipal, bg=COLOR_BASE, )
        frameSelect.grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky="NSEW")

        ## SELECT
        label_equipo = tk.Label(frameSelect, text="Equipo")
        label_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_equipo.grid(row=0, column=0, padx=30, pady=5)
        
        self.list_filter_tipos_equipos=list_values(self.list_tipos_equipos)
        self.list_filter_tipos_equipos.insert(0, 'Todos')
        self.select_filter_tipo_equipo = ttk.Combobox(
            frameSelect, state="readonly",
            values=self.list_filter_tipos_equipos, width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_filter_tipo_equipo.grid(row=1, column=0, padx=30, pady=5)
        self.select_filter_tipo_equipo.config(style="Combobox.TCombobox")
        self.select_filter_tipo_equipo.bind("<<ComboboxSelected>>", self.filterEquipos)
        self.select_filter_tipo_equipo.current(0)


        label_ubicacion = tk.Label(frameSelect, text="Ubicación")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=0, column=1, padx=30, pady=5)

        self.list_filter_ubicacion=self.list_ubicacion
        self.list_filter_ubicacion.insert(0, 'Todos')
        self.select_filter_ubicacion = ttk.Combobox(
            frameSelect, state="readonly",
            values=self.list_filter_ubicacion, width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_filter_ubicacion.grid(row=1, column=1, padx=30, pady=5)
        self.select_filter_ubicacion.config(style="Combobox.TCombobox")
        self.select_filter_ubicacion.bind("<<ComboboxSelected>>", self.filterEquipos)
        self.select_filter_ubicacion.current(0)

        label_estado = tk.Label(frameSelect, text="Estado")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=0, column=2, padx=30, pady=5)

        self.list_filter_estados=list_values(self.list_estados)
        self.list_filter_estados.insert(0, 'Todos')
        self.select_filter_estado = ttk.Combobox(
            frameSelect, state="readonly",
            values=self.list_filter_estados, width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_filter_estado.grid(row=1, column=2, padx=30, pady=5)
        self.select_filter_estado.config(style="Combobox.TCombobox")
        self.select_filter_estado.bind("<<ComboboxSelected>>", self.filterEquipos)
        self.select_filter_estado.current(0)

        label_area = tk.Label(frameSelect, text="Are de Trabajo")
        label_area.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area.grid(row=0, column=3, padx=30, pady=5)

        self.list_filter_areas_trabajo=list_values(self.list_areas_trabajos)
        self.list_filter_areas_trabajo.insert(0, 'Todos')
        self.select_filter_area_trabajo = ttk.Combobox(
            frameSelect, state="readonly",
            values=self.list_filter_areas_trabajo, width=20, font=("Arial", 10, "roman"), justify="center"
        )
        self.select_filter_area_trabajo.grid(row=1, column=3, padx=30, pady=5)
        self.select_filter_area_trabajo.config(style="Combobox.TCombobox")
        self.select_filter_area_trabajo.bind("<<ComboboxSelected>>", self.filterEquipos)
        self.select_filter_area_trabajo.current(0)

        # TABLA
        self.list_equipos = Equipos.list()

        self.tabla_equipos()
        # botones finales

        # Buscar
        boton_buscar = tk.Button(self.framePrincipal, text="Buscar", command=self.infoEquipo)
        boton_buscar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        boton_buscar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Crear
        boton_crear = tk.Button(self.framePrincipal, text="Registrar", command=lambda:self.cambioInterfaz(self.frameEquipos))
        boton_crear.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        boton_crear.grid(row=4, column=1, padx=10, pady=10)

    def tabla_equipos(self):
        self.tabla_historial_listEquipos = ttk.Treeview(
            self.framePrincipal, columns=("ID", "Serial", "Alias", "Equipo", "Ubicacion", "Estado", "Area"), height=25, show='headings'
        )
        self.tabla_historial_listEquipos.grid(row=3, column=0, sticky="NSEW", padx=10, columnspan=4)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_historial_listEquipos.yview
        )
        scroll.grid(row=3, column=3, sticky="nsew")
        self.tabla_historial_listEquipos.configure(yscrollcommand=scroll.set)

        self.tabla_historial_listEquipos.heading("ID", text="ID", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Serial", text="SERIAL", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Alias", text="ALIAS", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Equipo", text="EQUIPO", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Ubicacion", text="UBICACIÓN", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Estado", text="ESTADO", anchor=tk.W)
        self.tabla_historial_listEquipos.heading("Area", text="AREA DE TRABAJO", anchor=tk.W)

        # edit column
        self.tabla_historial_listEquipos.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla_historial_listEquipos.column("Serial", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_historial_listEquipos.column("Alias", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_historial_listEquipos.column("Equipo", stretch=tk.NO, minwidth="25", width="140")
        self.tabla_historial_listEquipos.column("Ubicacion", stretch=tk.NO, minwidth="25", width="140")
        self.tabla_historial_listEquipos.column("Estado", stretch=tk.NO, minwidth="25", width="140" )
        self.tabla_historial_listEquipos.column("Area", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        for index, item in enumerate(self.list_equipos, start=1):
            ubicacion="Plaza Bolívar" if item[3]==0 else "La Marrón"
            id_equipo=item[0]
            tupla=(index, item[1], item[2],item[3], ubicacion, item[5], item[6])
            self.tabla_historial_listEquipos.insert("", tk.END, text=id_equipo, values=tupla)

    # *la que destrulle y crea una nueva interfaz
    def cambioInterfaz(self, interfaz):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        interfaz()

    def filterEquipos(self, event):
        tipo_equipo=self.select_filter_tipo_equipo.current()
        ubicacion=self.select_filter_ubicacion.current()
        area_trabajo=self.select_filter_area_trabajo.current()
        estado=self.select_filter_estado.current()

        
        if not tipo_equipo==0:
            tipo_equipo=determinar_campo(list_campos_sql=self.list_tipos_equipos, campo_select=self.list_filter_tipos_equipos[tipo_equipo])[0]

        if not area_trabajo==0:
            area_trabajo=determinar_campo(list_campos_sql=self.list_areas_trabajos, campo_select=self.list_filter_areas_trabajo[area_trabajo])[0]

        if not estado==0:
            estado=determinar_campo(list_campos_sql=self.list_estados, campo_select=self.list_filter_estados[estado])[0]
        

        self.list_equipos=Equipos.filter(estado=estado, area_trabajo=area_trabajo, ubicacion=ubicacion, tipo_equipo=tipo_equipo)
        self.tabla_equipos()

    def frameEquipos(self):
        self.icon_papelera = leer_imagen("./img/trash.png", (30, 30))
        self.framePrincipal.columnconfigure(1, weight=1)
        self.componentes=[]

        buttonRegresar = tk.Button(self.framePrincipal, text="Regresar")
        buttonRegresar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
            command=lambda:self.cambioInterfaz(self.lista_Equipos)
        )
        buttonRegresar.grid(row=0, column=0, padx=10, pady=10)

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Registrar Nuevo Equipo")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        # LABELS
        label_serial = tk.Label(self.framePrincipal, text="Serial:")
        label_serial.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_serial.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        label_alias = tk.Label(self.framePrincipal, text="Alias:")
        label_alias.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_alias.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        label_tipo_equipo = tk.Label(self.framePrincipal, text="Tipo de Equipo:")
        label_tipo_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_tipo_equipo.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        label_ubicacion = tk.Label(self.framePrincipal, text="Ubicacion:")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        label_estado = tk.Label(self.framePrincipal, text="Estado:")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        label_area_trabajo = tk.Label(self.framePrincipal, text="Area de Trabajo:")
        label_area_trabajo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area_trabajo.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        # SELECTS
        self.mi_serial = tk.StringVar()
        self.entry_serial = tk.Entry(self.framePrincipal, textvariable=self.mi_serial)
        self.entry_serial.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_serial.grid(row=2, column=1, pady=10, padx=10, columnspan=2, sticky="ew")

        self.mi_alias = tk.StringVar()
        self.entry_alias = tk.Entry(self.framePrincipal, textvariable=self.mi_alias)
        self.entry_alias.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_alias.grid(row=3, column=1, pady=10, padx=10, columnspan=2, sticky="ew")
        

        self.select_tipo_equipo = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_tipos_equipos), width=25, font=("Arial", 10, "roman"), justify="center")
        self.select_tipo_equipo.config(style="Combobox.TCombobox")
        self.select_tipo_equipo.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        self.select_ubicacion = ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_ubicacion, width=25, font=("Arial", 10, "roman"), justify="center")
        self.select_ubicacion.config(style="Combobox.TCombobox")
        self.select_ubicacion.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

        self.select_estado = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_estados), width=25, font=("Arial", 10, "roman"), justify="center")
        self.select_estado.config(style="Combobox.TCombobox")
        self.select_estado.grid(row=6, column=1, padx=10, pady=10, columnspan=2)

        self.select_area_trabajo = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_areas_trabajos), width=25, font=("Arial", 10, "roman"), justify="center")
        self.select_area_trabajo.config(style="Combobox.TCombobox")
        self.select_area_trabajo.grid(row=7, column=1, padx=10, pady=10, columnspan=2 )


        label_componente = tk.Label(self.framePrincipal, text="Componentes")
        label_componente.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_componente.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.list_values_componentes=list_values(self.list_componentes)
        self.select_componente = ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_values_componentes, width=18, font=("Arial", 10, "roman"), justify="center")
        self.select_componente.config(style="Combobox.TCombobox")
        self.select_componente.grid(row=8, column=1, padx=10, pady=10)
        
        self.boton_agregar = tk.Button(self.framePrincipal, text="Agregar")
        self.boton_agregar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
            command=self.agregarComponente
        )
        self.boton_agregar.grid(row=8, column=2, padx=10, pady=10)

        self.frameComponentes = tk.Frame(self.framePrincipal, bg=COLOR_BASE, height=150)
        self.frameComponentes.grid(row=9, column=0, pady=5, padx=10, columnspan=3, sticky="NSEW")
        self.boton_guardar = tk.Button(
            self.framePrincipal, text="Guardar", command=self.guardar
        )
        if self.dataEquipo:
            buttonHistorial = tk.Button(self.framePrincipal, text="Historial")
            buttonHistorial.config(
                width=TAMAÑO_BOTON,
                font=FONT_LABEL,
                fg=LETRA_CLARA,
               bg=COLOR_AZUL,
               cursor="hand2",
               activebackground=ACTIVE_AZUL,
               command=lambda:self.cambioInterfaz(self.frameHistorial)
            )
            buttonHistorial.grid(row=0, column=2, padx=10, pady=10)

            self.mi_serial.set(f"{self.dataEquipo[0][1]}")
            self.mi_alias.set(f"{self.dataEquipo[0][2]}")
            indice_tipo_equipo=determinar_indice(self.list_tipos_equipos, self.dataEquipo[0][3])
            self.select_tipo_equipo.current(indice_tipo_equipo)
            self.select_ubicacion.current(self.dataEquipo[0][5])
            indice_estado=determinar_indice(self.list_estados, self.dataEquipo[0][6])
            self.select_estado.current(indice_estado)
            indice_area_trabajo=determinar_indice(self.list_areas_trabajos, self.dataEquipo[0][8])
            self.select_area_trabajo.current(indice_area_trabajo)

            # Botones
            self.boton_nuevo = tk.Button(
                self.framePrincipal, text="Editar", command=self.habilitar_campos
            )
            self.boton_cancelar = tk.Button(
            self.framePrincipal, text="Eliminar", command=self.deleteEquipo
            )
            for componente in self.dataEquipo[1]:
                frame=tk.Frame(self.frameComponentes, bg=COLOR_BASE)
                frame.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10)

                frameOption=tk.Frame(frame, bg=COLOR_BASE)
                frameOption.pack(side=tk.TOP, fill=tk.BOTH)
                buton_eliminar = tk.Button(frameOption, image=self.icon_papelera,  bg=COLOR_ROJO, width=50, pady=10, cursor="hand2", activebackground=COLOR_ROJO)
                componenteData=[
                    componente[1],  #Id componente
                    componente[2],  #Nombre
                    frame,          #Frame
                    "old",          #Tipo
                    buton_eliminar, #Boton
                    componente[0],  #id_equipo_componente

                ]

                label = tk.Label(frameOption, text=f"{componente[2]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
                label.pack(side=tk.LEFT)

                buton_eliminar.pack(side=tk.RIGHT, padx=10)
                buton_eliminar.config(state="disabled", command=lambda:self.deleteEquipoComponent(componente))

                frameData=tk.Frame(frame, bg=COLOR_BASE)
                frameData.pack(side=tk.BOTTOM, fill=tk.BOTH)

                labelNombre=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Tipo de Componente:  {componente[3]}")
                labelMarca=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Marca:  {componente[4]}")
                labelModelo=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Modelo:  {componente[5]}")
                labelDescripcion=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Descripción:  {componente[6]}")

                labelNombre.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
                labelMarca.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
                labelModelo.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
                labelDescripcion.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)

                self.componentes.append(componenteData)
            
            
            self.list_values_componentes=verificacion_campos([self.list_componentes, 0], [self.componentes, 0])
            self.select_componente.config(values=self.list_values_componentes)
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

        self.boton_nuevo.grid(row=10, column=0, padx=10, pady=10)

        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        self.boton_guardar.grid(row=10, column=1, padx=10, pady=10)

        self.boton_cancelar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
        )
        self.boton_cancelar.grid(row=10, column=2, padx=10, pady=10)

    def agregarComponente(self):
        try:
            seleccionado = self.select_componente.current()
            componente_seleccionada =  determinar_campo(self.list_componentes, self.list_values_componentes[seleccionado])
        
            frame=tk.Frame(self.frameComponentes, bg=COLOR_BASE)
            frame.pack(side=tk.TOP, fill=tk.BOTH, ipadx=10)
            componente=[
                componente_seleccionada[0],
                componente_seleccionada[1],
                frame,
                "new",       #Tipo
            ]

            frameOption=tk.Frame(frame, bg=COLOR_BASE)
            frameOption.pack(side=tk.TOP, fill=tk.BOTH)

            label = tk.Label(frameOption, text=f"{componente[1]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
            label.pack(side=tk.LEFT)

            buton_eliminar = tk.Button(frameOption, image=self.icon_papelera,  bg=COLOR_ROJO, width=40, pady=10, cursor="hand2", activebackground=COLOR_ROJO, command=lambda:self.eliminarComponente(componente))
            buton_eliminar.pack(side=tk.RIGHT, padx=10)

            frameData=tk.Frame(frame, bg=COLOR_BASE)
            frameData.pack(side=tk.BOTTOM, fill=tk.BOTH)

            labelNombre=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Tipo de Componente:  {componente_seleccionada[6]}")
            labelMarca=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Marca:  {componente_seleccionada[7]}")
            labelModelo=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Modelo:  {componente_seleccionada[8]}")
            labelDescripcion=tk.Label(frame, font=FONT_LABEL, bg=COLOR_BASE, anchor="w", text=f"Descripción:  {componente_seleccionada[9]}")

            labelNombre.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
            labelMarca.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
            labelModelo.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)
            labelDescripcion.pack(side=tk.TOP, fill=tk.BOTH, ipady=3)

            self.componentes.append(componente)

            self.list_values_componentes=verificacion_campos([self.list_componentes, 0], [self.componentes, 0])
            self.select_componente.config(values=self.list_values_componentes)
        
        except Exception as error:
            controlError(
                error, 
                messageRange="No hay mas componentes para agregar"
            )

    def eliminarComponente(self, componente):

        componente[2].destroy()
        for index, campo in enumerate(self.componentes):
            if campo[0] == componente[0]:
                self.componentes.pop(index)

        self.list_values_componentes=verificacion_campos([self.list_componentes, 0], [self.componentes, 0])
        self.select_componente.config(values=self.list_values_componentes)

    def deleteEquipoComponent(self, componente):
        try:
            valor = messagebox.askquestion(
                "Eliminar Componente", "Desea eliminar el componente seleccionada"
            )
            if valor == "yes":
                Componentes_has_Equipos.delete(componente[5], componente[0])
                componente[2].destroy()
                for index, campo in enumerate(self.componentes):
                    if campo[0] == componente[0]:
                        self.componentes.pop(index)

                self.list_values_componentes=verificacion_campos([self.list_componentes, 0], [self.componentes, 0])
                self.select_componente.config(values=self.list_values_componentes)

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )

    def guardar(self):
        try:
            
            tipo_equipo=self.select_tipo_equipo.current()
            if tipo_equipo < 0:
                titulo = "Campos"
                message = "Seleccione un tipo de componente"
                messagebox.showwarning(titulo, message)
                return

            ubicacion=self.select_ubicacion.current()
            if ubicacion < 0:
                titulo = "Campos"
                message = "Seleccione una ubicación"
                messagebox.showwarning(titulo, message)
                return

            estado=self.select_estado.current()
            if estado < 0:
                titulo = "Campos"
                message = "Seleccione un estado"
                messagebox.showwarning(titulo, message)
                return

            area_trabajo=self.select_area_trabajo.current()
            if area_trabajo < 0:
                titulo = "Campos"
                message = "Seleccione un area de trabajo"
                messagebox.showwarning(titulo, message)
                return

            serial=self.mi_serial.get()
            alias=self.mi_alias.get()
            id_tipo_equipo=self.list_tipos_equipos[tipo_equipo][0]
            id_estado=self.list_estados[estado][0]
            id_area_trabajo=self.list_areas_trabajos[area_trabajo][0]
            
            componentes=[]
            for data in self.componentes:
                if data[3]=="new":
                    componentes.append(data[0])
            
            if self.dataEquipo:
                valor = messagebox.askquestion(
                    "Editar Registro", "Desea editar este registro"
                )
                if valor == "yes":
                    actualizar_equipo=Equipos.update(id=self.dataEquipo[0][0], serial=serial, alias=alias, area_trabajo_id=id_area_trabajo, estado_actual_id=id_estado, tipos_equipos_id=id_tipo_equipo, bolivar_marron=ubicacion, componentes=componentes)
                    if actualizar_equipo:
                        titulo="Exito"
                        message="Registro Completado"
                        valor=messagebox.showinfo(titulo, message)
                        if valor == "ok":
                            self.cambioInterfaz(self.lista_Equipos)
            else:
                valor = messagebox.askquestion(
                    "Registro Nuevo", "Desea ingresar nuevo registro "
                )
                if valor == "yes":
                    crear_equipo=Equipos.create(serial=serial, alias=alias, area_trabajo_id=id_area_trabajo, estado_actual_id=id_estado, tipos_equipos_id=id_tipo_equipo, bolivar_marron=ubicacion, componentes=componentes)
                    if crear_equipo:
                        titulo="Exito"
                        message="Desea crear otro registro"
                        valor=messagebox.askquestion(titulo, message)
                        if valor == "yes":
                            self.reset()
                        else:
                            self.cambioInterfaz(self.lista_Equipos)

        except Exception as error:
            controlError(
                error
            )

    def reset(self):
        self.mi_serial.set("")
        self.select_area_trabajo.set("")
        self.select_componente.set("")
        self.select_ubicacion.set("")
        self.select_tipo_equipo.set("")
        self.select_estado.set("")

        for componente in self.componentes:
            componente[2].destroy()

    def infoEquipo(self):
        try:
            self.id_equipo=self.tabla_historial_listEquipos.item(self.tabla_historial_listEquipos.selection())["text"]
            if self.id_equipo=="":
                messagebox.showwarning("Buscar Equipo", "No ha seleccionado ningun registro")
                return
            
            self.dataEquipo=Equipos.list(id=int(self.id_equipo))
            self.cambioInterfaz(self.frameEquipos)
        except Exception as error:
            print(error)
            controlError(
                error,
                titleSelection="Busquedad de Equipo"
            )

    def frameHistorial(self):
        try:
            self.list_tipos_registros=Tipos_registros.list(order=True)
            self.framePrincipal.columnconfigure(1, weight=1)

            buttonRegresar = tk.Button(self.framePrincipal, text="Regresar")
            buttonRegresar.config(
               width=TAMAÑO_BOTON,
               font=FONT_LABEL,
               fg=LETRA_CLARA,
               bg=COLOR_VERDE,
               cursor="hand2",
               activebackground=ACTIVE_VERDE,
               command=lambda:self.cambioInterfaz(self.frameEquipos)
            )
            buttonRegresar.grid(row=0, column=0, padx=10, pady=10)

            tituloPage = tk.Label(self.framePrincipal, text=f"Historial del {self.dataEquipo[0][4]} '{self.dataEquipo[0][2]}'")
            tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
            tituloPage.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

            # Labels
            label_fecha = tk.Label(self.framePrincipal, text="Fecha:")
            label_fecha.config(font=FONT_LABEL, bg=COLOR_BASE)
            label_fecha.grid(row=2, column=0, padx=10, pady=10, sticky="w")

            label_tipo_registro = tk.Label(self.framePrincipal, text="Tipo de Registro:")
            label_tipo_registro.config(font=FONT_LABEL, bg=COLOR_BASE)
            label_tipo_registro.grid(row=3, column=0, padx=10, pady=10, sticky="w")

            label_descripcion = tk.Label(self.framePrincipal, text="Descripción:")
            label_descripcion.config(font=FONT_LABEL, bg=COLOR_BASE)
            label_descripcion.grid(row=4, column=0, padx=10, pady=10, sticky="w")

            # Campos de entrada
            self.fecha = tk.StringVar()

            self.entry_fecha = tk.Entry(self.framePrincipal, textvariable=self.fecha)
            self.entry_fecha.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
            self.entry_fecha.grid(row=2, column=1, pady=10, columnspan=2, sticky="ew")

            self.select_tipo_registro = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_tipos_registros), width=20, font=("Arial", 10, "roman"), justify="center")
            self.select_tipo_registro.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
            self.select_tipo_registro.config(style="Combobox.TCombobox")


            self.entry_descripcion = tk.Text(self.framePrincipal)
            self.entry_descripcion.config(height=10, font=FONT_LABEL)
            self.entry_descripcion.grid(row=4, column=1, pady=10, columnspan=3, sticky="ew")

            scroll = tk.Scrollbar(self.framePrincipal, command=self.entry_descripcion.yview)
            scroll.grid(row=4, column=3, sticky="nsw", pady=10)
            self.entry_descripcion.config(yscrollcommand=scroll.set)

            # Botones

            self.boton_nuevo_historial = tk.Button(
                self.framePrincipal, text="Nuevo", command=self.habilitar_campos_historial
            )
            self.boton_nuevo_historial.config(
                width=TAMAÑO_BOTON,
                font=FONT_LABEL,
                fg=LETRA_CLARA,
                bg=COLOR_VERDE,
                cursor="hand2",
                activebackground=ACTIVE_VERDE,
            )
            self.boton_nuevo_historial.grid(row=5, column=0, padx=8, pady=10)

            self.boton_guardar_historial = tk.Button(
                self.framePrincipal, text="Guardar", command=self.guardar_campos_historial
            )
            self.boton_guardar_historial.config(
                width=TAMAÑO_BOTON,
                font=FONT_LABEL,
                fg=LETRA_CLARA,
                bg=COLOR_AZUL,
                cursor="hand2",
                activebackground=ACTIVE_AZUL,
            )
            self.boton_guardar_historial.grid(row=5, column=1, padx=8, pady=10)

            self.boton_cancelar_historial = tk.Button(
                self.framePrincipal, text="Cancelar", command=self.desabilitar_campos_historial
            )
            self.boton_cancelar_historial.config(
                width=TAMAÑO_BOTON,
                font=FONT_LABEL,
                fg=LETRA_CLARA,
                bg=COLOR_ROJO,
                cursor="hand2",
                activebackground=ACTIVE_ROJO,
            )
            self.boton_cancelar_historial.grid(row=5, column=2, padx=8, pady=10)
            self.tabla_lista_historial()

        except Exception as error:
            controlError(
                error,
                titleSelection="Historial de Equipo"
            )
    
    def tabla_lista_historial(self):
        self.dataHistorial=Historial.list(equipo_id=self.id_equipo)
        self.dataHistorial.reverse()
         # la lista de areas de trabajo
        self.tabla_historial = ttk.Treeview(
            self.framePrincipal, 
            columns=("ID", "Tipo de Registro", "Fecha", "Descripcion"), 
            height=18,
            show='headings'
        )
        self.tabla_historial.grid(row=6, column=0, columnspan=4, sticky="NSEW", padx=10)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_historial.yview
        )
        scroll.grid(row=6, column=3, sticky="nsew")
        self.tabla_historial.configure(yscrollcommand=scroll.set)

        self.tabla_historial.heading("ID", text="ID", anchor=tk.W)
        self.tabla_historial.heading("Tipo de Registro", text="TIPO DE REGISTRO", anchor=tk.W)
        self.tabla_historial.heading("Fecha", text="FECHA", anchor=tk.W)
        self.tabla_historial.heading("Descripcion", text="DESCRIPCIÓN", anchor=tk.W)

        self.tabla_historial.column("ID", stretch=tk.NO, minwidth="25", width="50")
        self.tabla_historial.column("Tipo de Registro", stretch=tk.NO, minwidth="50", width="200")
        self.tabla_historial.column("Fecha", stretch=tk.NO, minwidth="50", width="150")
        self.tabla_historial.column("Descripcion", stretch=tk.YES, minwidth="25")


        # iterar la lista de areas de trabao
        for index, item in enumerate(self.dataHistorial, start=1):
            id_registro=item[0]
            tupla=(index, item[1], Fecha(item[2]), item[3])
            self.tabla_historial.insert("", tk.END, text=id_registro, values=tupla)

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
            command=self.editar_datos_historial,
        )
        boton_editar.grid(row=7, column=0, padx=10, pady=10)

        # eliminar
        boton_eliminar = tk.Button(self.framePrincipal, text="Eliminar")
        boton_eliminar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_ROJO,
            cursor="hand2",
            activebackground=ACTIVE_ROJO,
            command=self.eliminar_datos_historial,
        )
        boton_eliminar.grid(row=7, column=1, padx=10, pady=10)

        self.desabilitar_campos_historial()

    def guardar_campos_historial(self):
        tipo_registro = self.select_tipo_registro.current()
        if tipo_registro < 0:
            titulo = "Campos"
            message = "Seleccione un tipo de registro"
            messagebox.showwarning(titulo, message)
            return
        id_tipo_registro=self.list_tipos_registros[tipo_registro][0]
        fecha = self.fecha.get()
        descripcion = self.entry_descripcion.get(1.0, tk.END)
        if self.id_historial == None:
            valor = messagebox.askquestion(
                "Registro Nuevo", "Desea ingresar nuevo registro"
            )
            if valor == "yes":
                Historial.create(
                    tipo_registro_id=id_tipo_registro, descripcion=descripcion, equipo_id=self.id_equipo, fecha=fecha
                )
            self.tabla_lista_historial()
        else:
            valor = messagebox.askquestion(
                "Editar Registro", "Desea editar este registro"
            )
            if valor == "yes":
                Historial.update(
                     tipo_registro_id=id_tipo_registro, descripcion=descripcion, fecha=fecha, id_registro=self.id_historial
                )
            self.tabla_lista_historial()

    def habilitar_campos_historial(self):
        self.entry_fecha.config(state="normal")
        self.entry_descripcion.config(state="normal")
        self.select_tipo_registro.config(state="readonly")

        self.boton_guardar_historial.config(state="normal")
        self.boton_cancelar_historial.config(state="normal")

    def desabilitar_campos_historial(self):
        self.fecha.set("")
        self.select_tipo_registro.set("")
        self.entry_descripcion.delete(1.0, tk.END)
        self.id_historial = None

        self.entry_fecha.config(state="disabled")
        self.entry_descripcion.config(state="disabled")
        self.select_tipo_registro.config(state="disabled")

        self.boton_guardar_historial.config(state="disabled")
        self.boton_cancelar_historial.config(state="disabled")

    def editar_datos_historial(self):
        try:
            self.desabilitar_campos_historial()
            self.id_historial = self.tabla_historial.item(self.tabla_historial.selection())["text"]
            tipo_registro = self.tabla_historial.item(self.tabla_historial.selection())["values"][1]
            tipo_registro = determinar_indice(list_campos_sql=self.list_tipos_registros, nombre=tipo_registro)
            fecha = self.tabla_historial.item(self.tabla_historial.selection())["values"][2]
            descripcion = self.tabla_historial.item(self.tabla_historial.selection())["values"][3]

            self.habilitar_campos_historial()

            self.entry_fecha.insert(0, fecha)
            self.entry_descripcion.insert(1.0, descripcion)
            self.select_tipo_registro.current(tipo_registro)

        except Exception as error:
            print(error)
            controlError(
                error,
                titleSelection="Edición de Registro"
            )

    def eliminar_datos_historial(self):
        try:
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el registro seleccionado"
            )
            if valor == "yes":
                self.id_historial = self.tabla_historial.item(self.tabla_historial.selection())["text"]
                if self.id_historial=="":
                    titulo="Eliminación de Registro"
                    message="No a seleccionado el registro que desea eliminar"
                    messagebox.showwarning(titulo, message)
                else:
                    Historial.delete_registro(self.id_historial)
                self.tabla_lista_historial()

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )
    
    def deleteEquipo(self):
        try:
            valor = messagebox.askquestion(
                "Eliminar Registro", "Desea Eliminar el equipo"
            )
            if valor == "yes":
                delete=Equipos.delete(self.dataEquipo[0][0])
                if delete:
                    self.cambioInterfaz(self.listComponentes)

        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar de Registro",
                messageTable="El registro no se ha podido eliminar"
            )
    
    def habilitar_campos(self):
        self.entry_serial.config(state="normal")
        self.entry_alias.config(state="normal")
        self.select_area_trabajo.config(state="readonly")
        self.select_estado.config(state="readonly")
        self.select_ubicacion.config(state="readonly")
        self.select_tipo_equipo.config(state="readonly")
        self.select_componente.config(state="readonly")
        self.boton_guardar.config(state="normal")
        self.boton_agregar.config(state="normal")
        self.boton_cancelar.config(state="normal")

        if self.dataEquipo: 
            for campo in self.componentes:
                campo[4].config(state="normal")

    def desabilitar_campos(self):
        self.entry_serial.config(state="disabled")
        self.entry_alias.config(state="disabled")
        self.select_area_trabajo.config(state="disabled")
        self.select_estado.config(state="disabled")
        self.select_ubicacion.config(state="disabled")
        self.select_tipo_equipo.config(state="disabled")
        self.select_componente.config(state="disabled")
        self.boton_guardar.config(state="disabled")
        self.boton_agregar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

        if self.dataEquipo: 
            for campo in self.componentes:
                campo[4].config(state="disabled")

        if not self.dataEquipo:
            self.mi_serial.set("")
            self.mi_alias.set("")
            self.select_area_trabajo.set("")
            self.select_estado.set("")
            self.select_ubicacion.set("")
            self.select_tipo_equipo.set("")
            self.select_componente.set("")

            for campo in self.componentes:
                campo[2].destroy()
            self.componentes.clear()