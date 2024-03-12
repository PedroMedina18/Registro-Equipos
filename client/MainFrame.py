import tkinter as tk
from tkinter import font, ttk
from config import COLOR_BASE, COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_img as util_img


class MainFrame():

    def __init__(self, root):
        self.root = root
        self.imgInicio = util_img.leer_imagen("./img/ordenador.png", (300, 300))
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
   
    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self.root, bg=COLOR_BARRA_SUPERIOR, height=60)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self.root, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(self.root, bg=COLOR_BASE)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)


    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Control de Equipos Locatel")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=25)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, font=font_awesome,command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.config(text="\uf109")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(self.barra_superior, text="Bienvenido")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)


    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
         
        # Botones del menú lateral
        
        self.buttonDashBoard = tk.Button(self.menu_lateral)        
        self.buttonProfile = tk.Button(self.menu_lateral)        
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\u01BA", self.buttonDashBoard),
            ("Profile", "\uf007", self.buttonProfile),
            ("Picture", "\uf03e", self.buttonPicture),
            ("Info", "\uf129", self.buttonInfo),
            ("Settings", "\uf013", self.buttonSettings)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu) 


    # Imagen en el cuerpo principal
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal

        # label = tk.Label(self.cuerpo_principal, image=self.imgInicio ,bg=COLOR_BASE)
        # label.pack(anchor="center")

        # tituloLogo = tk.Label(self.cuerpo_principal, text="Bienvenido", bg=COLOR_BASE)
        # tituloLogo.config(fg=COLOR_BARRA_SUPERIOR, font=("Roboto", 20), padx=10, width=20)
        # tituloLogo.pack(anchor="center")

        # label = tk.Label(self.cuerpo_principal, image=self.imgInicio ,bg="blue", anchor="n")
        # label.pack(expand=True, fill=tk.X, pady=0, ipadx=0)

        self.labelTituloInicial=tk.Label(self.cuerpo_principal, image=self.imgInicio,bg=COLOR_BASE ).pack(side=tk.TOP, fill=tk.X)
        self.labelTituloIniciall=tk.Label(self.cuerpo_principal, text="Bienvenido", bg=COLOR_BASE, font=("Roboto", 30, "bold")).pack(side=tk.TOP, fill=tk.X)


        pass
        

    # *Esta funcion se encarga de configurar los botones del menu
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config( text=f"  {icon}    {text}",cursor="pointer", anchor="w", font=font_awesome, bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)


     # *Esta funcion es para el evento al pasar el cursor
    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))


    # *funcion al dar clik
    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')


    # *funcion al pasar el mause
    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')


    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')