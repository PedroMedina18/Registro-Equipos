from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError

class Componentes:

    def create(nombre="", componente_id=0, dañados=0, almacen=0, caracteristicas=[]):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        sql_componente = """
            INSERT INTO componentes (nombre, componente_id, uso, dañados, almacen)
            VALUES(?, ?, 0, ?, ?)
        """

        sql_componente_caracteristica='''
            INSERT INTO componentes_has_caracteristicas (componente_id, caracteristica_id, value)
            VALUES(?, ?, ?)
        '''

        try:
            conexion.cursor.execute(sql_componente, (str(nombre).capitalize(), int(componente_id), int(dañados), int(almacen)))
            ultimo_registro_component = conexion.cursor.lastrowid
            
            for caracteristica_component in caracteristicas:
                conexion.cursor.execute(sql_componente_caracteristica, (int(ultimo_registro_component), int(caracteristica_component["id"]), caracteristica_component["value"]))
        
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla componentes no esta creada en la base de datos",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
        finally:
            conexion.cerrar()

    def update(nombre="", descripcion="", id=0):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)
        comprobacionDescripcion = comprobacionString(descripcion, 200, False)

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
            UPDATE estados
            SET nombre=?, descripcion=?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(sql, (str(nombre).capitalize(), str(descripcion), int(id)))
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
            DELETE FROM componentes
            WHERE id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id)])
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar Datos",
                messageTable="No se pudo eliminar el registro"
            )
        finally:
            conexion.cerrar()

    def list(id_componente=0):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT 
                id,
                nombre,
                uso,
                dañados,
                almacen 
            FROM componentes ORDER BY id ASC;
        """

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla componentes en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
