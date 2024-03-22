def list_values(list):
    lista=[]
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