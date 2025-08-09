import network.api as api


def is_of_interest(materia):
    ementa = materia["Ementa"].lower()
    return "calçada" in ementa \
        or "calcada" in ementa \
        or "passeio" in ementa \
        or "cicli" in ementa \
        or "ciclo" in ementa \
        or "pedestre" in ementa \
        or "veículo" in ementa \
        or "veiculo" in ementa \
        or "onibus" in ementa \
        or "ônibus" in ementa \
        or "transporte" in ementa \
        or "estufa" in ementa \
        or "gee" in ementa \
        or "clima" in ementa \
        or "14.933" in ementa \
        or "16.802" in ementa \
        or "18.225" in ementa


def is_following(materia):
    sigla = materia["Sigla"]
    numero = materia["Numero"]
    ano = materia["Ano"]
    return (sigla == "PL" and numero == 438 and ano == 2024) or \
        (sigla == "PL" and numero == 476 and ano == 2023) or \
        (sigla == "PL" and numero == 17 and ano == 2025)


        # Legislação de interesse:
# Lei nº 14.933, de 5 de junho de 2009 - lei original de metas ambientais do transporte urbano
# Lei nº 16.802, de 17 de janeiro de 2018 - alteração na lei de metas ambientais do transporte urbano
# Lei nº 16.802, de 17 de janeiro de 2018 - alteração na lei de metas ambientais do transporte urbano
# LEI 18.225 de 15/01/2025 - PL da fumaça do M Leite (altera novamente a lei de metas ambientais do transporte urbano)

def find_materias(data):
    jsonResponse = api.get_materias_eventos(data)

    jsonResult = []
    for materia in jsonResponse:

        priority = -1
        if is_following(materia):
            priority = 0
        elif is_of_interest(materia):
            priority = 1

        if priority >= 0:
            autores = ""
            for autor in materia["Autores"]:
                autores += f'{autor["Nome"]}, '
            autores = autores.removesuffix(", ")

            eventos = ""
            for evento in materia["Eventos"]:
                eventos += f'{evento["Data"]} - {evento["Descricao"]}\n'

            jsonEvento = {
                "sigla": materia["Sigla"],
                "numero": materia["Numero"],
                "ano": materia["Ano"],
                "autores": autores,
                "ementa": materia["Ementa"],
                "priority": priority,
                "eventos": eventos,
            }
            jsonResult.append(jsonEvento)

    # data = json.loads(jsonResult)
    sorted_data = sorted(jsonResult, key=lambda x: x['priority'])

    return sorted_data


def get_eventos_for_date_pretty(date, show_eventos):
    json = find_materias(date)

    response = ""
    for materia in json:
        printable = ""

        if materia["priority"] == 0:
            printable += "****** SEGUINDO ******\n"

        printable += (f'Materia: {materia["sigla"]}-{materia["numero"]}/{materia["ano"]}\n'
                     f'Ementa: {materia["ementa"]}\n'
                     f'Autores: {materia["autores"]}\n')

        codigo_materia = ""

        if materia["sigla"] == "PL":
            codigo_materia = "1"
        elif materia["sigla"] == "PDL":
            codigo_materia = "2"
        elif materia["sigla"] == "PLO":
            codigo_materia = "4"
        elif materia["sigla"] == "RDS":
            codigo_materia = "13"

        if show_eventos:
            printable += f'Eventos: \n{materia["eventos"]}'

        if codigo_materia != "":
            printable += f'Link: https://splegisconsulta.saopaulo.sp.leg.br/Pesquisa/DetailsDetalhado?' \
                         f'COD_MTRA_LEGL={codigo_materia}' \
                         f'&COD_PCSS_CMSP={materia["numero"]}&ANO_PCSS_CMSP={materia["ano"]}\n'

        response += printable+"\n"

    return response


# text = get_eventos_for_date_pretty(date="2025-04-17", show_eventos=True)
# print(text)

# https://splegisconsulta.saopaulo.sp.leg.br/Pesquisa/DetailsDetalhado?COD_MTRA_LEGL=1&COD_PCSS_CMSP=15&ANO_PCSS_CMSP=2006
# https://splegisconsulta.saopaulo.sp.leg.br/Pesquisa/DetailsDetalhado?COD_MTRA_LEGL=1&COD_PCSS_CMSP=28&ANO_PCSS_CMSP=2011