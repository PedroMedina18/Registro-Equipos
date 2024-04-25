from .conexion import ConexionDB
from tkinter import messagebox
from util.util_error import controlError
from .componentes_has_caracteristicas import Componentes_has_Caracteristicas

class Componentes_has_Equipos:

    
    def list(id_equipo=0):
        conexion = ConexionDB()

        lista_componentes = []
        sql = """
            SELECT 
                ce.id AS id_componentes_has_equipos,
                com.id AS id_componete,
                com.nombre
            FROM componentes_has_equipos AS ce
            INNER JOIN componentes AS com ON ce.componente_id = com.id
            INNER JOIN equipos AS equi ON ce.equipo_id = equi.id
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