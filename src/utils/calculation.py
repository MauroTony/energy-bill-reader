def converte_coordenadas(area):
    """
    Converte coordenadas x,y do referencial do opencv para o referencial do camelot.

    Parameters
    ----------
    area : dict
        Sistema de referência de entrada.
    Returns
    -------
    list
        Sistema de referência de saída.
    """
    return [f"{int(area['x'] / 4.216346154)},{int((2475 - area['y']) / 4.274611399) + 8},{int(area['x_final'] / 4.216346154)},{int((2475 - area['y_final']) / 4.274611399)}"]
