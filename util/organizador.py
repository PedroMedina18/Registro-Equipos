# Necesito que realice la siguiente función en python te voy a pasar como argumento una lista de tuplas, un número de índice y un valor que seria ASC o DESC lo que quiero hacer es organizar esa lista de tuplas dependiendo de que posición se pase como argumento ejemplo si las tuplas tienen 4 índices y se pasa como argumento el índice 2 ese es el que se va a usar como referencia para organizar esa lista también se debe tener en cuenta si va ser ascendente=ASC o descentente=DESC, como último detalle como valores de las tuplas pueden ver string o numer

def sort_tuples(tuples_list, index, order):
    
    def sort_key(t):
        
        return t[index]

    # Sort the list of tuples using the sort_key function and the specified order
    if order == 'ASC':
        tuples_list.sort(key=sort_key)
    elif order == 'DESC':
        tuples_list.sort(key=sort_key, reverse=True)
    else:
        raise ValueError("Invalid sort order. Must be either 'ASC' or 'DESC'.")

    return tuples_list



