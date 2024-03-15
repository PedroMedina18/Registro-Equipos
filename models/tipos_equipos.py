from .conexion import ConexionDB
from util.comprobacionCampos import  comprobacionString
from tkinter import messagebox


class TipoEquipos():

    def create(self, nombre="", marca="", descripcion=""):
        conexion =ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionMarca=comprobacionString(marca, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 500, False)
        self.tituloCampos="Comprobación de Campos"

        if(not comprobacionNombre["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionNombre["message"])
            return None
        
        if(not comprobacionMarca["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionMarca["message"])
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionDescripcion["message"])
            return None

        sql=f'''
            INSERT INTO tipos_equipos (nombre, marca, descripcion)
            VALUES(%s, %s, %s)
        '''

        try:
            conexion.cursor.execute(sql, [str(nombre), str(marca), str(descripcion)])
            conexion.cerrar()
        
        except:
            titulo = "Conexion al registro"
            message= "La tabla peliculas no esta creada en la base de datos"
            messagebox.showwarning(titulo, message)

    def update(self, nombre="", marca="", descripcion="", id=0):
        conexion=ConexionDB()
        comprobacionNombre=comprobacionString(nombre, 100)
        comprobacionMarca=comprobacionString(marca, 100)
        comprobacionDescripcion=comprobacionString(descripcion, 500, False)
        
        if(not comprobacionNombre["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionNombre["message"])
            return None
        
        if(not comprobacionMarca["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionMarca["message"])
            return None
        
        if(not comprobacionDescripcion["status"]):
            messagebox.showwarning(self.tituloCampos, comprobacionDescripcion["message"])
            return None

        sql=f'''
            UPDATE tipos_equipos
            SET nombre= '{nombre}', marca='{marca}', descripcion='{descripcion}'
            WHERE id = {id}

        '''

        try:
            conexion.cursor.execute(sql)
            conexion.cerrar()
        except:
            titulo = "Edicion de datos"
            message= "No se a podido editar el registro"
            messagebox.showwarning(titulo, message)

    def delete(self, id=0):
        conexion=ConexionDB()

        sql=f'''
            Delete FROM tipos_equipos
            WHERE id = %s;
        '''

        try:
            conexion.cursor.execute(sql, [int(id)])
            conexion.cerrar()
        except:
            titulo = "Eliminar Datos"
            message= "No se pudo eliminar el registro"
            messagebox.showwarning(titulo, message)

    def list():
        conexion=ConexionDB()

        lista = []
        sql='''
            SELECT * FROM tipos_equipos
        '''

        try:
            conexion.cursor.execute(sql)
            lista=conexion.cursor.fetchall()
            conexion.cerrar()
        except:
            titulo = "Conexion al registro"
            message= "Crea la tabla en la base de datos"
            messagebox.showwarning(titulo, message)

        return lista