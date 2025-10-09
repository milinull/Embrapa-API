import pandas as pd
import requests
import boto3
import unicodedata
import re
import time
import random
from decouple import config, Config, RepositoryEnv
from bs4 import BeautifulSoup
import io

config = Config(RepositoryEnv('.env'))

s3 = boto3.client(
    's3',
    aws_access_key_id = config('AWS_ACCESS_KEY'),
    aws_secret_access_key = config('AWS_SECRET_KEY'),
    region_name = config('AWS_LOCAL'),
)

bucket_name = config('AWS_DESTINY')

def sanitize_filename(filename):
    """
    Remove acentos, espaços e caracteres especiais de nomes de arquivo.
    """
    # Normaliza para remover acentos
    nfkd_form = unicodedata.normalize('NFKD', filename)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    # Substitui espaços e caracteres não alfanuméricos por underscore
    sanitized = re.sub(r'[^0-9a-zA-Z]+', '_', only_ascii)
    return sanitized.strip('_')

# Upload de arquivo local para o S3
def upload_arquivo(caminho_local, chave_s3):
    s3.upload_file(caminho_local, bucket_name, chave_s3)
    print(f"Upload concluído: {caminho_local} -> s3://{bucket_name}/{chave_s3}")

def scrape_table(url, ano, botao_text=None):
    """
    Faz o scraping de uma tabela em uma URL e adiciona o ano e, opcionalmente, o tipo.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='tb_base tb_dados')
    if not table:
        return [], None

    table_name_tag = soup.find('p', class_='text_center')
    table_name = table_name_tag.text.strip() if table_name_tag else "table"
    botao_text = soup.find('button', {'value': botao_text}).get_text(strip=True)

    rows = []
    for row in table.find_all('tr'):
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:
            # Adiciona botao_text se fornecido
            if botao_text:
                rows.append([ano, botao_text] + cols)
            else:
                rows.append([ano] + cols)

    return rows, table_name

# Definindo colunas por página
columns_dict = {
    2: ["Ano", "Produto", "Quantidade (L.)"],
    3: ["Ano", "Tipo", "Cultivar", "Quantidade (KG)"],
    4: ["Ano", "Produto", "Quantidade (L.)"],
    5: ["Ano", "Tipo", "Países", "Quantidade (KG)", "Valor (US$)"],
    6: ["Ano", "Tipo", "Países", "Quantidade (KG)", "Valor (US$)"]
}

# Número de subopções por página
suboptions_dict = {
    3: 4,
    5: 5,
    6: 4
}

for page in range(2, 7):
    element_list = []

    for ano in range(2024, 1969, -1):
        base_url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_0{page}"

        # Verifica se a página tem subopções
        if page in suboptions_dict:
            for x in range(1, suboptions_dict[page] + 1):
                url = f"{base_url}&subopcao=subopt_0{x}"
                botao_text = f"subopt_0{x}"  # texto do botão para adicionar à tabela
                rows, table_name = scrape_table(url, ano, botao_text)
                element_list.extend(rows)

                # Pausa de 1 a 3 segundos aleatoriamente para não sobrecarregar o servidor
                time.sleep(random.uniform(2, 4))
        else:
            rows, table_name = scrape_table(base_url, ano)
            element_list.extend(rows)

    # Cria DataFrame e salva CSV
    df = pd.DataFrame(element_list, columns=columns_dict.get(page, ["Ano", "Dado1", "Dado2"]))
    
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='fastparquet')
    parquet_buffer.seek(0)

    # Enviar para o S3
    sanitized_table_name = sanitize_filename(table_name[:-7].strip().replace(",", ""))
    s3.put_object(
        Bucket=bucket_name,
        Key=f"embrapa-api/bronze/table_{sanitized_table_name}.parquet",
        Body=parquet_buffer.getvalue()
    )

    print(f"Página {page} concluída. Parquet enviado para S3: bronze/table_{sanitized_table_name}.parquet")
