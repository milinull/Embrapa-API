import requests  # Biblioteca para realizar requisições HTTP
from bs4 import BeautifulSoup  # Biblioteca para parsear HTML e XML
import pandas as pd  # Biblioteca para manipulação e análise de dados
import time  # Biblioteca para funções relacionadas ao tempo

def obter_dados_vinhos():
    """
    Função para coletar dados sobre vinhos e derivados (importação de vinhos) do site da Embrapa.
    
    Esta função acessa uma URL base da Embrapa para extrair dados tabulares sobre a quantidade e valor de vinhos
    importados para o Brasil, entre os anos de 1970 e 2023. Os dados são organizados em categorias de países e valores,
    processados em tabelas e salvos em um arquivo CSV.
    
    Retorna:
        pd.DataFrame: Um DataFrame consolidado contendo os dados extraídos sobre a importação de vinhos.
    """
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    anos = list(range(1970, 2024))  # Lista de anos para busca (1970 a 2023)
    todas_as_tabelas = []  # Lista para armazenar todas as tabelas extraídas

    for ano in anos:
        # Parâmetros da requisição GET
        params = {
            "ano": ano,  # Ano a ser consultado
            "opcao": "opt_05",  # Opção específica no sistema (importação de vinhos)
            "subopcao": "subopt_01"  # Subopção relacionada aos vinhos mesa
        }
        
        # Realiza a requisição HTTP
        response = requests.get(base_url, params=params)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code != 200:
            print(f"Erro ao acessar o ano {ano}. Pulando para o próximo.")
            continue
        
        # Parseia o conteúdo HTML da resposta
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Procura pela tabela de dados no HTML
        tabela_html = soup.find("table", class_="tb_base tb_dados")
        
        if tabela_html:
            dados = []  # Lista para armazenar os dados da tabela atual
            current_category = None  # Categoria atual (se aplica a subitens)

            # Itera pelas linhas da tabela
            for row in tabela_html.find_all("tr"):
                cols = row.find_all("td")  # Colunas da linha
                
                # Caso tenha três colunas na tabela (categoria, produto, quantidade)
                if len(cols) == 3:
                    categoria = cols[0].get_text(strip=True)  # Primeira coluna (categoria)
                    produto = cols[1].get_text(strip=True)  # Segunda coluna (produto)
                    quantidade = cols[2].get_text(strip=True)  # Terceira coluna (quantidade)

                    # Ignora linhas onde o texto é "Total"
                    if categoria.lower() == "total":
                        continue
                    
                    dados.append([categoria, produto, quantidade, ano])
                
                # Caso tenha duas colunas (produto e quantidade)
                elif len(cols) == 2:
                    produto = cols[0].get_text(strip=True)  # Primeira coluna (produto)
                    quantidade = cols[1].get_text(strip=True)  # Segunda coluna (quantidade)

                    # Ignora linhas onde o texto é "Total"
                    if produto.lower() == "total":
                        continue
                    
                    # Se for uma categoria (linha de item)
                    if 'tb_item' in cols[0].get('class', []):
                        current_category = produto
                        dados.append([current_category, "TOTAL", quantidade, ano])
                    # Se for um subitem (linha de subcategoria)
                    elif 'tb_subitem' in cols[0].get('class', []):
                        if current_category:
                            dados.append([current_category, produto, quantidade, ano])
            
            # Cria DataFrame com os dados extraídos
            df = pd.DataFrame(dados, columns=["Países", "Quantidade (Kg)", "Valor (US$)", "Ano"])
            todas_as_tabelas.append(df)  # Adiciona o DataFrame à lista
            print(f"Tabela do ano {ano} extraída com sucesso.")
        else:
            print(f"Nenhuma tabela encontrada para o ano {ano}.")
        
        # Aguarda 1 segundo entre as requisições para evitar sobrecarregar o servidor
        time.sleep(1)

    # Consolida todas as tabelas extraídas em um único DataFrame
    tabela_completa = pd.concat(todas_as_tabelas, ignore_index=True)
    # Salva os dados em um arquivo CSV com codificação UTF-8 com BOM
    tabela_completa.to_csv("dados_vinhos_import_vinho_mesa.csv", index=False, encoding="utf-8-sig")
    print("Todas as tabelas foram consolidadas.")
    
    return tabela_completa  # Retorna o DataFrame consolidado

if __name__ == "__main__":
    """
    Executa a função `obter_dados_vinhos` se o script for executado diretamente.
    """
    obter_dados_vinhos()
