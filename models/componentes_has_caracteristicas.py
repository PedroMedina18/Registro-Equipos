from .conexion import ConexionDB
from tkinter import messagebox
from util.util_error import controlError

class Componentes_has_Caracteristicas:

    def create(componente_id=0, caracteristica_id=0, value=None):
        conexion = ConexionDB()
        sql_componente_caracteristica='''
            INSERT INTO componentes_has_caracteristicas (componente_id, caracteristica_id, value)
            VALUES(?, ?, ?)
        '''
        try:
            conexion.cursor.execute(sql_componente_caracteristica, (int(componente_id), int(caracteristica_id), str(value)))
            
        except Exception as error:
            print(error)
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla componentes no esta creada en la base de datos",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
        finally:
            conexion.cerrar()

    def update(id=0, value=None):
        conexion = ConexionDB()
        sql_componente_caracteristica='''
            UPDATE componentes_has_caracteristicas 
            SET value = ?
            WHERE id = ?
        '''

        try:
            conexion.cursor.execute(sql_componente_caracteristica, [str(value), int(id)])
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
        finally:
            conexion.cerrar()

    def list(id_componente=0):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT 
                comca.id, 
                com.nombre,
                ca.id,
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

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM componentes_has_caracteristicas
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