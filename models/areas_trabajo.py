from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS, MESSAGE_DELETE
from util.util_error import controlError

class AreasTrabajo:

    def create(nombre="", descripcion=""):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)
        comprobacionDescripcion = comprobacionString(descripcion, 300, False)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None

        sql = """
            INSERT INTO areas_trabajo (nombre, descripcion)
            VALUES(?, ?)
        """

        try:
            conexion.cursor.execute(sql, (str(nombre).capitalize(), str(descripcion)))
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla areas_trabajo no esta creada en la base de datos",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
        finally:
            conexion.cerrar()

    def update(nombre="", descripcion="", id=0):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)
        comprobacionDescripcion = comprobacionString(descripcion, 300, False)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None

        sql = """
            UPDATE areas_trabajo
            SET nombre=?, descripcion=?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(sql, (str(nombre).capitalize(), str(descripcion), int(id)))
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM areas_trabajo
            WHERE id = ?;
        """

        sql_comprobacion="""
            SELECT id FROM equipos WHERE area_trabajo_id = ?
        """

        try:
            conexion.cursor.execute(sql_comprobacion, [int(id)])
            comprobacion= conexion.cursor.fetchall()
            if len(comprobacion)>0:
                messagebox.showerror("Eliminar Registro", MESSAGE_DELETE)
                return None

            conexion.cursor.execute(sql, [int(id)])
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar Datos",
                messageTable="No se pudo eliminar el registro"
            )
        finally:
            conexion.cerrar()

    def list(ordenador={"campo":None, "order":None}):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT * FROM areas_trabajo ORDER BY id ASC;
        """

        if ordenador["campo"] and ordenador["order"]:
            sql=f'''
                SELECT * FROM areas_trabajo ORDER BY {ordenador["campo"]} {ordenador["order"]};
            '''

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla areas_ trabajo en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
