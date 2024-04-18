from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS


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
            print(error)
            titulo = "Conexion al registro"
            message = "La tabla componentes no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
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
            print(error)
            titulo = "Edicion de datos"
            message = "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)
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
            SELECT * FROM estados ORDER BY id ASC;
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
