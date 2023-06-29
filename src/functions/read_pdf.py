import camelot
import cv2
import numpy as np
from pdf2image import convert_from_path
from utils import converte_coordenadas, ordena_areas, plot_table, validar_mes_ano, validar_remuneracao, validar_cnpj, validar_data
from models import (
    Relacao,
    identification,
    modelos,
    Contributions,
    modelo1,
    modelo2,
    modelo3,
    modelo4,
    modelo5,
    modelo6,
)


class LeitorExtrato:
    def __init__(self, path_file):
        self.path_file = path_file
        self.img_formatada = None
        self.relacoes = []
        self.identificacao = None
        self.areas_tabelas = []
        self.qtd_paginas = None

    def extrair_identificacao(self):
        tables = camelot.read_pdf(
            self.path_file,
            pages="1",
            flavor="stream",
            edge_tol=50,
            # row_tol=10,
            columns=["218,356"],
            table_areas=["21,485,826,453"],
            # strip_text="\n",
        )
        table_df = tables[0].df
        dict_data = table_df.to_dict()
        identificacao = identification(
            nit=(
                dict_data[0][0].split(":")[1]
                if dict_data[0][0].split(":")[1] != ""
                else dict_data[0][0].split("\n")[0]
            ).replace("\n", ""),
            birthDate=(
                dict_data[0][1].split(":")[1]
                if dict_data[0][1].split(":")[1] != ""
                else dict_data[0][1].split("\n")[0]
            ).replace("\n", ""),
            cpf=(
                dict_data[1][0].split(":")[1]
                if dict_data[1][0].split(":")[1] != ""
                else dict_data[1][0].split("\n")[0]
            ).replace("\n", ""),
            name=(
                dict_data[2][0].split(":")[1]
                if dict_data[2][0].split(":")[1] != ""
                else dict_data[2][0].split("\n")[0]
            ).replace("\n", ""),
        )
        self.identificacao = identificacao

    def identifica_tabelas(self):
        pages = convert_from_path(self.path_file, dpi=300)
        self.qtd_paginas = len(pages)

        for pagina in range(1, self.qtd_paginas + 1):
            image = cv2.cvtColor(np.array(pages[pagina - 1]), cv2.COLOR_RGB2BGR)
            img = image[750:2200, 115:3392]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            ultimo_x = -1
            ultimo_y = -100
            areas_pagina = {"pagina": pagina, "areas": []}
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                area = w * h
                if area > 352000:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if x != 0 and x != ultimo_x:
                        x_pdf = x + 119
                        y_pdf = y + 718
                        x_final = x_pdf + w
                        y_final = y_pdf + h
                        ultimo_x = x
                        ultimo_y = y
                        areas_pagina["areas"].append(
                            {
                                "x": x_pdf,
                                "y": y_pdf,
                                "x_final": x_final,
                                "y_final": y_final,
                            }
                        )
            if len(areas_pagina["areas"]) == 0:
                areas_pagina["areas"].append(
                    {"x": 115, "y": 750, "x_final": 3392, "y_final": 2200}
                )
            self.areas_tabelas.append(areas_pagina)

    def extrair_relacoes(self):
        self.areas_tabelas = ordena_areas(self.areas_tabelas)

        for pagina in range(1, self.qtd_paginas + 1):
            areas = self.areas_tabelas[pagina - 1]["areas"]
            for area in areas:
                ref_table_areas = converte_coordenadas(area)
                for modelo in modelos:
                    insere_dados = True
                    tables = camelot.read_pdf(
                        self.path_file,
                        pages=str(pagina),
                        flavor="stream",
                        edge_tol=50,
                        row_tol=10,
                        columns=modelo["colunas"],
                        table_areas=ref_table_areas,
                    )

                    table_df = tables[0].df
                    dict_data = table_df.to_dict()
                    qtd_seq = 0
                    dados = []
                    status_valor = 0  # 0 - Buscando Seq. 1 - Buscando Valor 2 - verificando se tem competencia
                    tabela = {}
                    verifica_competencia = False
                    seq_encontrado = False
                    verifica_competencia_sem_seq = False
                    verifica_competencia_sem_seq_sem_titulo = False

                    ref_table_remuneracoes = ["115,205,285,375,470,554,640,730"]
                    ref_table_contribuicoes = ["96,156,225,322,418,499,559,626,725"]
                    ref_table_contratos = ["120,279,452,573,710"]
                    ref_tables = [ref_table_remuneracoes, ref_table_contribuicoes, ref_table_contratos]

                    for keys, values in dict_data[0].items():
                        if (
                            values == "Competência"
                            and status_valor == 0
                            and qtd_seq == 0
                        ):
                            self.relacoes[-1].update({"remuneracao": True})
                            verifica_competencia_sem_seq = True
                        if validar_mes_ano(values) and status_valor == 0 and qtd_seq == 0:
                            self.relacoes[-1].update({"remuneracao": True})
                            verifica_competencia_sem_seq_sem_titulo = True
                        if values == "Seq.":
                            if status_valor != 0:
                                tabela["remuneracao"] = False
                                dados.append(tabela)
                                tabela = {}
                            qtd_seq += 1
                            status_valor = 1
                            seq_encontrado = True
                            continue
                        if status_valor == 1:
                            tabela["seq"] = values
                            status_valor = 2
                            continue
                        if status_valor == 2:
                            if "Competência" in values:
                                tabela["remuneracao"] = True
                                status_valor = 0
                                dados.append(tabela)
                                verifica_competencia = True
                                tabela = {}
                            continue
                    else:
                        if tabela != {}:
                            tabela["remuneracao"] = False
                            dados.append(tabela)


                    if (verifica_competencia_sem_seq or verifica_competencia_sem_seq_sem_titulo) and qtd_seq > 0:
                        insere_dados = False
                        break
                    if not seq_encontrado and (verifica_competencia_sem_seq or verifica_competencia_sem_seq_sem_titulo):
                        for ref_table in ref_tables:
                            tables_remuneracoes = camelot.read_pdf(
                                self.path_file,
                                pages=str(pagina),
                                flavor="stream",
                                edge_tol=50,
                                row_tol=10,
                                columns=ref_table,
                                table_areas=ref_table_areas,
                            )
                            table_df = tables_remuneracoes[0].df
                            dict_data_remuneracoes = table_df.to_dict()
                            try:
                                if ref_table == ref_table_remuneracoes:
                                    result = self.extrair_remuneracoes(
                                        dict_data_remuneracoes
                                    )
                                elif ref_table == ref_table_contribuicoes:
                                    result = self.extrair_contribuicoes(
                                        dict_data_remuneracoes
                                    )
                                elif ref_table == ref_table_contratos:
                                    result = self.extrair_contratos(
                                        dict_data_remuneracoes
                                    )
                            except Exception as e:
                                print(e)
                                continue
                            verifica_remuneracao = self.relacoes[-1].get("remuneracoes")
                            if verifica_remuneracao is None:
                                self.relacoes[-1].update({"remuneracoes": result})
                            else:
                                verifica_remuneracao.extend(result)
                                self.relacoes[-1].update(
                                    {"remuneracoes": verifica_remuneracao}
                                )
                            break
                        insere_dados = False
                        break
                    if len(dados) > 1 or len(dados) == 0:
                        insere_dados = False
                        break

                    for coluna in range(1, len(dict_data)):
                        row = 0
                        chave_atual = None
                        tabela = {}
                        status_valor = 0  # 0 - Buscando chave. 1 - Buscando Valor 2 - verificando se tem competencia
                        for keys, values in dict_data[coluna].items():
                            if values in modelo["modelo"]:
                                if status_valor != 0:
                                    tabela[chave_atual] = None
                                    dados[row].update(tabela)
                                    tabela = {}
                                if values in dados[0].keys():
                                    continue
                                chave_atual = values
                                status_valor = 1
                                continue
                            if status_valor == 1:
                                tabela[chave_atual] = values
                                dados[row].update(tabela)
                                break
                        else:
                            if status_valor != 0:
                                tabela[chave_atual] = ""
                                dados[row].update(tabela)

                    verifica_modelo = [
                        keys for keys in dados[0].keys() if keys != "remuneracao"
                    ]
                    if verifica_modelo == modelo["modelo"]:
                        dados[0].update({"modelo": modelo["modelo"]})

                        if verifica_competencia:
                            for ref_table in ref_tables:
                                tables_remuneracoes = camelot.read_pdf(
                                    self.path_file,
                                    pages=str(pagina),
                                    flavor="stream",
                                    edge_tol=50,
                                    row_tol=10,
                                    columns=ref_table,
                                    table_areas=ref_table_areas,
                                )

                                table_df = tables_remuneracoes[0].df
                                dict_data_remuneracoes = table_df.to_dict()
                                try:
                                    if ref_table == ref_table_remuneracoes:
                                        result = self.extrair_remuneracoes(
                                            dict_data_remuneracoes
                                        )

                                    elif ref_table == ref_table_contribuicoes:
                                        result = self.extrair_contribuicoes(
                                            dict_data_remuneracoes
                                        )

                                    elif ref_table == ref_table_contratos:
                                        result = self.extrair_contratos(
                                            dict_data_remuneracoes
                                        )
                                except Exception as e:
                                    print(e)
                                    continue
                                dados[0].update({"remuneracoes": result})
                                break
                        break
                    insere_dados = False
                if insere_dados and dados[0] not in self.relacoes:
                    self.relacoes.extend(dados)

    def resultado(self):
        dados_idenficacao = self.identificacao
        dados_relacoes_bruto = self.relacoes
        dados_relacoes_formatado = []

        for dados in dados_relacoes_bruto:
            dados_contribuicoes = []
            if dados.get("remuneracoes"):
                for contribuicao in dados.get("remuneracoes"):
                    value = contribuicao.get("value")
                    if value:
                        value = value.strip()
                        value = value.replace(".", "")
                        value = value.replace(",", ".")
                        value = float(value)
                    else:
                        value = ""
                    competence = contribuicao.get("competencia").strip()

                    contribuicao_formatado = {
                        "competence": competence,
                        "value": value,
                    }
                    if value != "":
                        dados_contribuicoes.append(contribuicao_formatado)

            seq = int(dados.get("seq"))
            origin = dados.get("Origem do Vínculo").replace("\n", " ").strip()
            if dados.get("modelo") == modelo1:
                split_date = dados.get("Data Início Data Fim").split(" ")
                init_date = split_date[0].strip()
                end_date = split_date[1].strip() if len(split_date) > 1 else ""
            elif (
                dados.get("modelo") == modelo2
                or dados.get("modelo") == modelo3
                or dados.get("modelo") == modelo4
                or dados.get("modelo") == modelo5
                or dados.get("modelo") == modelo6
            ):
                init_date = dados.get("Data Início").strip()
                end_date = dados.get("Data Fim").strip()

            dado_formatado = Relacao(
                seq=seq,
                origin=origin,
                initDate=init_date,
                endDate=end_date,
                contributions=dados_contribuicoes,
            )
            dados_relacoes_formatado.append(dado_formatado.dict())
        dados_formatados = dados_idenficacao.dict()

        dados_formatados["relations"] = dados_relacoes_formatado

        return dados_formatados

    @staticmethod
    def extrair_remuneracoes(dict_data):
        contribuicao_coluna1 = []
        contribuicao_coluna2 = []
        contribuicao_coluna3 = []

        modelo_colunas = {
            0: contribuicao_coluna1,
            1: contribuicao_coluna1,
            3: contribuicao_coluna2,
            4: contribuicao_coluna2,
            6: contribuicao_coluna3,
            7: contribuicao_coluna3,
        }
        valida_colunas = {
            "competencia": False,
            "remuneracao": False,
        }
        verifica_linha = 0
        for coluna in dict_data:
            procurando_dados = True
            linhas = 0
            for linha, value in dict_data[coluna].items():
                if coluna in [0, 3, 6]:
                    if value == "" and linha == verifica_linha:
                        verifica_linha += 1
                    if value == "Competência":
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                        continue
                    if procurando_dados and validar_mes_ano(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"competencia": value}
                        modelo_colunas[coluna].append(contribuicao_dict)
                if coluna in [1, 4, 7]:
                    if value == "Remuneração":
                        procurando_dados = False
                        valida_colunas["remuneracao"] = True
                        continue
                    if procurando_dados and validar_remuneracao(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["remuneracao"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"value": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [2, 5, 8]:
                    continue
                    if value == "Indicadores":
                        procurando_dados = False
                        valida_colunas["indicadores"] = True
                        continue
                    if not procurando_dados:
                        contribuicao_dict = {"Indicadores": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
        if False in valida_colunas.values():
            raise Exception("Não foi possível extrair as remunerações")
        return contribuicao_coluna1 + contribuicao_coluna2 + contribuicao_coluna3

    @staticmethod
    def extrair_contratos(dict_data):
        contribuicao_coluna1 = []
        modelo_colunas = {
            0: contribuicao_coluna1,
            1: contribuicao_coluna1,
            2: contribuicao_coluna1,
            3: contribuicao_coluna1,
            4: contribuicao_coluna1,
            5: contribuicao_coluna1,
        }

        valida_colunas = {
            "competencia": False,
            "Contrat./Cooperat.": False,
            "Estabelecimento": False,
            "Tomador": False,
            "Forma Prestação Serviço": False,
            "Remuneração": False
        }
        sem_titulo = False
        verifica_linha = 0
        for coluna in dict_data:
            procurando_dados = True
            linhas = 0
            for linha, value in dict_data[coluna].items():
                if coluna in [0]:
                    if value == "" and linha == verifica_linha:
                        verifica_linha += 1
                    if value == "Competência":
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                        continue
                    if procurando_dados and validar_mes_ano(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"competencia": value}
                        modelo_colunas[coluna].append(contribuicao_dict)
                if coluna in [1]:
                    if value == "Contrat./Cooperat.":
                        procurando_dados = False
                        valida_colunas["Contrat./Cooperat."] = True
                        continue
                    if procurando_dados and validar_cnpj(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["Contrat./Cooperat."] = True
                        sem_titulo = True
                    if not procurando_dados:
                        contribuicao_dict = {"Contrat./Cooperat.": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [2]:
                    if value == "Estabelecimento":
                        procurando_dados = False
                        valida_colunas["Estabelecimento"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Estabelecimento"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"Estabelecimento": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [3]:
                    if value == "Tomador":
                        procurando_dados = False
                        valida_colunas["Tomador"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Tomador"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"Tomador": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [4]:
                    if value == 'Forma Prestação Serviço':
                        procurando_dados = False
                        valida_colunas["Forma Prestação Serviço"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Forma Prestação Serviço"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"servico": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [5]:
                    if value == "Remuneração":
                        procurando_dados = False
                        valida_colunas["Remuneração"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Remuneração"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"value": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
        if False in valida_colunas.values():
            raise Exception("Não foi possível extrair os contratos")
        return contribuicao_coluna1

    @staticmethod
    def extrair_contribuicoes(dict_data):
        contribuicao_coluna1 = []
        contribuicao_coluna2 = []

        modelo_colunas = {
            0: contribuicao_coluna1,
            1: contribuicao_coluna1,
            2: contribuicao_coluna1,
            3: contribuicao_coluna1,
            5: contribuicao_coluna2,
            6: contribuicao_coluna2,
            7: contribuicao_coluna2,
            8: contribuicao_coluna2,
        }
        valida_colunas = {
            "competencia": False,
            "Data Pgto.": False,
            "Contribuição": False,
            "Salário Contribuição": False,
        }
        sem_titulo = False
        verifica_linha = 0
        for coluna in dict_data:
            procurando_dados = True
            linhas = 0
            for linha, value in dict_data[coluna].items():
                if coluna in [0, 5]:
                    if value == "" and linha == verifica_linha:
                        verifica_linha += 1
                    if value == "Competência":
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                        continue
                    if procurando_dados and validar_mes_ano(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["competencia"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"competencia": value}

                        modelo_colunas[coluna].append(contribuicao_dict)
                if coluna in [1, 6]:
                    if value == "Data Pgto.":
                        procurando_dados = False
                        valida_colunas["Data Pgto."] = True
                        continue
                    if procurando_dados and validar_data(value) and linha == verifica_linha:
                        procurando_dados = False
                        valida_colunas["Data Pgto."] = True
                        sem_titulo = True
                    if not procurando_dados:
                        contribuicao_dict = {"Data Pgto.": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [2, 7]:
                    if value == "Contribuição":
                        procurando_dados = False
                        valida_colunas["Contribuição"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Contribuição"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"Contribuição": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1
                if coluna in [3, 8]:
                    if value == "Salário Contribuição":
                        procurando_dados = False
                        valida_colunas["Salário Contribuição"] = True
                        continue
                    if sem_titulo:
                        procurando_dados = False
                        valida_colunas["Salário Contribuição"] = True
                    if not procurando_dados:
                        contribuicao_dict = {"value": value}
                        modelo_colunas[coluna][linhas].update(contribuicao_dict)
                        linhas += 1

        if False in valida_colunas.values():
            raise Exception("Não foi possível extrair as remunerações")
        return contribuicao_coluna1 + contribuicao_coluna2
