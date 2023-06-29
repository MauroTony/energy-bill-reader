from functions import LeitorExtrato
import json

pdf = "extrato (38)"

leitor = LeitorExtrato(f"pdfs/{pdf}.pdf")
leitor.identifica_tabelas()
leitor.extrair_identificacao()
leitor.extrair_relacoes()
result = leitor.resultado()

content = result
print(content)
content = json.dumps(content)
with open(f"{pdf}.txt", 'w') as file:
    pdf_content = file.write(content)