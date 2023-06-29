import re

def ordena_areas(areas):
    for pagina in areas:
        pagina['areas'] = sorted(pagina['areas'], key=lambda d: d['y'])
    return areas

def validar_mes_ano(variavel):
    padrao = r'^(0[1-9]|1[0-2])\/(19\d\d|20[0-9]\d|3000)$'
    resultado = re.match(padrao, variavel)
    return resultado is not None

def validar_data(variavel):
    padrao = r'^(0[1-9]|1\d|2\d|3[01])\/(0[1-9]|1[0-2])\/(19\d\d|20[0-9]\d|3000)$'
    resultado = re.match(padrao, variavel)
    return resultado is not None


def validar_remuneracao(remuneracao):
    try:
        value = remuneracao.strip()
        value = value.replace(".", "")
        value = value.replace(",", ".")
        value = float(value)
        return True
    except:
        return False

def validar_cnpj(cnpj):
    # Remover caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verificar se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verificar se todos os dígitos do CNPJ são iguais
    if len(set(cnpj)) == 1:
        return False

    # Calcular o primeiro dígito verificador
    soma = 0
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * pesos[i]
    digito1 = (soma % 11)
    if digito1 < 2:
        digito1 = 0
    else:
        digito1 = 11 - digito1

    # Calcular o segundo dígito verificador
    soma = 0
    pesos.insert(0, 6)
    for i in range(13):
        soma += int(cnpj[i]) * pesos[i]
    digito2 = (soma % 11)
    if digito2 < 2:
        digito2 = 0
    else:
        digito2 = 11 - digito2

    # Verificar se os dígitos verificadores estão corretos
    if int(cnpj[-2]) != digito1 or int(cnpj[-1]) != digito2:
        return False
    return True
