from datetime import datetime, date

def list_values(list):
    lista = []
    for element in list:
        lista.append(element[1])

    return lista


def verificacion_campos(list_principal, list_secundaria):
    list = []
    for tupla_principal in list_principal[0]:
        exists = False
        for tupla_secundaria in list_secundaria[0]:
            if tupla_principal[list_principal[1]] == tupla_secundaria[list_secundaria[1]]:
                exists = True
        if not exists:
            list.append(tupla_principal[1])

    return list


def determinar_campo(list_campos_sql, campo_select):

    result = False
    for tupla in list_campos_sql:
        if tupla[1] == campo_select:
            return tupla

    if not result:
        return None



def determinar_indice(list_campos_sql, id_campo_select=0, nombre=None):
    for index, tupla in enumerate(list_campos_sql):
        if id_campo_select>0:
            if tupla[0] == int(id_campo_select):
                return index
        if nombre:
            if tupla[1] == str(nombre):
                return index


def organizador_registros(tuples_list):
    grouped_tuples = {}

    for t in tuples_list:
        if t[0] not in grouped_tuples:
            grouped_tuples[t[0]] = []
        grouped_tuples[t[0]].append(t)

    return grouped_tuples


def asignar_valores(object_campos, group_tuplas):
    list_registros = []
    for key, value in group_tuplas.items():
        
        valores_registros = object_campos.copy()
        valores_registros["id"] = key

        for index, registro in enumerate(value, start=1):
            if index == 1:
                valores_registros["fecha_creacion"] = formatoFecha(registro[2])
            valores_registros["fecha_actualizacion"] = formatoFecha(registro[3])
            valores_registros[f"{registro[5]}"] = registro[1]

        list_registros.append(valores_registros)

    return list_registros

def formatoFecha(fecha):
    formatoDateTime="%Y-%m-%d %H:%M:%S.%f"
    fechaStr=datetime.strptime(fecha, formatoDateTime)
    stringFecha=f"{fechaStr.day:02}/{fechaStr.month:02}/{fechaStr.year}    {fechaStr.hour if fechaStr.hour <= 12 else fechaStr.hour - 12}:{fechaStr.minute:02} {'am' if fechaStr.hour <= 12 else 'pm'}"
    return stringFecha

def Fecha(fecha):
    formatoDateTime="%Y-%m-%d %H:%M:%S"
    fechaStr=datetime.strptime(fecha, formatoDateTime)
    stringFecha=f"{fechaStr.day:02}/{fechaStr.month:02}/{fechaStr.year}"
    return stringFecha

def validate_date(date_str):
    formats = ["%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            fecha=datetime.strptime(str(date_str), fmt)
            return fecha
        except ValueError:
            pass
    return False