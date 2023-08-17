# Introduction 
Microserviço que realiza extraçao dos dados de um pdf funcionando via rabbitmq 

# Getting Started
1. Enviroments
2. Instalaçao
3. Testes

# Enviroments
    RABBITMQ_USER -> Usuario do Rabbitmq
    RABBITMQ_PASS -> Senha do usuario do Rabbitmq
    RABBITMQ_HOST -> Endereço de conexao do Rabbitmq
    RABBITMQ_PORT -> Porta de conexao do Rabbitmq
    RABBITMQ_SUBSCRIBE_QUEUE -> Nome da Fila que o sistema vai ler as mensagens
    RABBITMQ_PUBLISH_QUEUE -> Nome da Fila que o sistema vai enviar a resposta 
    THREADS -> Quantidade de Threads que o sistema vai utilizar para rodar em paralelo

# Instalaçao
## dependencias
* OBS: Ambiente linux ou wls
## Build Docker
Configurar .env baseada no .env.example

    docker compose  up -d

## Build Local
Instale as dependencias do requirements

    pip install -r requirements.txt

Instale algumas dependencias do sistema

    apt-get update && apt-get install ffmpeg libsm6 libxext6 poppler-utils -y

Executar o main.py
* Navegue para o src: `cd src`
* Execute o programa `python main`

# Exemplo de resposta e payload
O sistema espera receber da fila, configurada no parametro RABBITMQ_SUBSCRIBE_QUEUE da .env, um payload igual ao arquivo example-payload.json

O sistema irá retornar um json para a fila, configurada no parametro RABBITMQ_PUBLISH_QUEUE da .env, do mesmo modelo encontrado no arquivo example-response.json
    
# Teste
No arquivo test_read_pdf.py altere o valor da variavel 'pdf' com o nome do pdf que deseja analisar e que esteja disponivel da pasta pdf e  execute.

`python test_read_pdf `

