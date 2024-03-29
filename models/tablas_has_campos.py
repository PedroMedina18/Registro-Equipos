from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox

class Tablas_has_Campos():

    def create(tablas=0, campos=0):
        conexion =ConexionDB()
        
        sql_create='''
            INSERT INTO tablas_has_campos_tablas (tablas_id, campos_id)
            VALUES(?, ?)
        '''

        try:
            conexion.cursor.execute(sql_create, [int(tablas), int(campos)])
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "La tabla tablas_has_campos_tablas no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
    
    def delete(id):
        conexion=ConexionDB()

        sql='''
            DELETE FROM tablas_has_campos_tablas
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

    def list(id_tabla=0):
        conexion=ConexionDB()

        lista = []
        sql='''
            SELECT 
                tc.id, 
                ca_ta.nombre, 
                ca_ta.numero_caracteres,
                tc.campos_id AS campos_id
            FROM tablas_has_campos_tablas AS tc
            INNER JOIN tablas AS ta ON tc.tablas_id = ta.id
            INNER JOIN campos_tablas AS ca_ta ON tc.campos_id = ca_ta.id
            WHERE tc.tablas_id = ?;
        '''
        try:
            conexion.cursor.execute(sql, [int(id_tabla)])
            lista=conexion.cursor.fetchall()
            
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return lista
