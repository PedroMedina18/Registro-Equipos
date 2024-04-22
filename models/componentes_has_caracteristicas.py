from .conexion import ConexionDB
from tkinter import messagebox
from util.util_error import controlError

class Componentes_has_Caracteristicas:

    def list(id_componente=0):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT 
                comca.id, 
                com.nombre,
                ca.nombre,
                comca.value
            FROM componentes_has_caracteristicas AS comca
            INNER JOIN componentes AS com ON comca.componente_id = com.id
            INNER JOIN caracteristicas AS ca ON comca.caracteristica_id = ca.id
            WHERE com.id = ?;
        """

        try:
            conexion.cursor.execute(sql, [int(id_componente)])
            lista = conexion.cursor.fetchall()
            lista = [list(tupla) for tupla in lista]
    
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla equipos en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista