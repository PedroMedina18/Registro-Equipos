from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.numero_unico import numero_unico
from datetime import datetime

class Registros():
    def create(campos=[]):
        conexion =ConexionDB()
        numero_registro=numero_unico()
        fecha_hora_actual=datetime.now()
        for campo in campos:
            comprobacionValue=comprobacionString(campo["value"], campo["caracteres"])

            if(not comprobacionValue["status"]):
                messagebox.showwarning(TITULO_CAMPOS, f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}')
                return None

        sql='''
            INSERT INTO registros (campo_tablas_id, value, numero_registro, fecha_creacion, fecha_actualizacion)
            VALUES(?, ?, ?, ?, ?)
        '''

        try:
            for campo in campos:
                conexion.cursor.execute(sql, [campo["id"], campo["value"], numero_registro, fecha_hora_actual, fecha_hora_actual])
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
        sql_registros='''
            SELECT 
                re.numero_registro, 
                re.value, 
                re.fecha_creacion, 
                re.fecha_actualizacion,
                ct.id,
                ct.nombre
            FROM registros AS re
            INNER JOIN tablas_has_campos_tablas AS tct ON re.campo_tablas_id=tct.id
            LEFT JOIN campos_tablas AS ct ON tct.campos_id=ct.id
            WHERE tct.tablas_id=?
            ORDER BY re.numero_registro ASC;
        '''
        sql_campos='''
            SELECT 
                tc.id, 
                ca_ta.nombre, 
                tc.campos_id AS campos_id
            FROM tablas_has_campos_tablas AS tc
            INNER JOIN campos_tablas AS ca_ta ON tc.campos_id = ca_ta.id
            WHERE tc.tablas_id = ?;
        '''

        try:
            conexion.cursor.execute(sql_campos, [id_tabla])
            campos=conexion.cursor.fetchall()
            print(f"{"_"<"_"*10}")
            conexion.cursor.execute(sql_registros, [id_tabla])
            results=conexion.cursor.fetchall()
            lista=[]
            object={}
            print(results)
            
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message= "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return lista
