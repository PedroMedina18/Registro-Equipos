from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.numero_unico import numero_unico


class Registros():
    def create(campos=[]):
        conexion =ConexionDB()
        numero_registro=numero_unico()
        
        for campo in campos:
            comprobacionValue=comprobacionString(campo["value"], campo["caracteres"])

            if(not comprobacionValue["status"]):
                messagebox.showwarning(TITULO_CAMPOS, f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}')
                return None

        sql='''
            INSERT INTO registros (campo_tablas_id, value, numero_registro)
            VALUES(?, ?, ?)
        '''

        try:
            for campo in campos:
                conexion.cursor.execute(sql, [campo["id"], campo["value"], numero_registro])
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "La tabla registro no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()


    def update(campos=[]):
        conexion=ConexionDB()
        
        for campo in campos:
            comprobacionValue=comprobacionString(campo["value"], campo["caracteres"])

            if(not comprobacionValue["status"]):
                messagebox.showwarning(TITULO_CAMPOS, f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}')
                return None

        sql='''
            UPDATE campos_tablas
            SET value=?
            WHERE id = ?
        '''
        try:
            for campo in campos:
                conexion.cursor.execute(sql, [campo["value"], campo["id"]])
        except Exception as error:
            print(error)
            titulo = "Edicion de datos"
            message= "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def delete(numero_registro):
        conexion=ConexionDB()

        sql='''
            DELETE FROM registros
            WHERE numero_registro = ?;
        '''

        try:
            conexion.cursor.execute(sql, [int(numero_registro)])
        except:
            titulo = "Eliminar Datos"
            message= "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def list(id_tabla):
        conexion=ConexionDB()

        lista = []
        sql='''
            SELECT * FROM registros AS re
            INNER JOIN  tablas_has_campos_tablas AS tct ON re.campo_tablas_id=tct.id
            WHERE tct.tablas_id=?;
        '''

        try:
            conexion.cursor.execute(sql, [id_tabla])
            lista=conexion.cursor.fetchall()
            
        except:
            titulo = "Conexion al registro"
            message= "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return lista
