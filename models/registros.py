from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from util.numero_unico import numero_unico
from util.list_values import organizador_registros, asignar_valores
from util.util_error import controlError
from config import TITULO_CAMPOS
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
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla registros no esta creada en la base de datos",
            )
        finally:
            conexion.cerrar()

    def update(campos=[],  numero_registro=0):
        conexion = ConexionDB()
        fecha_hora_actual = datetime.now()

        for campo in campos:
            comprobacionValue = comprobacionString(campo["value"], campo["caracteres"])

            if not comprobacionValue["status"]:
                messagebox.showwarning(
                    TITULO_CAMPOS,
                    f'Campo {campo["nombre"].capitalize()} {comprobacionValue["message"]}',
                )
                return None

        sql_update = """
            UPDATE registros
            SET value=?, fecha_actualizacion=?
            WHERE numero_registro=? AND campo_tablas_id=?
        """
        sql_create = """
            INSERT INTO registros (campo_tablas_id, value, numero_registro, fecha_creacion, fecha_actualizacion)
            VALUES(?, ?, ?, ?, ?)
        """
        try:
            for campo in campos:
                if campo["type"]=="update":
                    conexion.cursor.execute(sql_update, [campo["value"], fecha_hora_actual, numero_registro, campo["id"]])
                elif campo["type"]=="create":
                    conexion.cursor.execute(sql_create, [campo["id"], campo["value"], numero_registro, fecha_hora_actual, fecha_hora_actual])

        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
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
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar Datos",
                messageTable="No se pudo eliminar el registro"
            )
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

            campos_tabla={keys:"" for keys in campos}
            
            grupo_registros = organizador_registros(registros)

            lista_registros = asignar_valores(campos_tabla, grupo_registros )
            
            return lista_registros

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla registros en la base de datos"
            )
        finally:
            conexion.cerrar()
        return []
