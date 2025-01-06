import os
import sys
import django
import pandas as pd
import logging

# Adicione o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar o Django para usar o arquivo de configurações do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

# Importar o modelo após configurar o Django
from embrapa.models import *

# Configurar logging para exibir mensagens informativas
logging.basicConfig(level=logging.INFO)

def importar_csv_processamento(caminho_arquivo):
    """
    Função que importa dados de um arquivo CSV para o banco de dados. 
    Ela lê o arquivo CSV, processa cada linha e cria objetos do modelo 'Comercio'.
    
    Parâmetros:
    caminho_arquivo (str): O caminho completo para o arquivo CSV a ser importado.

    Observações:
    O código comentado dentro da função pode ser usado para categorizar os dados 
    do CSV, dependendo do nome do arquivo. A implementação pode ser alterada conforme
    a necessidade, descomentando o código e adaptando-o.
    """

#    nome_arquivo = os.path.basename(caminho_arquivo)
    
#    if "espumantes" in nome_arquivo:
#        tipo = "Espumantes"
#    elif "suco_uva" in nome_arquivo:
#        tipo = "Suco de Uva"
#    elif "uvas_frescas" in nome_arquivo:
#        tipo = "Uvas Frescas"
#    elif "uvas_passas" in nome_arquivo:
#        tipo = "Uvas Passas"
#    elif "vinho_mesa" in nome_arquivo:
#        tipo = "Vinho de Mesa"
#    else:
#        tipo = "Outros"

    # Carregar o CSV usando pandas
    df = pd.read_csv(caminho_arquivo, encoding='utf-8')

    for _, linha in df.iterrows():
        """
        Itera sobre as linhas do DataFrame 'df' e cria um objeto 'Comercio' para cada linha,
        salvando os dados no banco de dados. Também registra uma mensagem no log informando
        que a linha foi importada com sucesso.

        Parâmetros:
        - df (pandas.DataFrame): O DataFrame que contém os dados a serem importados.

        Para cada linha do DataFrame:
        - 'Categoria': A categoria do produto (e.g., tipo de vinho ou uva).
        - 'Produto': O nome do produto (e.g., vinho, uva fresca).
        - 'Quantidade (L.)': A quantidade do produto em litros.
        - 'Total_Categoria': O valor total da categoria (e.g., valor total de vendas ou produção).
        - 'Ano': O ano relacionado à importação do produto.

        A linha é convertida em um dicionário e registrada no log para acompanhamento.
        """
        # Criar um novo objeto 'Comercio' com os dados da linha
        Comercio.objects.create(
            categoria=linha['Categoria'],
            produto=linha['Produto'],
            quantidade_litros=linha['Quantidade (L.)'],
            total_categoria=linha['Total_Categoria'],
            ano=linha['Ano'],
        )
        # Registrar no log a importação da linha
        logging.info(f"Importada linha: {linha.to_dict()}")


# Este bloco de código é executado quando o script é executado diretamente.
if __name__ == "__main__":
    # Chama a função 'importar_csv_processamento' passando o caminho do arquivo CSV
    importar_csv_processamento(
        'C:\\Users\\Raphael\\Desktop\\Embrapa_API\\dir_csv\\dados_vinhos_comercio.csv'
    )

    # Exibe uma mensagem indicando que a importação foi concluída
    print("Importação do arquivo CSV concluída!")
