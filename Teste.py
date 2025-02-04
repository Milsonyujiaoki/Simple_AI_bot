import os
from dotenv import load_dotenv
import openai
import asyncio

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define sua chave de API da OpenAI a partir da variável de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

# Inicializa o cliente assíncrono
client = openai.AsyncOpenAI(
    api_key=openai.api_key,
    max_retries=2,
    timeout=20.0
)

# Função assíncrona para interagir com o ChatGPT
async def conversar_com_chatgpt(mensagem_usuario):
    try:
        resposta = await client.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem_usuario}]
        )
        return resposta.choices[0].message['content']

    except openai.error.APIConnectionError as e:
        print("O servidor não pôde ser alcançado")
        print(e)
    except openai.error.RateLimitError as e:
        print("Erro 429: Limite de requisições excedido. Aguarde um momento antes de tentar novamente.")
    except openai.error.APIError as e:
        print(f"Erro na API com status {e.http_status}")
        print(e)

# Função principal para gerenciar a interação
async def main():
    while True:
        mensagem = input("Você: ")
        if mensagem.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando a conversa. Até logo!")
            break

        resposta_chatgpt = await conversar_com_chatgpt(mensagem)
        if resposta_chatgpt:
            print(f"ChatGPT: {resposta_chatgpt}")

# Executa o loop assíncrono
asyncio.run(main())
