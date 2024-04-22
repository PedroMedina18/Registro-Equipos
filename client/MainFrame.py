import tkinter as tk
from tkinter import font, ttk
from config import (
    COLOR_BASE,
    COLOR_BARRA_SUPERIOR,
    COLOR_MENU_LATERAL,
    COLOR_MENU_CURSOR_ENCIMA,
    LETRA_CLARA,
    FONT_ROBOTO_SMALL,
    FONT_ROBOTO_MEDIUN
)
import util.util_img as util_img
from .PageTypeEquipos import PageTypeEquipos
from .PageCampos_tablas import PageCampos_tablas
from .PageAgregarCampos import PageAgregarCampos
from .PageListTablas import PageListTablas
from .Pagebasic import PageBasic
from .PageEquipos import PageEquipos
from .PageComponent import PageComponent
from models.crearTablas import crearTablas
from .ScrollFrame import VerticalScrolledFrame
# -------------------------------
from models.tablas import Tablas
from models.caracteristicas import Caracteristicas
from models.estados import Estados
from models.areas_trabajo import AreasTrabajo

from prueba import pruebasql


# La magina inicial al cargar la aplicacion
class MainFrame:

    def __init__(self, root):
        self.root = root
        self.imgInicio = util_img.leer_imagen("./img/ordenador.png", (300, 300))
        self.rootScroll=None
        self.cuerpo_principal = None
        self.menus()
        self.barra_superior()
        self.menu_lateral()
        self.create_cuerpo_principal()

    # *Se crea la barra de menus
    def menus(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu, width=300, heigh=300)

        menu_inicio = tk.Menu(barra_menu, tearoff=0)
        menu_tablas = tk.Menu(barra_menu, tearoff=0)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)

        menu_inicio.add_command(label="Crear Base de Datos", command=crearTablas)
        menu_inicio.add_command(label="Salir", command=self.root.destroy)
        menu_inicio.add_command(label="Prueba", command=pruebasql)

        menu_tablas.add_command(
            label="Tablas",
            command=lambda: self.destroyCuerpo(
                object_page=PageBasic,
                atributos={"titulo": "Nombre de las Tablas", "model": Tablas},
            ),
        )
        menu_tablas.add_command(
            label="Campos",
            command=lambda: self.destroyCuerpo(object_page=PageCampos_tablas),
        )
        menu_tablas.add_command(
            label="Seleccionar Campos",
            command=lambda: self.destroyCuerpo(object_page=PageAgregarCampos),
        )

        menu_opciones.add_command(
            label="Estados",
            command=lambda: self.destroyCuerpo(
                object_page=PageBasic,
                atributos={"titulo": "Estados de los Equipos", "model": Estados},
            ),
        )
        menu_opciones.add_command(
            label="Areas de Trabajo",
            command=lambda: self.destroyCuerpo(
                object_page=PageBasic,
                atributos={"titulo": "Areas de Trabajo", "model": AreasTrabajo},
            ),
        )
        menu_opciones.add_command(
            label="Caracteristicas",
            command=lambda: self.destroyCuerpo(
                object_page=PageBasic,
                atributos={
                    "titulo": "Caracteristicas de los Componentes",
                    "model": Caracteristicas,
                },
            ),
        )

        barra_menu.add_cascade(label="Inicio", menu = menu_inicio)
        barra_menu.add_cascade(label="Tablas", menu = menu_tablas)
        barra_menu.add_cascade(label="Opciones", menu = menu_opciones)

    # funcion encargada de crear el frame en donde va el contenido principal para luego colocar el contenido
    def create_cuerpo_principal(self):
        if not self.rootScroll:
            frameScroll = VerticalScrolledFrame(self.root)
            self.rootScroll=frameScroll
            frameScroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # *se crea el scroll
        if self.cuerpo_principal:
            self.cuerpo_principal.destroy()

        FramePrincipal = tk.Frame(self.rootScroll.interior, bg=COLOR_BASE)
        self.cuerpo_principal = FramePrincipal
        FramePrincipal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.content_principal()

    # *Opciones de a barra superior
    def barra_superior(self):
        self.frame_barra_superior = tk.Frame(self.root, bg=COLOR_BARRA_SUPERIOR, height=60)
        self.frame_barra_superior.pack(side=tk.TOP, fill=tk.BOTH)

        font_awesome = font.Font(family="FontAwesome", size=12)
        self.menu = util_img.leer_imagen("./img/menu.png", (50, 50))

        # Etiqueta de título
        self.labelTitulo = tk.Label(
            self.frame_barra_superior, text="Control de Equipos Locatel"
        )
        self.labelTitulo.config(
            fg=LETRA_CLARA, font=FONT_ROBOTO_MEDIUN, bg=COLOR_BARRA_SUPERIOR, pady=10, width=25
        )
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(
            self.frame_barra_superior,
            font=font_awesome,
            command=self.toggle_panel,
            bd=0,
            bg=COLOR_BARRA_SUPERIOR,
            fg=LETRA_CLARA,
        )
        self.buttonMenuLateral.config(image=self.menu, cursor="hand2")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(self.frame_barra_superior, text="Bienvenido")
        self.labelTitulo.config(
            fg=LETRA_CLARA, font=FONT_ROBOTO_SMALL, bg=COLOR_BARRA_SUPERIOR, padx=10, width=20
        )
        self.labelTitulo.pack(side=tk.RIGHT)

    # *Crea todos los botones del menu lateral
    def menu_lateral(self):
        self.menu_lateral = tk.Frame(self.root, bg=COLOR_MENU_LATERAL, width=130)
        self.menu_lateral.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Configuración del menú lateral
        self.ancho_menuButton = 18
        self.alto_menuButton = 2
        self.font_awesomeButton = font.Font(family="FontAwesome", size=15)
        self.home = util_img.leer_imagen("./img/home.png", (50, 50))
        self.destokp = util_img.leer_imagen("./img/destokp.png", (50, 50))
        self.devices = util_img.leer_imagen("./img/devices.png", (50, 50))
        self.tables = util_img.leer_imagen("./img/table.png", (50, 50))
        self.component = util_img.leer_imagen("./img/componente.png", (50, 50))

        # Botones del menú lateral
        self.buttonHome = ttk.Button(
            self.menu_lateral,
            text="Inicio",
            image=self.home,
            compound="left",
            cursor="hand2",
            command=lambda: self.create_cuerpo_principal()
        )
        self.buttonDevices = ttk.Button(
            self.menu_lateral,
            text="Tipos de Equipo",
            image=self.devices,
            compound="left",
            cursor="hand2",
            command=lambda: self.destroyCuerpo(object_page=PageTypeEquipos)
        )
        self.buttonComponent = ttk.Button(
            self.menu_lateral,
            text="Componente",
            image=self.component,
            compound="left",
            cursor="hand2",
            command=lambda: self.destroyCuerpo(
                object_page=PageComponent, atributos={"funtion_cambio_cuerpo": True}
            )
            
        )
        self.buttonDestokp = ttk.Button(
            self.menu_lateral,
            text="Equipos",
            image=self.destokp,
            compound="left",
            cursor="hand2",
            command=lambda: self.destroyCuerpo(
                object_page=PageEquipos, atributos={"funtion_cambio_cuerpo": True}
            )
        )
        self.buttonTable = ttk.Button(
            self.menu_lateral,
            text="Tablas",
            image=self.tables,
            compound="left",
            cursor="hand2",
            command=lambda: self.destroyCuerpo(
                object_page=PageListTablas, atributos={"funtion_cambio_cuerpo": True}
            )
        )
        buttons_info = [
            (self.buttonHome),
            (self.buttonDevices),
            (self.buttonComponent),
            (self.buttonDestokp),
            (self.buttonTable),
        ]

        for button in buttons_info:
            self.configurar_boton_menu(
                button,
                self.font_awesomeButton,
                self.ancho_menuButton,
                self.alto_menuButton,
            )

    # *Esta funcion se encarga de configurar los botones del menu
    def configurar_boton_menu(self, button, font_awesome, ancho_menu, alto_menu):
        style = ttk.Style()
        style.configure(
            "ButtonNormal.TButton",
            font=font_awesome,
            background=COLOR_MENU_LATERAL,
            foreground="white",
            borderwidth=0,
            justify="left",
            width=ancho_menu,
            height=alto_menu,
        )
        style.configure(
            "ButtonHover.TButton",
            font=font_awesome,
            background=COLOR_MENU_CURSOR_ENCIMA,
            foreground="white",
            borderwidth=0,
            justify="left",
            width=ancho_menu,
            height=alto_menu,
        )
        # style.theme_create( "button-center", parent="alt", settings={
        # "TButton": {"configure": {"anchor": "center"}}} )
        style.theme_use("alt")

        button.config(style="ButtonNormal.TButton")
        button.pack(side=tk.TOP, ipady=10)
        self.bind_hover_events(button)

    # *Funcion para activar los estados del boton
    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    # *funcion al dar clik
    def on_enter(self, event, button):
        style = ttk.Style()
        button.config(style="ButtonHover.TButton")

    # *funcion al pasar el mause
    def on_leave(self, event, button):
        button.config(style="ButtonNormal.TButton")

    # *Imagen en el cuerpo principal
    def content_principal(self):
        # Imagen en el cuerpo principal

        self.labelTituloInicial = tk.Label(
            self.cuerpo_principal,
            text="Bienvenido",
            image=self.imgInicio,
            bg=COLOR_BASE,
            font=("Roboto", 30, "bold"),
            compound="top",
        ).pack(side=tk.TOP, fill=tk.X, pady=100)

    # *Funcion para quitaro colocar el menu lateral
    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill="y")

    # *Funcion que destruye el frame principal para remplazarlo por otro de la iterfaz elejida
    def destroyCuerpo(self, object_page=object, atributos={}):
        self.cuerpo_principal.destroy()
        if "titulo" in atributos and "model" in atributos:
            nuevo_cuerpo_principal = object_page(
                self.rootScroll.interior, atributos["titulo"], atributos["model"]
            )
        elif "funtion_cambio_cuerpo" in atributos:
            nuevo_cuerpo_principal = object_page(
                self.rootScroll.interior, self.cambio_cuerpo_principal
            )
        else:
            nuevo_cuerpo_principal = object_page(self.rootScroll.interior)

        self.cuerpo_principal = nuevo_cuerpo_principal.framePrincipal

    def cambio_cuerpo_principal(self, cuerpo):
        self.cuerpo_principal = cuerpo
