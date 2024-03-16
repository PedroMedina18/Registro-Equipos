from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS

class TipoEquipos():

    def create(nombre="", marca="", descripcion=""):
        conexion =ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionMarca=comprobacionString(marca, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 500, False)

        if(not comprobacionNombre["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}')
            return None
        
        if(not comprobacionMarca["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Marca {comprobacionMarca["message"]}')
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}')
            return None

        sql='''
            INSERT INTO tipos_equipos (nombre, marca, descripcion)
            VALUES(?, ?, ?)
        '''

        try:
            conexion.cursor.execute(sql, (str(nombre), str(marca), str(descripcion)))
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "La tabla tipo de equipos no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()


    def update(nombre="", marca="", descripcion="", id=0):
        conexion=ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionMarca=comprobacionString(marca, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 500, False)
        
        if(not comprobacionNombre["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}')
            return None
        
        if(not comprobacionMarca["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Marca {comprobacionMarca["message"]}')
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}')
            return None

        sql='''
            UPDATE tipos_equipos
            SET nombre=?, marca=?, descripcion=?
            WHERE id = ?
        '''

        try:
            conexion.cursor.execute(sql, (str(nombre), str(marca), str(descripcion), int(id)))
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
            Delete FROM tipos_equipos
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
            SELECT * FROM tipos_equipos
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
