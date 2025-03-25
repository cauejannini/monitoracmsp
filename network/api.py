from requests import get

# https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx/MateriasEventosJSON?dataPesquisa=2025-03-13

api_url = "https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx"

materias_eventos_endpoint = "/MateriasEventosJSON"


def get_materias_eventos(data):
    url = f"{api_url}{materias_eventos_endpoint}?dataPesquisa={data}"
    response = get(url)
    return response.json()

