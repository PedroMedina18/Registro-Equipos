from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS

class Estados():

    def create(componente_id=0, dañados=0, almacen=0, caracteristicas=[]):
        conexion =ConexionDB()
        
        sql_create='''
            INSERT INTO componentes (componente_id, uso, dañados, almacen)
            VALUES(?, 0, ?, ?)
        '''

        try:
            conexion.cursor.execute(sql_create)
            ultimo_registro=conexion.cursor.lastrowid()
            print(ultimo_registro)
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "La tabla componentes no esta creada en la base de datos"
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
            DELETE FROM componentes
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
            SELECT * FROM estados ORDER BY id ASC;
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
