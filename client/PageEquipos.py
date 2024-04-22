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
    LETRA_CLARA,
    ACTIVE_VERDE,
    ACTIVE_AZUL,
    TAMAÑO_BOTON,
    TAMAÑO_ENTRYS
)
from util.list_values import list_values, determinar_campo, verificacion_campos
from util.util_error import controlError
from util.util_img import leer_imagen
from models.equipos import Equipos
from models.estados import Estados
from models.tipos_equipos import TipoEquipos
from models.areas_trabajo import AreasTrabajo
from models.componentes import Componentes

class PageEquipos:
    def __init__(self, root, cambio_cuerpo):
        self.root = root
        self.framePrincipal = None
        self.cambio_cuerpo = cambio_cuerpo
        self.id_equipo = None
        self.crearCuerpo()
        self.lista_Equipos()

    # *para crear el cuerpo principal
    def crearCuerpo(self):

        # LISTA VALORES SELECTS
        self.list_tipos_equipos=TipoEquipos.list(equipo_componente=True)
        self.list_areas_trabajos=AreasTrabajo.list()
        self.list_estados=Estados.list()
        self.list_componentes=Componentes.list()
        self.list_ubicacion=["Plaza Bolivar", "La Marrón"]


        if self.framePrincipal:
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)
        else:
            self.framePrincipal = tk.Frame(self.root, bg=COLOR_BASE)
            self.framePrincipal.pack(side=tk.RIGHT, fill="both", expand=True)

    # *la primera lista en donde se ven todas las tablas
    def lista_Equipos(self):

        # Titulo
        tituloPage = tk.Label(self.framePrincipal, text="Lista de Equipos")
        tituloPage.config(font=FONT_LABEL_TITULO, bg=COLOR_BASE, anchor="center")
        tituloPage.grid(row=0, column=0, padx=10, pady=10, columnspan=5)


        ## SELECT
        label_equipo = tk.Label(self.framePrincipal, text="Equipo")
        label_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_equipo.grid(row=1, column=0, padx=10, pady=5)

        select_tipo_equipo = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=list_values(self.list_tipos_equipos)
        )
        select_tipo_equipo.grid(row=2, column=0, padx=10, pady=5)


        label_ubicacion = tk.Label(self.framePrincipal, text="Ubicación")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=1, column=1, padx=10, pady=5)

        select_ubicacion = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=self.list_ubicacion
        )
        select_ubicacion.grid(row=2, column=1, padx=10, pady=5)


        label_estado = tk.Label(self.framePrincipal, text="Estado")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=1, column=2, padx=10, pady=5)

        select_estado = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=list_values(self.list_estados)
        )
        select_estado.grid(row=2, column=2, padx=10, pady=5)


        label_area = tk.Label(self.framePrincipal, text="Are de Trabajo")
        label_area.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area.grid(row=1, column=3, padx=10, pady=5)

        select_area_trabajo = ttk.Combobox(
            self.framePrincipal, state="readonly",
            values=list_values(self.list_areas_trabajos)
        )
        select_area_trabajo.grid(row=2, column=3, padx=10, pady=5)

        # TABLA
        self.list_equipos = Equipos.list()
        self.list_equipos.reverse()

        self.tabla_listEquipos = ttk.Treeview(
            self.framePrincipal, columns=("Serial", "Equipo", "Ubicación", "Estado", "Area"), height=25
        )
        self.tabla_listEquipos.grid(row=3, column=0, sticky="NSEW", padx=10, columnspan=8)

        # Scroll bar
        scroll = ttk.Scrollbar(
            self.framePrincipal, orient="vertical", command=self.tabla_listEquipos.yview
        )
        scroll.grid(row=3, column=7, sticky="ns")
        self.tabla_listEquipos.configure(yscrollcommand=scroll.set)

        self.tabla_listEquipos.heading("#0", text="ID", anchor=tk.W)
        self.tabla_listEquipos.heading("#1", text="SERIAL", anchor=tk.W)
        self.tabla_listEquipos.heading("#2", text="EQUIPO", anchor=tk.W)
        self.tabla_listEquipos.heading("#3", text="UBICACIÓN", anchor=tk.W)
        self.tabla_listEquipos.heading("#4", text="ESTADO", anchor=tk.W)
        self.tabla_listEquipos.heading("#5", text="AREA DE TRABAJO", anchor=tk.W)


        # edit column
        self.tabla_listEquipos.column("#0", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#1", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#2", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#3", stretch=tk.NO, minwidth="25", width="150")
        self.tabla_listEquipos.column("#4", stretch=tk.NO, minwidth="25", width="150" )
        self.tabla_listEquipos.column("#5", stretch=tk.YES, minwidth="25")


        # iterar la lista de campos
        for item in self.list_equipos:
            ubicacion="Plaza Bolívar" if item[3]==0 else "La Marron"
            self.tabla_listEquipos.insert("", 0, text=item[0], values=(item[1], item[2], ubicacion, item[4], item[5]))

        # botones finales

        # Buscar
        boton_buscar = tk.Button(self.framePrincipal, text="Buscar")
        boton_buscar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
        )
        boton_buscar.grid(row=4, column=0, padx=10, pady=10)

        # Crear
        boton_crear = tk.Button(self.framePrincipal, text="Registrar", command=self.crearEquipos)
        boton_crear.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_AZUL,
            cursor="hand2",
            activebackground=ACTIVE_AZUL,
        )
        boton_crear.grid(row=4, column=3, padx=10, pady=10)

     # *la que destrulle y crea el para registrar equipos
    def crearEquipos(self):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        self.frameRegisterEquipos()

    def frameRegisterEquipos(self):
        self.icon_papelera = leer_imagen("./img/trash.png", (30, 30))
        self.componentes=[]

        buttonRegresar = tk.Button(self.framePrincipal, text="Regresar")
        buttonRegresar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
            command=self.regresar,
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

        label_tipo_equipo = tk.Label(self.framePrincipal, text="Tipo de Equipo:")
        label_tipo_equipo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_tipo_equipo.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        label_ubicacion = tk.Label(self.framePrincipal, text="Ubicacion:")
        label_ubicacion.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_ubicacion.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        label_estado = tk.Label(self.framePrincipal, text="Estado:")
        label_estado.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_estado.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        label_area_trabajo = tk.Label(self.framePrincipal, text="Area de Trabajo:")
        label_area_trabajo.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_area_trabajo.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        # SELECTS
        self.mi_serial = tk.StringVar()
        self.entry_serial = tk.Entry(self.framePrincipal, textvariable=self.mi_serial)
        self.entry_serial.config(width=TAMAÑO_ENTRYS, font=FONT_LABEL)
        self.entry_serial.grid(row=2, column=1, pady=10, padx=10, columnspan=2)

        self.select_tipo_equipo = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_tipos_equipos))
        self.select_tipo_equipo.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

        self.select_ubicacion = ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_ubicacion)
        self.select_ubicacion.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        self.select_estado = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_estados))
        self.select_estado.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

        self.select_area_trabajo = ttk.Combobox(self.framePrincipal, state="readonly", values=list_values(self.list_areas_trabajos))
        self.select_area_trabajo.grid(row=6, column=1, padx=10, pady=10, columnspan=2)

        label_componente = tk.Label(self.framePrincipal, text="Componentes")
        label_componente.config(font=FONT_LABEL, bg=COLOR_BASE)
        label_componente.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.list_values_componentes=list_values(self.list_componentes)
        self.select_componente = ttk.Combobox(self.framePrincipal, state="readonly", values=self.list_values_componentes)
        self.select_componente.grid(row=7, column=1, padx=10, pady=10)

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
        self.boton_agregar.grid(row=7, column=2, padx=10, pady=10)

        self.frameComponentes = tk.Frame(self.framePrincipal, bg=COLOR_BASE, height=150)
        self.frameComponentes.grid(row=8, column=0, pady=5, padx=10, columnspan=3, sticky="NSEW")

        self.boton_guardar = tk.Button(self.framePrincipal, text="Guardar", command=self.guardar)
        self.boton_guardar.config(
            width=TAMAÑO_BOTON,
            font=FONT_LABEL,
            fg=LETRA_CLARA,
            bg=COLOR_VERDE,
            cursor="hand2",
            activebackground=ACTIVE_VERDE,
            command=self.guardar
        )
        self.boton_guardar.grid(row=9, column=1, padx=10, pady=10)
    
    def agregarComponente(self):
        try:
            seleccionado = self.select_componente.current()
            componente_seleccionada =  determinar_campo(self.list_componentes, self.list_values_componentes[seleccionado])
        
            frame=tk.Frame(self.frameComponentes, bg=COLOR_BASE)
            frame.pack(side=tk.TOP, fill=tk.BOTH, ipady=10, ipadx=10)
            componente=[
                componente_seleccionada[0],
                componente_seleccionada[1],
                frame
            ]

            label = tk.Label(frame, text=f"{componente[1]}", font=FONT_LABEL, bg=COLOR_BASE, anchor="w")
            label.pack(side=tk.LEFT, padx=10)

            buton_eliminar = tk.Button(frame, image=self.icon_papelera,  bg=COLOR_ROJO, width=40, pady=10, cursor="hand2", activebackground=COLOR_ROJO, command=lambda:self.eliminarComponente(componente))
            buton_eliminar.pack(side=tk.RIGHT, padx=10)

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
            id_tipo_equipo=self.list_tipos_equipos[tipo_equipo][0]
            id_estado=self.list_estados[estado][0]
            id_area_trabajo=self.list_areas_trabajos[area_trabajo][0]
            
            componentes=[data[0] for data in self.componentes]

            crear_equipo=Equipos.create(serial=serial, area_trabajo_id=id_area_trabajo, estado_actual_id=id_estado, tipos_equipos_id=id_tipo_equipo, bolivar_marron=ubicacion, componentes=componentes)

            if crear_equipo:
                titulo="Exito"
                message="Desea crear otro registro"
                valor=messagebox.askquestion(titulo, message)
                if valor == "yes":
                    self.reset()
                else:
                    self.regresar()
                
            else:
                titulo="Error"
                message="Error en el registro"
                messagebox.showerror(titulo, message)

        except Exception as error:
            controlError(
                error
            )

    def regresar(self):
        self.framePrincipal.destroy()
        self.framePrincipal = None
        self.crearCuerpo()
        self.cambio_cuerpo(self.framePrincipal)
        self.lista_Equipos()
    
    def reset(self):
        self.mi_serial.set("")
        self.select_area_trabajo.set("")
        self.select_componente.set("")
        self.select_ubicacion.set("")
        self.select_tipo_equipo.set("")
        self.select_estado.set("")

        for componente in self.componentes:
            componente[2].destroy()
