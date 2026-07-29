import urllib.parse


def gerar_link_google_maps(origem, destinos, retorno=""):
    """
    Gera um link do Google Maps contendo:

    - Origem
    - Waypoints
    - Destino Final

    Se existir um endereço de retorno,
    ele será utilizado como destino final.

    Caso contrário,
    o último destino da lista será o destino final.
    """

    destinos = [
        endereco.strip()
        for endereco in destinos
        if str(endereco).strip()
    ]

    if not origem:
        return None

    if len(destinos) == 0:
        return None

    if retorno.strip():

        destino_final = retorno.strip()

        waypoints_lista = destinos

    else:

        destino_final = destinos[-1]

        waypoints_lista = destinos[:-1]

    origem = urllib.parse.quote(origem)

    destino_final = urllib.parse.quote(destino_final)

    if len(waypoints_lista) == 0:

        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={origem}"
            f"&destination={destino_final}"
            "&travelmode=driving"
        )

    waypoints = "|".join(
        urllib.parse.quote(endereco)
        for endereco in waypoints_lista
    )

    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origem}"
        f"&destination={destino_final}"
        f"&waypoints={waypoints}"
        "&travelmode=driving"
    )
