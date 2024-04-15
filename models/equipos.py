from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS


class Equipos:

    def create(serial="", tipos_equipos_id=0, bolivar_marron=bool, estado_actual_id=0, area_trabajo_id=0):
        conexion = ConexionDB()
        comprobacionSerial = comprobacionString(serial, 100)

        if not comprobacionSerial["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Serial {comprobacionSerial["message"]}'
            )
            return None

        sql = """
            INSERT INTO equipos (serial, tipos_equipos_id, bolivar_marron, estado_actual_id, area_trabajo_id)
            VALUES(?, ?, ?, ?, ?)
        """

        try:
            conexion.cursor.execute(sql, (str(serial), int(tipos_equipos_id), bool(bolivar_marron), int(estado_actual_id), int(area_trabajo_id)))
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message = "La tabla equipos no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def update(serial="", tipos_equipos_id=0, bolivar_marron=bool, estado_actual_id=0, area_trabajo_id=0, id=0):
        conexion = ConexionDB()
        comprobacionSerial = comprobacionString(serial, 100)

        if not comprobacionSerial["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Serial {comprobacionSerial["message"]}'
            )
            return None

        
        sql = """
            UPDATE equipos
            SET 
                serial=?, 
                tipos_equipos_id=?, 
                bolivar_marron=?, 
                estado_actual_id=?, 
                area_trabajo_id=?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(sql, (str(serial), int(tipos_equipos_id), bool(bolivar_marron), int(estado_actual_id), int(area_trabajo_id), int(id)))
        except Exception as error:
            print(error)
            titulo = "Edicion de datos"
            message = "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM equipos
            WHERE id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id)])
        except:
            titulo = "Eliminar Datos"
            message = "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def list():
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT * FROM equipos ORDER BY id ASC;
        """

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except:
            titulo = "Conexion al registro"
            message = "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
        return lista
