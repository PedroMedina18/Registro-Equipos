from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString, comprobacionBoolean
from tkinter import messagebox
from config import TITULO_CAMPOS, MESSAGE_DELETE
from util.util_error import controlError

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
                    str(nombre).capitalize(),
                    str(marca).capitalize(),
                    str(modelo).capitalize(),
                    str(descripcion),
                    int(equipo_componente),
                ),
            )
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla tipos_equipos no esta creada en la base de datos",
            )
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
                    str(nombre).capitalize(),
                    str(marca).capitalize(),
                    str(modelo).capitalize(),
                    str(descripcion),
                    int(equipo_componente),
                    int(id),
                ),
            )
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
            )
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM tipos_equipos
            WHERE id = ?;
        """

        sql_comprobacion_equipo="""
            SELECT id FROM equipos WHERE tipos_equipos_id = ?
        """

        sql_comprobacion_componente="""
            SELECT id FROM componentes WHERE componente_id = ?
        """

        try:
            conexion.cursor.execute(sql_comprobacion_equipo, [int(id)])
            comprobacion_equipo= conexion.cursor.fetchall()
            conexion.cursor.execute(sql_comprobacion_componente, [int(id)])
            comprobacion_componente= conexion.cursor.fetchall()
            if len(comprobacion_equipo)>0 or len(comprobacion_componente)>0:
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

    def list(equipo_componente=None, ordenador={"campo":None, "order":None}):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT id, nombre, marca, modelo, equipo_componente, descripcion FROM tipos_equipos
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
            """
        if ordenador["campo"] and ordenador["order"]:
            sql = sql + f'''
                ORDER BY {ordenador["campo"]} {ordenador["order"]};
            '''
        else:
            sql = sql + "ORDER BY id ASC;"

        try:
            conexion.cursor.execute(sql)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla estados en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
