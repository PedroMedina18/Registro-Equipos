from tkinter import messagebox
from config import (
    TITULO_CAMPOS
    
)

def controlError(error, messageTable=None, titleTable=None, messageNumber=None, titleNumber=None, messageRange=None, titleRange=None, messageSelection=None, titleSelection=None,):
    if "no such table" in str(error):
        titulo= "Conexion al registro" if not titleTable else str(titleTable)
        mensage= "Crea la tabla en la base de datos" if not messageTable  else str(messageTable)
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
