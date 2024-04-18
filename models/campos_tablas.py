from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS


class Campos_Tabla:

    def create(nombre="", descripcion="", caracteres=0):
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

        if caracteres >= 1000:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f"Campo Caracteres. El campo no puede superar los 1000 unidades",
            )
            return None

        if caracteres <= 0:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f"Campo Caracteres. El campo no puede ser enor o igual a cero",
            )
            return None

        sql = """
            INSERT INTO campos_tablas (nombre, descripcion, numero_caracteres)
            VALUES(?, ?, ?)
        """

        try:
            conexion.cursor.execute(
                sql, (str(nombre).capitalize(), str(descripcion), int(caracteres))
            )
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message = "La tabla campos_tablas no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def update(nombre="", descripcion="", caracteres=0, id=0):
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

        if caracteres >= 1000:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f"Campo Caracteres. El campo no puede superar los 1000 unidades",
            )
            return None

        if caracteres <= 0:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f"Campo Caracteres. El campo no puede ser enor o igual a cero",
            )
            return None

        sql = """
            UPDATE campos_tablas
            SET nombre=?, descripcion=?, numero_caracteres=?
            WHERE id = ?
        """
        try:
            conexion.cursor.execute(
                sql,
                (str(nombre.capitalize()), str(descripcion), int(caracteres), int(id)),
            )
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
            DELETE FROM campos_tablas
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
            SELECT * FROM campos_tablas ORDER BY id ASC;
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
