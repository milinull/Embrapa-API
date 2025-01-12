import requests  # Biblioteca para realizar requisições HTTP
from bs4 import BeautifulSoup  # Biblioteca para parsear HTML e XML
import pandas as pd  # Biblioteca para manipulação e análise de dados
import time  # Biblioteca para funções relacionadas ao tempo

def obter_dados_vinhos():
    """
    Função para coletar dados sobre vinhos e derivados do site da Embrapa.
    
    Esta função acessa uma URL base da Embrapa para extrair dados tabulares sobre vinhos, derivados e produção agrícola
    entre os anos de 1970 e 2023. Os dados são organizados em categorias, processados em tabelas e salvos em um arquivo CSV.
    
    Retorna:
        pd.DataFrame: Um DataFrame consolidado contendo os dados extraídos.
    """
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    anos = list(range(1970, 2024))  # Lista de anos para busca (1970 a 2023)
    todas_as_tabelas = []  # Lista para armazenar todas as tabelas extraídas

    for ano in anos:
        # Parâmetros da requisição GET
        params = {
            "ano": ano,  # Ano a ser consultado
            "opcao": "opt_04",  # Opção específica no sistema
            # "subopcao": "subopt_04"  # Usado para opções adicionais, se necessário
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
                if len(cols) > 1:  # Verifica se há colunas suficientes
                    produto = cols[0].get_text(strip=True)  # Primeira coluna (produto ou categoria)
                    quantidade = cols[1].get_text(strip=True)  # Segunda coluna (quantidade)

                    # Verifica se a linha representa uma categoria total
                    if 'tb_item' in cols[0].get('class', []):
                        current_category = produto
                        # Adiciona os dados da categoria total
                        dados.append([f"{current_category}_TOTAL", "", "", quantidade, ano])
                    
                    # Verifica se a linha representa um subitem
                    elif 'tb_subitem' in cols[0].get('class', []):
                        if current_category:  # Garante que haja uma categoria associada
                            # Adiciona os dados do subitem
                            dados.append([current_category, produto, quantidade, "", ano])
            
            # Converte os dados em um DataFrame
            df = pd.DataFrame(dados, columns=["Categoria", "Produto", "Quantidade (L.)", "Total_Categoria", "Ano"])
            todas_as_tabelas.append(df)  # Adiciona o DataFrame à lista
            print(f"Tabela do ano {ano} extraída com sucesso.")
        else:
            print(f"Nenhuma tabela encontrada para o ano {ano}.")
        
        # Aguarda 1 segundo entre as requisições para evitar sobrecarregar o servidor
        time.sleep(1)

    # Consolida todas as tabelas extraídas em um único DataFrame
    tabela_completa = pd.concat(todas_as_tabelas, ignore_index=True)
    tabela_completa.to_csv("dados_vinhos_comerc.csv", index=False)  # Salva os dados em um arquivo CSV
    print("Todas as tabelas foram consolidadas.")
    
    return tabela_completa  # Retorna o DataFrame consolidado

if __name__ == "__main__":
    """
    Executa a função `obter_dados_vinhos` se o script for executado diretamente.
    """
    obter_dados_vinhos()
