import requests

# Lista de URLs para testar
urls = [
    "http://127.0.0.1:8000/producao/",
    "http://127.0.0.1:8000/comercio/",
    "http://127.0.0.1:8000/processamento/",
    "http://127.0.0.1:8000/importacao/",
    "http://127.0.0.1:8000/exportacao/",
]

# Função para testar os endpoints
def testar_endpoints(urls):
    """
    Função que realiza requisições HTTP GET para cada URL na lista fornecida,
    verificando o status da resposta e imprimindo o resultado.

    Parâmetros:
    - urls (list): Lista de URLs para testar.

    Para cada URL, a função:
    - Realiza uma requisição HTTP GET.
    - Verifica o código de status da resposta:
        - 200: Sucesso.
        - 404: URL não encontrada.
        - Outros códigos: Erro inesperado.
    - Em caso de falha na requisição, imprime a mensagem de erro correspondente.
    """
    for url in urls:
        try:
            # Realiza a requisição GET
            response = requests.get(url)
            status_code = response.status_code
            # Verifica o código de status e imprime o resultado
            if status_code == 200:
                print(f"URL: {url} -> Sucesso (200)")
            elif status_code == 404:
                print(f"URL: {url} -> Não encontrado (404)")
            else:
                print(f"URL: {url} -> Erro inesperado ({status_code})")
        except requests.exceptions.RequestException as e:
            # Captura e imprime qualquer erro de conexão
            print(f"URL: {url} -> Falha ao conectar ({e})")

# Executa o teste
if __name__ == "__main__":
    # Chama a função de teste passando a lista de URLs
    testar_endpoints(urls)
