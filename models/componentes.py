from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError
from models.componentes_has_caracteristicas import Componentes_has_Caracteristicas


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
        ultimo_registro_component = None
        try:
            conexion.cursor.execute(sql_componente, (str(nombre).capitalize(), int(componente_id), int(dañados), int(almacen)))
            ultimo_registro_component = conexion.cursor.lastrowid
            
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla componentes no esta creada en la base de datos",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
            return False
        finally:
            for caracteristica_component in caracteristicas:
                Componentes_has_Caracteristicas.create(componente_id=int(ultimo_registro_component), caracteristica_id=int(caracteristica_component["id_caracteristica"]), value=caracteristica_component["value"])
            conexion.cerrar()

    def update(nombre="", componente_id=0, dañados=0, almacen=0, caracteristicas=[], id=0):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        sql_componente = """
            UPDATE componentes
            SET nombre = ?, componente_id = ?, dañados = ?, almacen = ?
            WHERE id = ?
        """

        try:
            conexion.cursor.execute(sql_componente, [str(nombre).capitalize(), int(componente_id), int(dañados), int(almacen), int(id)])
            
            for caracteristica in caracteristicas:
                if caracteristica["tipo"]=="new":
                    Componentes_has_Caracteristicas.create(componente_id=int(id), caracteristica_id=int(caracteristica["id_caracteristica"]), value=caracteristica["value"])
                else:
                    Componentes_has_Caracteristicas.update(id=int(caracteristica["id_caracteristica_component"]), value=caracteristica["value"])


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

        sql = """
            SELECT 
                id,
                nombre,
                uso,
                dañados,
                almacen 
            FROM componentes ORDER BY id ASC;
        """

        if id_componente>0:
            sql = """
            SELECT 
                com.id,
                com.nombre,
                com.uso,
                com.dañados,
                com.almacen,
                tir.id,
                tir.nombre,
                tir.marca,
                tir.modelo,
                tir.descripcion
            FROM componentes AS com
            LEFT JOIN tipos_equipos AS tir ON com.componente_id = tir.id
            WHERE com.id = ?;
            """
            

        try:
            if id_componente>0:
                conexion.cursor.execute(sql, [int(id_componente)])
                componente=conexion.cursor.fetchall()
                caracteristicas = Componentes_has_Caracteristicas.list(id_componente=componente[0][0])
                data_componente=[item for item in componente[0]]
                data_componente.append(caracteristicas)
                return data_componente
                
            else:
                conexion.cursor.execute(sql)
                lista = conexion.cursor.fetchall()
                return lista

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla componentes en la base de datos"
            )
        finally:
            conexion.cerrar()
