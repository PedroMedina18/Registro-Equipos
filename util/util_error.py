from tkinter import messagebox
from config import (
    TITULO_CAMPOS
    
)

def controlError(error, messageTable=None, titleTable=None, messageUnique=None, titleUnique=None, messageNumber=None, titleNumber=None, messageRange=None, titleRange=None, messageSelection=None, titleSelection=None, errors=[]):
    if len(errors)>0:
        for data in errors:
            if data["error"]==error:
                titulo= data["title"]
                mensage= data["mesage"]
                messagebox.showwarning(titulo, mensage)
                return
    
    if "no such table" in str(error):
        titulo= "Conexion al registro" if not titleTable else str(titleTable)
        mensage= "Crea la tabla en la base de datos" if not messageTable  else str(messageTable)
        messagebox.showwarning(titulo, mensage)

    elif "UNIQUE constraint failed" in str(error):
        titulo= "Campo Unico" if not titleUnique else str(titleUnique)
        mensage= "Valor de campo repetido. Debe ser Unico" if not messageUnique  else str(messageUnique)
        messagebox.showwarning(titulo, mensage)

    elif "expected floating-point number but got" in str(error):
        titulo= "Tipo de dato Incorrepto" if not titleNumber else str(titleNumber)
        mensage= "Solo se permiten números en los campos" if not messageNumber  else str(messageNumber)
        messagebox.showwarning(titulo, mensage)

    elif "list index out of range" == error:
        titulo= "Error de selección" if not titleRange else str(titleRange)
        mensage= "No hay mas valores para agregar" if not messageRange  else str(messageRange)
        messagebox.showwarning(titulo, mensage)

    elif "string index out of range" == error:
        titulo= "Seleccion de campos" if not titleSelection else str(titleSelection)
        mensage= "No ha seleccionado ningun registro" if not messageSelection  else str(messageSelection)
        messagebox.showwarning(titulo, mensage)
    else:
        titulo="Error Desconocido"
        message=error
        messagebox.showerror(titulo, message)
