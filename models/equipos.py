from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString, comprobacionBoolean
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError

class Equipos:

    def create(serial="", tipos_equipos_id=0, bolivar_marron=None, estado_actual_id=0, area_trabajo_id=0, componentes=[]):
        conexion = ConexionDB()
        comprobacionSerial = comprobacionString(serial, 100)
        comprobarUbicacion = comprobacionBoolean(bolivar_marron)

        if not comprobacionSerial["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Serial {comprobacionSerial["message"]}'
            )
            return None

        if not comprobarUbicacion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f'Campo ubicación {comprobarUbicacion["message"]}',
            )
            return None

        sql_equipo = """
            INSERT INTO equipos (serial, tipos_equipos_id, bolivar_marron, estado_actual_id, area_trabajo_id)
            VALUES(?, ?, ?, ?, ?)
        """

        sql_componente_equipo = """
            INSERT INTO componentes_has_equipos (componente_id, equipo_id)
            VALUES(?, ?)
        """

        try:
            conexion.cursor.execute(sql_equipo, (str(serial), int(tipos_equipos_id), int(bolivar_marron), int(estado_actual_id), int(area_trabajo_id)))
            ultimo_registro_equipo = conexion.cursor.lastrowid

            for componente in componentes:
                conexion.cursor.execute(sql_componente_equipo, (int(componente), int(ultimo_registro_equipo)))

            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla equipos no esta creada en la base de datos",
                messageUnique="El valor del campo serial debe ser Unico"
            )
            return False
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
            SELECT 
                equi.id,
                equi.serial,
                tip.nombre,
                equi.bolivar_marron,
                es.nombre,
                art.nombre
            FROM equipos AS equi 
            INNER JOIN estados AS es ON equi.estado_actual_id=es.id
            INNER JOIN areas_trabajo AS art ON equi.area_trabajo_id=art.id
            INNER JOIN tipos_equipos AS tip ON equi.tipos_equipos_id=tip.id
            ORDER BY equi.id ASC;
        """

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla equipos en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
