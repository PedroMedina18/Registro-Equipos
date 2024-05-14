from .conexion import ConexionDB
from tkinter import messagebox
from util.util_error import controlError
from .componentes_has_caracteristicas import Componentes_has_Caracteristicas
from .componentes import Componentes

class Componentes_has_Equipos:

    def list(id_equipo=0):
        conexion = ConexionDB()

        lista_componentes = []
        sql = """
            SELECT 
                ce.id AS id_componentes_has_equipos,
                com.id AS id_componente,
                com.nombre,
                tir.nombre,
                tir.marca,
                tir.modelo,
                tir.descripcion
            FROM componentes_has_equipos AS ce
            INNER JOIN equipos AS equi ON ce.equipo_id = equi.id
            INNER JOIN componentes AS com ON ce.componente_id = com.id
            LEFT JOIN tipos_equipos AS tir ON com.componente_id = tir.id
            WHERE equi.id = ?;
        """
        try:
            conexion.cursor.execute(sql, [int(id_equipo)])
            lista_componentes = conexion.cursor.fetchall()
            lista_componentes = [list(tupla) for tupla in lista_componentes]

            for componente in lista_componentes:
                caracteristicas=Componentes_has_Caracteristicas.list(id_componente=componente[1])
                componente.append(caracteristicas)
            
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Error al consultar la tabla componentes_has_equipos"
            )
        finally:
            conexion.cerrar()

        return lista_componentes
    
    def delete(id_componente_has_equipo, id_componente):
        conexion = ConexionDB()

        sql = """
            DELETE FROM componentes_has_equipos
            WHERE id = ?;
        """

        try:
            Componentes.restarUsados(int(id_componente))
            conexion.cursor.execute(sql, [int(id_componente_has_equipo)])
        except Exception as error:
            print(error)
            controlError(
                error,
                titleTable="Eliminar Datos",
                messageTable="No se pudo eliminar el registro"
            )
        finally:
            conexion.cerrar()
    
    def delete_equipo(id_equipo):
        conexion = ConexionDB()

        sql = """
            DELETE FROM componentes_has_equipos
            WHERE equipo_id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id_equipo)])
        except Exception as error:
            controlError(
                error,
                titleTable="Eliminar Datos",
                messageTable="No se pudo eliminar el registro"
            )
        finally:
            conexion.cerrar()