from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError
from datetime import datetime

class Historial:

    def create(tipo_registro_id=0, equipo_id=0, descripcion=""):
        conexion = ConexionDB()
        comprobacionDescripcion = comprobacionString(descripcion, 3000)
        fecha_hora_actual = datetime.now()
        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None

        sql = """
            INSERT INTO historial (tipo_registro_id, equipo_id, fecha, descripcion)
            VALUES(?, ?, ?, ?)
        """

        try:
            conexion.cursor.execute(sql, (int(tipo_registro_id), int(equipo_id), fecha_hora_actual, str(descripcion)))
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al historial",
                messageTable="La tabla tipos_registros no esta creada en la base de datos"
            )
        finally:
            conexion.cerrar()


    def list(equipo_id):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT * FROM historial 
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
