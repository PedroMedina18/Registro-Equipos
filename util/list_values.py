def list_values(list):
    lista = []
    for element in list:
        lista.append(element[1])

    return lista


def verificacion_campos(list_principal, list_secundaria):
    list = []
    for tupla_principal in list_principal:
        exists = False
        for tupla_secundaria in list_secundaria:
            if tupla_principal[0] == tupla_secundaria[3]:
                exists = True
        if not exists:
            list.append(tupla_principal[1])

    return list


def determinar_campo(list_campos_sql, list_campos_select, value_select):
    campo_select = list_campos_select[value_select]

    result = False
    for tupla in list_campos_sql:
        if tupla[1] == campo_select:
            return tupla

    if not result:
        return None


def organizador_registros(tuples_list):
    grouped_tuples = {}

    for t in tuples_list:
        if t[0] not in grouped_tuples:
            grouped_tuples[t[0]] = []
        grouped_tuples[t[0]].append(t)

    return grouped_tuples


def asignar_valores(object_campos, group_tuplas):
    
    registros = []
    for key, value in group_tuplas.items():

        campos = object_campos
        campos["id"] = key

        for index, registro in enumerate(value, start=1):
            if index==1:
                campos["fecha_creacion"] = registro[2]
                campos["fecha_actualizacion"] = registro[3]
            campos[f"{registro[5]}"] = registro[1]

        registros.append(campos)

    return registros
