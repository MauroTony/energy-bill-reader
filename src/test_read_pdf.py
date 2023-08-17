from functions import LeitorExtrato
import json

pdf = "01-23"

leitor = LeitorExtrato(f"pdfs/{pdf}.pdf")
result = leitor.extrair_dados()
content = json.dumps(result, indent=4)
print(content)

with open(f"{pdf}.txt", 'w') as file:
    pdf_content = file.write(content)