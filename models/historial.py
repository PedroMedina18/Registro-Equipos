from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError
from util.list_values import validate_date
class Historial:

    def create(tipo_registro_id=0, fecha="",equipo_id=0, descripcion=""):
        conexion = ConexionDB()
        comprobacionDescripcion = comprobacionString(descripcion, 3000, True)
        fecha_registro = validate_date(fecha)
        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None
        
        if not fecha_registro:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Formato de fecha incorrecto debe ser d/m/a o d-m-a'
            )
            return None
        sql = """
            INSERT INTO historial (tipo_registro_id, equipo_id, fecha, descripcion)
            VALUES(?, ?, ?, ?)
        """

        try:
            conexion.cursor.execute(sql, (int(tipo_registro_id), int(equipo_id), fecha_registro, str(descripcion)))
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al historial",
                messageTable="La tabla tipos_registros no esta creada en la base de datos"
            )
        finally:
            conexion.cerrar()

    def update(id_registro=0, tipo_registro_id=0, descripcion="", fecha=""):
        conexion = ConexionDB()
        comprobacionDescripcion = comprobacionString(descripcion, 3000)
        fecha_registro = validate_date(fecha)
        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None
        if not fecha_registro:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Formato de fecha incorrecto deve d/m/a o d-m-a'
            )
            return None

        sql = """
            UPDATE historial
            SET 
                tipo_registro_id=?,
                fecha=?, 
                descripcion=?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(sql, (int(tipo_registro_id), fecha_registro, str(descripcion), int(id_registro)))
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
            )
            return False
        finally:
            conexion.cerrar()

    def delete_registro(id_historial=0):
        conexion = ConexionDB()

        sql = """
            DELETE FROM historial
            WHERE id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id_historial)])
            return True
        except:
            titulo = "Eliminar Datos"
            message = "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def delete_equipo(id_equipo=0):
        conexion = ConexionDB()

        sql = """
            DELETE FROM historial
            WHERE equipo_id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id_equipo)])
            return True
        except:
            titulo = "Eliminar Datos"
            message = "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()
    
    def list(equipo_id):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT 
                hi.id,
                tire.nombre,
                hi.fecha,
                hi.descripcion
            FROM historial AS hi
            LEFT JOIN tipos_registros AS tire ON hi.tipo_registro_id=tire.id
            WHERE equipo_id = ?
            ORDER BY fecha ASC;
        """

        try:
            conexion.cursor.execute(sql, [int(equipo_id)])
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla tipos_registros en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
