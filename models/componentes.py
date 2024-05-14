from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString
from tkinter import messagebox
from config import TITULO_CAMPOS, MESSAGE_DELETE
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

        sql_componente_caracteristica='''
            INSERT INTO componentes_has_caracteristicas (componente_id, caracteristica_id, value)
            VALUES(?, ?, ?)
        '''
        try:
            conexion.cursor.execute(sql_componente, (str(nombre).capitalize(), int(componente_id), int(dañados), int(almacen)))
            ultimo_registro_component = conexion.cursor.lastrowid

            for caracteristica_component in caracteristicas:
                conexion.cursor.execute(sql_componente_caracteristica, (int(ultimo_registro_component), int(caracteristica_component["id_caracteristica"]), caracteristica_component["value"]))
            
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla componentes no esta creada en la base de datos",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
            return False
        finally:
            conexion.cerrar()

    def update(nombre="", componente_id=0, dañados=0, almacen=0, caracteristicas=[], id=0):
        conexion = ConexionDB()
        comprobacionNombre = comprobacionString(nombre, 100)

        if not comprobacionNombre["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Nombre {comprobacionNombre["message"]}'
            )
            return None

        sql_componente_update = """
            UPDATE componentes
            SET nombre = ?, componente_id = ?, dañados = ?, almacen = ?
            WHERE id = ?
        """

        sql_componente_caracteristica='''
            INSERT INTO componentes_has_caracteristicas (componente_id, caracteristica_id, value)
            VALUES(?, ?, ?)
        '''
        sql_componente_caracteristica_update='''
            UPDATE componentes_has_caracteristicas 
            SET value = ?
            WHERE id = ?
        '''

        try:
            conexion.cursor.execute(sql_componente_update, [str(nombre).capitalize(), int(componente_id), int(dañados), int(almacen), int(id)])
            
            for caracteristica in caracteristicas:
                if caracteristica["tipo"]=="new":
                    conexion.cursor.execute(sql_componente_caracteristica, [int(id), int(caracteristica["id_caracteristica"]), caracteristica["value"]])
                
                if caracteristica["tipo"]=="update":
                    conexion.cursor.execute(sql_componente_caracteristica_update, [caracteristica["value"], int(caracteristica["id_caracteristica_component"])])
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
                messageUnique="El valor del campo Nombre debe ser Unico"
            )
            return False
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM componentes
            WHERE id = ?;
        """
        sql_comprobacion="""
            SELECT id FROM componentes_has_equipos WHERE componente_id = ?
        """

        try:
            conexion.cursor.execute(sql_comprobacion, [int(id)])
            comprobacion = conexion.cursor.fetchall()
            if len(comprobacion) > 0:
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

    def list(id_componente=0, almacen=False, ordenador={"campo":None, "order":None}):
        conexion = ConexionDB()

        sql = """
            SELECT 
                com.id,
                com.nombre,
                com.almacen,
                com.dañados,
                com.uso,
                tir.id,
                tir.nombre,
                tir.marca,
                tir.modelo,
                tir.descripcion
            FROM componentes AS com
            LEFT JOIN tipos_equipos AS tir ON com.componente_id = tir.id
        """
        
        if ordenador["campo"] and ordenador["order"]:
            sql = sql + f'''
                ORDER BY {ordenador["campo"]} {ordenador["order"]};
            '''
        else:
            sql = sql + "ORDER BY com.id ASC;"


        if id_componente>0 and not almacen:
            sql = """
            SELECT 
                com.id,
                com.nombre,
                com.almacen,
                com.dañados,
                com.uso,
                tir.id,
                tir.nombre,
                tir.marca,
                tir.modelo,
                tir.descripcion
            FROM componentes AS com
            LEFT JOIN tipos_equipos AS tir ON com.componente_id = tir.id
            WHERE com.id = ?;
            """

        if almacen:
            sql = """
            SELECT 
                com.id,
                com.nombre,
                com.almacen,
                com.dañados,
                com.uso,
                tir.id,
                tir.nombre,
                tir.marca,
                tir.modelo,
                tir.descripcion
            FROM componentes AS com
            LEFT JOIN tipos_equipos AS tir ON com.componente_id = tir.id
            WHERE com.almacen > 0 
            """

            if ordenador["campo"] and ordenador["order"]:
                sql = sql + f'''
                    ORDER BY {ordenador["campo"]} {ordenador["order"]};
                '''
            else:
                sql = sql + "ORDER BY com.id ASC;"

        try:
            if id_componente>0 and not almacen:
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

    def consultAlmacen(id_componente=0):
        conexion = ConexionDB()
        componente=None
        sql = """
            SELECT 
                id,
                nombre,
                almacen
            FROM componentes 
            WHERE id=?;
        """
        try:
            conexion.cursor.execute(sql, [int(id_componente)])
            componente=conexion.cursor.fetchall()
            if componente[0][2]<=0:
                title="Componentes"
                message=f"No quedan {componente[0][2]} en el almacen. Por favor verificar"
                messagebox.showwarning(title, message)
                return False
            else:
                return componente[0]

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla componentes en la base de datos"
            )
        finally:
            conexion.cerrar()

    def sumarUsados(id_componente=0):
        conexion = ConexionDB()
        componente = None
        sql_component = """
            SELECT 
                id,
                nombre,
                almacen,
                uso
            FROM componentes 
            WHERE id=?;
        """
        sql_update = """
            UPDATE componentes
            SET almacen = ?, uso = ?
            WHERE id = ?
        """
        try:
            conexion.cursor.execute(sql_component, [int(id_componente)])
            componente = conexion.cursor.fetchall()

            conexion.cursor.execute(sql_update, [int(componente[0][2]-1), int(componente[0][3]+1), int(id_componente)])
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla componentes en la base de datos"
            )
            return False
        finally:
            conexion.cerrar()
    
    def restarUsados(id_componente=0):
        conexion = ConexionDB()
        componente=None
        sql_component = """
            SELECT 
                id,
                nombre,
                almacen,
                uso
            FROM componentes 
            WHERE id=?;
        """
        sql_update = """
            UPDATE componentes
            SET almacen = ?, uso = ?
            WHERE id = ?
        """
        try:
            conexion.cursor.execute(sql_component, [int(id_componente)])
            componente=conexion.cursor.fetchall()
            if not int(componente[0][3]) <= 0:
                conexion.cursor.execute(sql_update, [int(componente[0][2]+1), int(componente[0][3]-1), int(id_componente)])
                return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla componentes en la base de datos"
            )
            return False
        finally:
            conexion.cerrar()
    
