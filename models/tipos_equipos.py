from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString, comprobacionBoolean
from tkinter import messagebox
from config import TITULO_CAMPOS


class TipoEquipos:

    def create(nombre="", marca="", descripcion="", modelo="", equipo_componente=None):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)
        comprobacionMarca = comprobacionString(marca, 100)
        comprobacionModelo = comprobacionString(modelo, 100)
        comprobarEquipo_componente = comprobacionBoolean(equipo_componente)
        comprobacionDescripcion = comprobacionString(descripcion, 500, False)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        if not comprobacionMarca["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Marca {comprobacionMarca["message"]}'
            )
            return None

        if not comprobacionModelo["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Modelo {comprobacionModelo["message"]}'
            )
            return None

        if not comprobarEquipo_componente["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f'Campo Tipo de Registro {comprobarEquipo_componente["message"]}',
            )
            return None

        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None

        sql = """
            INSERT INTO tipos_equipos (nombre, marca, modelo, descripcion, equipo_componente)
            VALUES(?, ?, ?, ?, ?)
        """
        try:
            conexion.cursor.execute(
                sql,
                (
                    str(nombre),
                    str(marca),
                    str(modelo),
                    str(descripcion),
                    int(equipo_componente),
                ),
            )
        except Exception as error:
            print(error)
            titulo = "Conexion al registro"
            message = "La tabla tipo de equipos no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)
        finally:
            conexion.cerrar()

    def update(
        nombre="", marca="", descripcion="", modelo="", equipo_componente=None, id=0
    ):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)
        comprobacionMarca = comprobacionString(marca, 100)
        comprobacionModelo = comprobacionString(modelo, 100)
        comprobarEquipo_componente = comprobacionBoolean(equipo_componente)
        comprobacionDescripcion = comprobacionString(descripcion, 500, False)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        if not comprobacionMarca["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Marca {comprobacionMarca["message"]}'
            )
            return None

        if not comprobacionModelo["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Marca {comprobacionModelo["message"]}'
            )
            return None

        if not comprobarEquipo_componente["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f'Campo Tipo de Registro {comprobarEquipo_componente["message"]}',
            )
            return None

        if not comprobacionDescripcion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Descripción {comprobacionDescripcion["message"]}'
            )
            return None

        sql = """
            UPDATE tipos_equipos
            SET nombre=?, marca=?, modelo=?, descripcion=?, equipo_componente=?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(
                sql,
                (
                    str(nombre),
                    str(marca),
                    str(modelo),
                    str(descripcion),
                    int(equipo_componente),
                    int(id),
                ),
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
            DELETE FROM tipos_equipos
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

    def list(equipo_componente=None):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT id, nombre, marca, modelo, equipo_componente, descripcion FROM tipos_equipos ORDER BY id ASC;
        """
        if equipo_componente==True:
            sql = """
                SELECT 
                    id, 
                    nombre, 
                    marca, 
                    modelo, 
                    equipo_componente, 
                    descripcion 
                FROM 
                    tipos_equipos 
                WHERE equipo_componente=1
                ORDER BY id ASC;
            """

        if equipo_componente==False:
            sql = """
                SELECT 
                    id, 
                    nombre, 
                    marca, 
                    modelo, 
                    equipo_componente, 
                    descripcion 
                FROM 
                    tipos_equipos 
                WHERE equipo_componente=0
                ORDER BY id ASC;
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
