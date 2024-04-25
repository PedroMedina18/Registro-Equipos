from .conexion import ConexionDB
from tkinter import messagebox


def crearTablas():
    conexion = ConexionDB()

    SQL_tablaEquipos = """
        CREATE TABLE tipos_equipos(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL,
            marca VARCHAR(100) NOT NULL,
            modelo VARCHAR(100) NOT NULL,
            equipo_componente BOOLEAN NOT NULL,
            descripcion VARCHAR(500),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """
    SQL_estados = """
        CREATE TABLE estados(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_areasTrabajo = """
        CREATE TABLE areas_trabajo(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )  
    """

    SQL_tipoRegistro = """
        CREATE TABLE tipo_registro(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )  
    """

    SQL_equipos = """
        CREATE TABLE equipos (
            id INTEGER NOT NULL,
            serial VARCHAR(100) NOT NULL UNIQUE,
            tipos_equipos_id INT NOT NULL,
            bolivar_marron BOOLEAN NOT NULL,
            estado_actual_id INT NOT NULL,
            area_trabajo_id INT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (tipos_equipos_id) REFERENCES tipos_equipos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (estado_actual_id) REFERENCES estados(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (area_trabajo_id) REFERENCES areas_trabajo(id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
    """

    SQL_componentes = """
        CREATE TABLE componentes(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            componente_id INTEGER NOT NULL,
            uso INTEGER NOT NULL DEFAULT 0,
            dañados INTEGER NOT NULL,
            almacen INTEGER NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (componente_id) REFERENCES tipos_equipos(id) ON DELETE RESTRICT ON UPDATE CASCADE 
        )  
    """

    SQL_caracteristicas = """
        CREATE TABLE caracteristicas(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )  
    """

    SQL_componentes_caracteristicas = """
        CREATE TABLE componentes_has_caracteristicas(
            id INTEGER NOT NULL, 
            componente_id INTEGER NOT NULL,
            caracteristica_id INTEGER NOT NULL,
            value VARCHAR(200) NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (componente_id) REFERENCES componentes(id) ON DELETE UPDATE ON UPDATE CASCADE,
            FOREIGN KEY (caracteristica_id) REFERENCES caracteristicas(id) ON DELETE UPDATE ON UPDATE CASCADE
        )  
    """

    SQL_componentes_equipos = """
        CREATE TABLE componentes_has_equipos(
            id INTEGER NOT NULL, 
            componente_id INTEGER NOT NULL,
            equipo_id INTEGER NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (componente_id) REFERENCES componentes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE RESTRICT ON UPDATE CASCADE
        )  
    """

    SQL_tablas = """
        CREATE TABLE tablas(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_campos_tablas = """
        CREATE TABLE campos_tablas(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            numero_caracteres INTEGER NOT NULL, 
            descripcion VARCHAR(200),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_tablas_campos_tablas = """
        CREATE TABLE tablas_has_campos_tablas(
            id INTEGER NOT NULL, 
            tablas_id INTEGER NOT NULL,
            campos_id INTEGER NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (tablas_id) REFERENCES tablas(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (campos_id) REFERENCES campos_tablas(id) ON DELETE RESTRICT ON UPDATE CASCADE
        )
    """

    SQL_registros = """
        CREATE TABLE registros(
            id INTEGER NOT NULL, 
            campo_tablas_id INTEGER NOT NULL,
            value VARCHAR(1000) NOT NULL,
            numero_registro INTEGER NOT NULL,
            fecha_creacion DATETIME NOT NULL,
            fecha_actualizacion DATETIME NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (campo_tablas_id) REFERENCES tablas_has_campos_tablas(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """

    try:
        conexion.cursor.execute(SQL_tablaEquipos)
        conexion.cursor.execute(SQL_estados)
        conexion.cursor.execute(SQL_areasTrabajo)
        conexion.cursor.execute(SQL_tipoRegistro)
        conexion.cursor.execute(SQL_equipos)
        conexion.cursor.execute(SQL_componentes)
        conexion.cursor.execute(SQL_caracteristicas)
        conexion.cursor.execute(SQL_componentes_caracteristicas)
        conexion.cursor.execute(SQL_componentes_equipos)
        conexion.cursor.execute(SQL_tablas)
        conexion.cursor.execute(SQL_campos_tablas)
        conexion.cursor.execute(SQL_tablas_campos_tablas)
        conexion.cursor.execute(SQL_registros)
        conexion.cerrar()
        titulo = "Crear Tablas"
        message = "Se creo todas las tablas de la base de datos"
        messagebox.showinfo(titulo, message)
    except Exception as ex:
        print(ex)
        titulo = "Crear Tablas"
        message = "La tabla ya esta creada"
        messagebox.showerror(titulo, message)
