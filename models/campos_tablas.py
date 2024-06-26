from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS, MESSAGE_DELETE
from util.util_error import controlError

class Campos_Tabla:

    def create(nombre="", descripcion="", caracteres=0):
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
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla campos_tabla no esta creada en la base de datos",
                messageUnique="El valor del campo nombre debe ser unico"
            )
        finally:
            conexion.cerrar()

    def update(nombre="", descripcion="", caracteres=0, id=0):
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
            conexion.cursor.execute(sql, (str(nombre.capitalize()), str(descripcion), int(caracteres), int(id)),)
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
                messageUnique="El valor del campo nombre debe ser unico"
            )
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM campos_tablas
            WHERE id = ?;
        """

        sql_comprobacion="""
            SELECT id FROM tablas_has_campos_tablas WHERE campos_id = ?
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
            SELECT * FROM campos_tablas ORDER BY id ASC;
        """

        if ordenador["campo"] and ordenador["order"]:
            sql=f'''
                SELECT * FROM campos_tablas ORDER BY {ordenador["campo"]} {ordenador["order"]};
            '''

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla campos_tablas en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
