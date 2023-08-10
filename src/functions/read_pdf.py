import camelot
from src.models import *
import json

class LeitorExtrato:
    def __init__(self, path_file):
        self.path_file = path_file
        self.dados = None

    def extrair_dados(self):
        tables = camelot.read_pdf(
            self.path_file,
            pages="1",
            flavor="stream",
            edge_tol=50,
            table_areas=TABLES_AREAS,
            COLUNAS=COLUNAS,

        )
        data_leituras = {}
        dados_gerais = {}
        dados_tributos = {}
        itens_fatura = {}
        info_consumo = {}
        grandezas = {}
        medidores = []
        for index in range(len(tables)):
            dataframe = tables[index].df
            dict_data = dataframe.to_dict()
            #print(json.dumps(dict_data, indent=4))
            match INDEX_TABLES[str(index)]:
                case "TENSAO":
                    #print(json.dumps(dict_data, indent=4))
                    print("TENSAO")
                case "DATAS_LEITURAS":
                    data_leituras["Leitura Anterior"] = dict_data[1][1]
                    data_leituras["Leitura Atual"] = dict_data[2][1]
                    data_leituras["Numero de Dias"] = dict_data[3][1]
                    data_leituras["Proxima Leitura"] = dict_data[4][1]

                case "PARCEIRO_DE_NEGOCIO":
                    dados_gerais["Parceiro de Negocio"] = dict_data[0][0]

                case "CONTA":
                    dados_gerais["Conta Contrato"] = dict_data[0][0]

                case "CONTA_MES_VENCIMENTO_TOTAL":
                    dados_gerais["Mes"] = dict_data[0][1]
                    dados_gerais["Vencimento"] = dict_data[1][1]
                    dados_gerais["Total"] = dict_data[2][1]

                case "TRIBUTOS":
                    for key, value in dict_data[0].items():
                        if dados_tributos.get(value) is None:
                            dados_tributos[value] = {}
                        dados_tributos[value]["base"] = dict_data[1][key]
                        dados_tributos[value]["aliquota"] = dict_data[2][key]
                        dados_tributos[value]["valor"] = dict_data[3][key]

                case "GRANDEZAS_CONTRATADAS":
                    for key, value in dict_data[0].items():
                        if "Demanda Contratada \u00danica (kW): " in value:
                            value_strip = value.split("Demanda Contratada \u00danica (kW): ")
                            grandezas["Demanda Contratada Única (kW)"] = value_strip[1]
                        if "Demanda Contratada Ponta (kW): " in value:
                            value_strip = value.split("Demanda Contratada Ponta (kW): ")
                            grandezas["Demanda Contratada Ponta (kW)"] = value_strip[1]
                        if "Demanda Contratada Fora Ponta (kW): " in value:
                            value_strip = value.split("Demanda Contratada Fora Ponta (kW): ")
                            grandezas["Demanda Contratada Fora Ponta (kW)"] = value_strip[1]
                        if "Dem. Reserva Cap. \u00danica (kW): " in value:
                            value_strip = value.split("Dem. Reserva Cap. \u00danica (kW): ")
                            grandezas["Dem. Reserva Cap. Única"] = value_strip[1]
                        if "Dem. Reserva Cap. Fora Ponta (kW): " in value:
                            value_strip = value.split("Dem. Reserva Cap. Fora Ponta (kW): ")
                            grandezas["Dem. Reserva Cap. Fora Ponta (kW)"] = value_strip[1]
                        if "Dem. Reserva Cap. Ponta (kW): " in value:
                            value_strip = value.split("Dem. Reserva Cap. Ponta (kW): ")
                            grandezas["Dem. Reserva Cap. Ponta (kW)"] = value_strip[1]
                        if "Dem. de Gera\u00e7\u00e3o (kW): " in value:
                            value_strip = value.split("Dem. de Gera\u00e7\u00e3o (kW): ")
                            grandezas["Dem. de Geração (kW)"] = value_strip[1]
                        if "Dem. de Dist. \u00danica (kW): " in value:
                            value_strip = value.split("Dem. de Dist. \u00danica (kW): ")
                            grandezas["Dem. de Dist. Única (kW)"] = value_strip[1]
                        if "Dem. de Dist. De Ponta (kW): " in value:
                            value_strip = value.split("Dem. de Dist. De Ponta (kW): ")
                            grandezas["Dem. de Dist. De Ponta (kW)"] = value_strip[1]
                        if "Dem. de Dist. Fora Ponta (kW): " in value:
                            value_strip = value.split("Dem. de Dist. Fora Ponta (kW): ")
                            grandezas["Dem. de Dist. Fora Ponta (kW)"] = value_strip[1]

                case "ITENS_FATURA":
                    for key, value in dict_data[0].items():
                        if value in ["ITENS FINANCEIROS", "Cip-Ilum Pub Pref Munic"]:
                            if value == "Cip-Ilum Pub Pref Munic":
                                itens_fatura[value] = {}
                                itens_fatura[value]["valor"] = dict_data[6][key]
                            continue
                        if itens_fatura.get(value) is None:
                            itens_fatura[value] = {}
                        itens_fatura[value]["quantidade"] = dict_data[1][key]
                        itens_fatura[value]["preco_unit_com_tributos"] = dict_data[2][key]
                        itens_fatura[value]["tarifca_unit"] = dict_data[3][key]
                        itens_fatura[value]["pis/confins"] = dict_data[4][key]
                        itens_fatura[value]["icms"] = dict_data[5][key]
                        itens_fatura[value]["valor"] = dict_data[6][key]

                case "RESERVADO_FISICO":
                    dados_gerais["Reservado Fisico"] = dict_data[0][0]

                case "APRESENTACAO":
                    dados_gerais["data_apresentacao"] = dict_data[0][0]

                case "RESOLUCAO":
                    dados_gerais["resolucao"] = dict_data[0][0]

                case "INFO_CONSUMO":
                    for key, value in dict_data[0].items():
                        if "Consumo M\u00e9dio Di\u00e1rio (kWh):" in value:
                            value_strip = value.split("Consumo M\u00e9dio Di\u00e1rio (kWh): ")
                            info_consumo["Consumo Médio Diário (kWh)"] = value_strip[1]
                        if "M\u00e9dia dos 12 meses (kWh): " in value:
                            value_strip = value.split("M\u00e9dia dos 12 meses (kWh): ")
                            info_consumo["Média dos 12 meses (kWh)"] = value_strip[1]
                        if "Dem. M\u00e1x. F. Ponta (kW): " in value:
                            value_strip = value.split("Dem. M\u00e1x. F. Ponta (kW): ")
                            info_consumo["Dem. Máx. F. Ponta (kW)"] = value_strip[1]
                        if "Dem. M\u00e1x. Ponta (kW): " in value:
                            value_strip = value.split("Dem. M\u00e1x. Ponta (kW): ")
                            info_consumo["Dem. Máx. Ponta (kW)"] = value_strip[1]

                case "MEDIDORES":
                    for key, value in dict_data[0].items():
                        dados_medidores = {}
                        if value != "":
                            dados_medidores[value] = {}
                        else:
                            continue
                        dados_medidores[value]["grandeza"] = dict_data[1][key]
                        dados_medidores[value]["posto_horario"] = dict_data[2][key]
                        dados_medidores[value]["leitura_anterior"] = dict_data[3][key]
                        dados_medidores[value]["leitura_atual"] = dict_data[4][key]
                        dados_medidores[value]["const_medidor"] = dict_data[5][key]
                        dados_medidores[value]["consumo"] = dict_data[6][key]
                        medidores.append(dados_medidores)

                case _:
                    print("Não foi possível identificar o tipo de dado")
        self.dados = {
            "data_leituras": data_leituras,
            "dados_gerais": dados_gerais,
            "dados_tributos": dados_tributos,
            "itens_fatura": itens_fatura,
            "info_consumo": info_consumo,
            "grandezas": grandezas,
            "medidores": medidores
        }
        print(self.dados)
