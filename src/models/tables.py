ref_colunas_model1 = ["59,135,228,415,540,640,752"]
ref_colunas_model2 = ["59,174,415,557,632,700"]
ref_colunas_model3 = ["59,134,215,360,535,607,673"]
ref_colunas_model4 = ["59,131,220,430,485,550,665,736"]
ref_colunas_model5 = ["59,96,204,429,487,552,691"]
ref_colunas_model6 = ["59,131,219,430,484,550,661,733"]

modelo1 = [
    "seq",
    "NIT",
    "Código Emp.",
    "Origem do Vínculo",
    "Matrícula do\nTrabalhador",
    "Tipo Filiado no\nVínculo",
    "Data Início Data Fim",
    "Últ. Remun.",
]
modelo2 = [
    "seq",
    "NIT",
    "Origem do Vínculo",
    "Tipo Filiado no Vínculo",
    "Data Início",
    "Data Fim",
    "Indicadores",
]
modelo3 = [
    "seq",
    "NIT",
    "NB",
    "Origem do Vínculo",
    "Espécie",
    "Data Início",
    "Data Fim",
    "Situação",
]

modelo4 = [
    "seq",
    "NIT",
    "CNPJ/CEI/CPF",
    "Origem do Vínculo",
    "Data Início",
    "Data Fim",
    "Tipo Filiado no Vínculo",
    "Últ. Remun.",
    "Indicadores",
]
modelo5 = [
    "seq",
    "NIT",
    "Origem do Vínculo",
    "Data Início",
    "Data Fim",
    "Tipo Filiado no Vínculo",
    "Indicadores",
]
modelo6 = [
    "seq",
    "NIT",
    "Código Emp.",
    "Origem do Vínculo",
    "Data Início",
    "Data Fim",
    "Tipo Filiado no Vínculo",
    "Últ. Remun.",
    "Indicadores",
]


modelos = [
    {"modelo": modelo1, "colunas": ref_colunas_model1},
    {"modelo": modelo2, "colunas": ref_colunas_model2},
    {"modelo": modelo3, "colunas": ref_colunas_model3},
    {"modelo": modelo4, "colunas": ref_colunas_model4},
    {"modelo": modelo6, "colunas": ref_colunas_model6},
    {"modelo": modelo5, "colunas": ref_colunas_model5},
]

ref_table_remuneracoes = ["115,205,235,375,470,554,640,730"]
ref_table_contribuicoes = ["96,156,225,322,418,499,559,626,725"]
colunas_remuneracoes = [ref_table_remuneracoes, ref_table_contribuicoes]
