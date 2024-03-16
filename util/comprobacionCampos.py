def comprobacionString(string, numeroCaracteresMaximo, obligatorio=True):
    if not isinstance(string, str):
        return {"status":False, "message":"no es un string. Campo Invalido"}
    
    if not len(string) <=numeroCaracteresMaximo:
        return {"status":False, "message":"número de caracteres excede la cantidad permitidad"}
    
    if obligatorio and len(string)==0:
        return {"status":False, "message":"es Obligatorio"}
    
    return {"status":True, "message":"Campo Valido"}