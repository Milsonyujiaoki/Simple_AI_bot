import os
import asyncio
from openai import AsyncOpenAI
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Defina sua chave de API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY', '')

# Inicializa o cliente assíncrono
client = AsyncOpenAI(
    api_key=openai.api_key,
    max_retries=3,
    timeout=20.0,
    organization='',
    project=''
)

# Implementa o retry com backoff exponencial para tratar Rate Limits
@retry(wait=wait_random_exponential(min=2, max=120), stop=stop_after_attempt(10))
async def conversar_com_chatgpt(mensagem_usuario):
    resposta = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": mensagem_usuario}]
    )
    return resposta.choices[0].message.content

# Função principal para gerenciar a interação
async def main():
    max_requests_per_minute = 60  # Limite máximo de requisições por minuto
    request_interval = 60 / max_requests_per_minute  # Intervalo entre requisições

    while True:
        mensagem = input("Você: ")
        if mensagem.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando a conversa. Até logo!")
            break

        try:
            resposta_chatgpt = await conversar_com_chatgpt(mensagem)
            if resposta_chatgpt:
                print(f"ChatGPT: {resposta_chatgpt}")
            await asyncio.sleep(request_interval)  # Controle de taxa de requisição
        except openai.APIConnectionError as e:
            print("O servidor não pôde ser alcançado. Verifique sua conexão de rede.")
            print(e.__cause__)
        except openai.RateLimitError as e:
            print("Erro 429: Limite de requisições excedido após várias tentativas. Tente novamente mais tarde.")
            print(f"Detalhes: {e}")
        except openai.AuthenticationError:
            print("Erro 401: Falha na autenticação. Verifique sua chave de API.")
        except openai.PermissionDeniedError:
            print("Erro 403: Acesso negado. Verifique suas permissões na API.")
        except openai.NotFoundError:
            print("Erro 404: Recurso não encontrado. Verifique o endpoint ou recurso solicitado.")
        except openai.BadRequestError as e:
            print(f"Erro 400: Solicitação inválida. Verifique os parâmetros enviados. Detalhes: {e}")
        except openai.APIError as e:
            print(f"Erro 500: Erro interno no servidor da OpenAI. Tente novamente mais tarde.")
            print(e)
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Executa o loop assíncrono
asyncio.run(main())
