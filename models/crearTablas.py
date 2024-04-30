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
            descripcion VARCHAR(300),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_areasTrabajo = """
        CREATE TABLE areas_trabajo(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(300),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_tipoRegistro = """
        CREATE TABLE tipo_registro(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(300),
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
            FOREIGN KEY (tipos_equipos_id) REFERENCES tipos_equipos(id) ON DELETE RESTRICT,
            FOREIGN KEY (estado_actual_id) REFERENCES estados(id) ON DELETE RESTRICT,
            FOREIGN KEY (area_trabajo_id) REFERENCES areas_trabajo(id) ON DELETE RESTRICT
        )
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
            descripcion VARCHAR(300),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_componentes_caracteristicas = """
        CREATE TABLE componentes_has_caracteristicas(
            id INTEGER NOT NULL, 
            componente_id INTEGER NOT NULL,
            caracteristica_id INTEGER NOT NULL,
            value VARCHAR(500) NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY (componente_id) REFERENCES componentes(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (caracteristica_id) REFERENCES caracteristicas(id) ON DELETE CASCADE ON UPDATE CASCADE
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
            descripcion VARCHAR(300),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_campos_tablas = """
        CREATE TABLE campos_tablas(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            numero_caracteres INTEGER NOT NULL, 
            descripcion VARCHAR(300),
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

    SQL_tipo_registro = """
        CREATE TABLE tipos_registros(
            id INTEGER NOT NULL, 
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion VARCHAR(300),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_historial = """
        CREATE TABLE historial(
            id INTEGER NOT NULL, 
            tipo_registro_id INTEGER NOT NULL, 
            equipo_id INTEGER NOT NULL, 
            fecha DATETIME NOT NULL,
            descripcion VARCHAR(3000),
            PRIMARY KEY(id AUTOINCREMENT)
        )
    """

    SQL_insert_estados='''
        INSERT INTO estados (nombre, descripcion)
        VALUES(?, ?)
    '''
    estados=[
        ("Dañados", "Equipos que se encuentran Dañados"),
        ("Mantenimiento", "Equipos que se encuentran en mantenimiento en el area de sistemas"),
        ("Uso", "Equipos que se encuentran en uso en su area de trabajo"),
    ]

    SQL_insert_areas_trabajo='''
        INSERT INTO areas_trabajo (nombre, descripcion)
        VALUES(?, ?)
    '''
    areas_trabajo=[
        ("Farmacía", "Area de Farmacía"),
        ("Caja", "Área de Caja"),
        ("Convenio", "Área de Convenio"),
        ("Sistemas", "Área de Sistemas"),
        ("Tesoreria", "Área de Tesoreria"),
        ("Atencion al Cliente", "Área de Atencion al Cliente"),
        ("Equipos Medicos", "Área de Equipos Medicos"),
        ("Gerencia", "Área de Gerencia"),
        ("Sub Gerencia", "Área de la Sub Gerencia"),
        ("Almacen", "Área de Almacen"),
        ("Seguridad", "Área de Seguridad"),
        ("Recursos Humanos", "Área de Recursos Humanos"),
        ("Cuentas por Pagar", "Área de Cuentas por Pagar"),
        ("Cuentas por Cobrar", "Área de Cuentas por Cobrar"),
    ]

    SQL_insert_tablas='''
        INSERT INTO tablas (nombre, descripcion)
        VALUES(?, ?)
    '''
    tablas=[
        ("Contraseñas Computadores", "Tabla con todas las contraseñas de los computadores"),
        ("Contraseñas WI-FI", "Tabla con todas las contraseñas de los puntos de WI-FI"),
        ("Extenciones Telefonicas", "Tabla con las diferentes extsiones de telefono"),
        ("Direcciones IP", "Tabla con las direcciones IP de los computadores"),
    ]

    SQL_insert_tablas='''
        INSERT INTO tipos_registros (nombre, descripcion)
        VALUES(?, ?)
    '''
    tablas=[
        ("Contraseñas Computadores", "Tabla con todas las contraseñas de los computadores"),
        ("Contraseñas WI-FI", "Tabla con todas las contraseñas de los puntos de WI-FI"),
        ("Extenciones Telefonicas", "Tabla con las diferentes extsiones de telefono"),
        ("Direcciones IP", "Tabla con las direcciones IP de los computadores"),
    ]

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
        conexion.cursor.execute(SQL_tipo_registro)
        conexion.cursor.execute(SQL_historial)
        conexion.cursor.executemany(SQL_insert_estados, estados)
        conexion.cursor.executemany(SQL_insert_areas_trabajo, areas_trabajo)
        conexion.cursor.executemany(SQL_insert_tablas, tablas)
        conexion.cerrar()
        titulo = "Crear Tablas"
        message = "Se creo todas las tablas de la base de datos"
        messagebox.showinfo(titulo, message)
    except Exception as ex:
        print(ex)
        titulo = "Crear Tablas"
        message = "La tabla ya esta creada"
        messagebox.showerror(titulo, message)
