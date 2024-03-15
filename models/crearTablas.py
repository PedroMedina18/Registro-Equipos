from .conexion import ConexionDB
from tkinter import messagebox

def crearTablas():
    conexion = ConexionDB()

    tablaEquipos='''
        CREATE TABLE tipos_equipos(
            id INTEGER, 
            nombre VARCHAR(100),
            marca VARCHAR(100),
            descripcion VARCHAR(500),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    '''
    estados='''
        CREATE TABLE estados(
            id INTEGER, 
            nombre VARCHAR(100),
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    '''
    
    areasTrabajo='''
        CREATE TABLE areas_trabajo(
            id INTEGER, 
            nombre VARCHAR(100),
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )  
    '''

    tipoRegistro='''
        CREATE TABLE tipo_registro(
            id INTEGER, 
            nombre VARCHAR(100),
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )  
    '''


    try:
        conexion.cursor.execute(tablaEquipos)
        conexion.cursor.execute(estados)
        conexion.cursor.execute(areasTrabajo)
        conexion.cursor.execute(tipoRegistro)
        conexion.cerrar()
        titulo = "Crear Tablas"
        message= "Se creo todas las tablas de la base de datos"
        messagebox.showinfo(titulo, message)
    except Exception as ex:
        print(ex)
        titulo = "Crear Tablas"
        message= "La tabla ya esta creada"
        messagebox.showerror(titulo, message)

