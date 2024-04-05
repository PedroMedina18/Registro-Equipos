from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.numero_unico import numero_unico
from util.list_values import organizador_registros, asignar_valores
from datetime import datetime


class Registros:
    def create(campos=[]):
        conexion = ConexionDB()
        numero_registro = numero_unico()
        fecha_hora_actual = datetime.now()
        for campo in campos:
            comprobacionValue = comprobacionString(campo["value"], campo["caracteres"])

            if not comprobacionValue["status"]:
                messagebox.showwarning(
                    TITULO_CAMPOS,
                    f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}',
                )
                return None

        sql = """
            INSERT INTO registros (campo_tablas_id, value, numero_registro, fecha_creacion, fecha_actualizacion)
            VALUES(?, ?, ?, ?, ?)
        """

        try:
            for campo in campos:
                conexion.cursor.execute(
                    sql,
                    [
                        campo["id"],
                        campo["value"],
                        numero_registro,
                        fecha_hora_actual,
                        fecha_hora_actual,
                    ],
                )
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message = "La tabla registro no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def update(campos=[]):
        conexion = ConexionDB()

        for campo in campos:
            comprobacionValue = comprobacionString(campo["value"], campo["caracteres"])

            if not comprobacionValue["status"]:
                messagebox.showwarning(
                    TITULO_CAMPOS,
                    f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}',
                )
                return None

        sql = """
            UPDATE campos_tablas
            SET value=?
            WHERE id = ?
        """
        try:
            for campo in campos:
                conexion.cursor.execute(sql, [campo["value"], campo["id"]])
        except Exception as error:
            print(error)
            titulo = "Edicion de datos"
            message = "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def delete(numero_registro):
        conexion = ConexionDB()

        sql = """
            DELETE FROM registros
            WHERE numero_registro = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(numero_registro)])
        except:
            titulo = "Eliminar Datos"
            message = "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def list(id_tabla, campos):
        conexion = ConexionDB()

        sql_registros = """
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
        """
        
        try:
            
            conexion.cursor.execute(sql_registros, [id_tabla])
            registros = conexion.cursor.fetchall()

            campos_tabla={keys:None for keys in campos}
            
            grupo_registros = organizador_registros(registros)
           
            lista_registros = asignar_valores(campos_tabla, grupo_registros )
            
            return lista_registros

        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message = "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return []
