import urllib.parse


def gerar_link_google_maps(origem, destinos):
    """
    Gera um link do Google Maps contendo:

    - Origem
    - Waypoints (paradas intermediárias)
    - Destino final

    Parâmetros:
        origem (str): Endereço de partida.
        destinos (list): Lista de endereços.

    Retorna:
        str: URL pronta para abrir no Google Maps.
    """

    # Remove endereços vazios
    destinos = [
        endereco.strip()
        for endereco in destinos
        if str(endereco).strip()
    ]

    if not origem:
        return None

    if len(destinos) == 0:
        return None

    origem = urllib.parse.quote(origem)

    # Apenas um destino
    if len(destinos) == 1:

        destino = urllib.parse.quote(destinos[0])

        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={origem}"
            f"&destination={destino}"
            "&travelmode=driving"
        )

    # Mais de um destino
    destino_final = urllib.parse.quote(destinos[-1])

    waypoints = "|".join(
        urllib.parse.quote(endereco)
        for endereco in destinos[:-1]
    )

    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origem}"
        f"&destination={destino_final}"
        f"&waypoints={waypoints}"
        "&travelmode=driving"
    )
