from .conexion import ConexionDB
from util.comprobacionCampos import comprobacionString, comprobacionBoolean
from tkinter import messagebox
from config import TITULO_CAMPOS
from util.util_error import controlError
from .componentes_has_equipos import Componentes_has_Equipos
from .componentes import Componentes

class Equipos:

    def create(serial="", tipos_equipos_id=0, bolivar_marron=None, estado_actual_id=0, area_trabajo_id=0, componentes=[]):
        conexion = ConexionDB()
        comprobacionSerial = comprobacionString(serial, 100)
        comprobarUbicacion = comprobacionBoolean(bolivar_marron)

        if not comprobacionSerial["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Serial {comprobacionSerial["message"]}'
            )
            return None

        if not comprobarUbicacion["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS,
                f'Campo ubicación {comprobarUbicacion["message"]}',
            )
            return None

        sql_equipo = """
            INSERT INTO equipos (serial, tipos_equipos_id, bolivar_marron, estado_actual_id, area_trabajo_id)
            VALUES(?, ?, ?, ?, ?)
        """

        sql_componente_equipo = """
            INSERT INTO componentes_has_equipos (componente_id, equipo_id)
            VALUES(?, ?)
        """

        try:
            conexion.cursor.execute(sql_equipo, (str(serial), int(tipos_equipos_id), int(bolivar_marron), int(estado_actual_id), int(area_trabajo_id)))
            ultimo_registro_equipo = conexion.cursor.lastrowid

            for componente in componentes:
                Componentes.sumarUsados(int(componente))
                conexion.cursor.execute(sql_componente_equipo, (int(componente), int(ultimo_registro_equipo)))

            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="La tabla equipos no esta creada en la base de datos",
                messageUnique="El valor del campo serial debe ser unico"
            )
            return False
        finally:
            conexion.cerrar()

    def update(serial="", tipos_equipos_id=0, bolivar_marron=bool, estado_actual_id=0, area_trabajo_id=0, id=0, componentes=[]):
        conexion = ConexionDB()
        comprobacionSerial = comprobacionString(serial, 100)

        if not comprobacionSerial["status"]:
            messagebox.showwarning(
                TITULO_CAMPOS, f'Campo Serial {comprobacionSerial["message"]}'
            )
            return None

        
        sql = """
            UPDATE equipos
            SET 
                serial=?, 
                tipos_equipos_id=?, 
                bolivar_marron=?, 
                estado_actual_id=?, 
                area_trabajo_id=?
            WHERE id = ?
        """
        sql_componente_equipo = """
            INSERT INTO componentes_has_equipos (componente_id, equipo_id)
            VALUES(?, ?)
        """

        try:
            conexion.cursor.execute(sql, (str(serial), int(tipos_equipos_id), bool(bolivar_marron), int(estado_actual_id), int(area_trabajo_id), int(id)))

            for componente in componentes:
                Componentes.sumarUsados(int(componente))
                conexion.cursor.execute(sql_componente_equipo, [int(componente), int(id)])
            return True
        except Exception as error:
            controlError(
                error,
                titleTable="Edicion de datos",
                messageTable="No se a podido editar el registro",
            )
            return False
        finally:
            conexion.cerrar()

    def delete(id):
        conexion = ConexionDB()

        sql = """
            DELETE FROM equipos
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

    def list(id=0):
        conexion = ConexionDB()

        lista = []
        sql = """
            SELECT 
                equi.id,
                equi.serial,
                tip.nombre,
                equi.bolivar_marron,
                es.nombre,
                art.nombre
            FROM equipos AS equi 
            INNER JOIN estados AS es ON equi.estado_actual_id=es.id
            INNER JOIN areas_trabajo AS art ON equi.area_trabajo_id=art.id
            INNER JOIN tipos_equipos AS tip ON equi.tipos_equipos_id=tip.id
            ORDER BY equi.id ASC;
        """

        if id>0:
            sql = """
            SELECT 
                equi.id,
                equi.serial,
                equi.tipos_equipos_id,
                tip.nombre,
                equi.bolivar_marron,
                equi.estado_actual_id,
                es.nombre,
                equi.area_trabajo_id,
                art.nombre
            FROM equipos AS equi 
            INNER JOIN estados AS es ON equi.estado_actual_id=es.id
            INNER JOIN areas_trabajo AS art ON equi.area_trabajo_id=art.id
            INNER JOIN tipos_equipos AS tip ON equi.tipos_equipos_id=tip.id
            WHERE equi.id=?;
        """
            
        try:
            if id>0:
                conexion.cursor.execute(sql, [id])
                lista = conexion.cursor.fetchall()
                lista = [tupla for tupla in lista]
                componentes= Componentes_has_Equipos.list(id_equipo=lista[0][0])
                lista.append(componentes)
            else:
                conexion.cursor.execute(sql)
                lista = conexion.cursor.fetchall()

        except Exception as error:
            print(error)
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla equipos en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista

    def filter(estado=0, ubicacion=0, tipo_equipo=0, area_trabajo=0):
        conexion = ConexionDB()
        lista = []
        sql_general='''
        SELECT 
            equi.id,
            equi.serial,
            tip.nombre AS tipo_equipo,
            equi.bolivar_marron,
            es.nombre AS estado,
            art.nombre AS area_trabajo
        FROM equipos AS equi 
        INNER JOIN estados AS es ON equi.estado_actual_id=es.id
        INNER JOIN areas_trabajo AS art ON equi.area_trabajo_id=art.id
        INNER JOIN tipos_equipos AS tip ON equi.tipos_equipos_id=tip.id
        '''
        contador=0
        if estado>0 or ubicacion>0 or tipo_equipo>0 or area_trabajo>0:
            sql_general=sql_general + "WHERE"

            if estado>0:
                sql_general=sql_general + f" equi.estado_actual_id={int(estado)}"
                contador=contador+1
            if ubicacion>0:
                if contador>=1:
                    sql_general=sql_general + " AND"
                tipo_ubicacion = 0 if ubicacion==1 else 1
                sql_general=sql_general + f" equi.bolivar_marron={tipo_ubicacion}"
                contador=contador+1
            if tipo_equipo>0:
                if contador>=1:
                    sql_general=sql_general + " AND"
                sql_general=sql_general + f" equi.tipos_equipos_id={int(tipo_equipo)}"
                contador=contador+1
            if area_trabajo>0:
                if contador>=1:
                    sql_general=sql_general + " AND"
                sql_general=sql_general + f" equi.area_trabajo_id={int(area_trabajo)}"
                contador=contador+1
        try:
            
            conexion.cursor.execute(sql_general)
            lista = conexion.cursor.fetchall()

        except Exception as error:
            controlError(
                error,
                titleTable="Conexion al registro",
                messageTable="Crea la tabla equipos en la base de datos"
            )
        finally:
            conexion.cerrar()
        return lista
