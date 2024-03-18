from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS

class Estados():

    def create(nombre="", descripcion=""):
        conexion =ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 200, False)

        if(not comprobacionNombre["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}')
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}')
            return None

        sql='''
            INSERT INTO estados (nombre, descripcion)
            VALUES(?, ?)
        '''

        try:
            conexion.cursor.execute(sql, (str(nombre), str(descripcion)))
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "La tabla estaoos no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()


    def update(nombre="", descripcion="", id=0):
        conexion=ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 200, False)
        
        if(not comprobacionNombre["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}')
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}')
            return None

        sql='''
            UPDATE estados
            SET nombre=?, descripcion=?
            WHERE id = ?
        '''

        try:
            conexion.cursor.execute(sql, (str(nombre), str(descripcion), int(id)))
        except Exception as error:
            print(error)
            titulo = "Edicion de datos"
            message= "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def delete(id):
        conexion=ConexionDB()

        sql='''
            Delete FROM estados
            WHERE id = ?;
        '''

        try:
            conexion.cursor.execute(sql, [int(id)])
        except:
            titulo = "Eliminar Datos"
            message= "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def list():
        conexion=ConexionDB()

        lista = []
        sql='''
            SELECT * FROM estados
        '''

        try:
            conexion.cursor.execute(sql)
            lista=conexion.cursor.fetchall()
            
        except:
            titulo = "Conexion al registro"
            message= "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return lista




# CREATE TABLE equipos (
#     id INT PRIMARY KEY,
#     serial VARCHAR(100) NOT NULL,
#     tipos_equipos INT,
#     bolivar_marron BOOLEAN,
#     estado_actual INT,
#     area_trabajo INT,
#     FOREIGN KEY (tipos_equipos) REFERENCES tipos_equipos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (estado_actual) REFERENCES estados(id) ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (area_trabajo) REFERENCES areas_trabajos(id) ON DELETE RESTRICT ON UPDATE CASCADE
# );

# SELECT * FROM nombre_tabla
# ORDER BY id ASC;