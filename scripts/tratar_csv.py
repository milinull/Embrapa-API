import pandas as pd

def tratar_valor(valor, tipo="texto"):
    """
    Trata valores vazios ou inválidos no dataframe.
    
    Parâmetros:
    - valor: O valor a ser tratado. Pode ser qualquer tipo de dado.
    - tipo (str): O tipo de tratamento a ser realizado. Pode ser:
        - "texto" (default): Trata valores como texto. Retorna None para valores vazios ou inválidos.
        - "numero": Trata valores como números. Retorna 0 para valores vazios ou inválidos.
    
    Retorna:
    - O valor tratado, conforme o tipo especificado:
        - Se tipo="texto" e o valor for vazio ou inválido, retorna None.
        - Se tipo="numero" e o valor for vazio ou inválido, retorna 0.
        - Caso contrário, retorna o valor convertido para o tipo adequado (número ou texto).
    """
    if pd.isna(valor) or valor in ["-", ""]:
        return None if tipo == "texto" else 0
    try:
        valor = str(valor)
        
        if tipo == "numero":
            if '.' in valor or ',' in valor:
                return float(valor.replace('.', '').replace(',', '.'))
            else:
                return int(valor)  # Garante que os valores inteiros não sejam convertidos para float
        return valor
    except ValueError:
        return None if tipo == "texto" else 0

def tratar_csv(caminho_arquivo, caminho_arquivo_tratado):
    """
    Carrega um arquivo CSV, trata os valores nas colunas e salva o arquivo tratado em outro local.
    
    Parâmetros:
    - caminho_arquivo (str): O caminho do arquivo CSV de entrada.
    - caminho_arquivo_tratado (str): O caminho para salvar o arquivo CSV tratado.
    
    A função realiza as seguintes ações:
    - Trata as colunas 'Categoria', 'Produto', 'Quantidade (L.)', 'Total_Categoria' e 'Ano'.
    - A coluna 'Categoria' e 'Produto' são tratadas como texto.
    - As colunas 'Quantidade (L.)', 'Total_Categoria' e 'Ano' são tratadas como números.
    - O arquivo tratado é salvo no caminho especificado.
    """
    # Carregar o CSV usando pandas
    df = pd.read_csv(caminho_arquivo, encoding='utf-8')

    # Tratar e limpar os dados do dataframe
    df['Categoria'] = df['Categoria'].apply(lambda x: tratar_valor(x, tipo="texto"))
    df['Produto'] = df['Produto'].apply(lambda x: tratar_valor(x, tipo="texto"))
    df['Quantidade (L.)'] = df['Quantidade (L.)'].apply(lambda x: tratar_valor(x, tipo="numero"))
    df['Total_Categoria'] = df['Total_Categoria'].apply(lambda x: tratar_valor(x, tipo="numero"))
    df['Ano'] = df['Ano'].apply(lambda x: tratar_valor(x, tipo="numero"))

    # Salvar o arquivo CSV tratado
    df.to_csv(caminho_arquivo_tratado, index=False, encoding='utf-8')

# Chamar a função com os caminhos de entrada e saída
tratar_csv(
    'C:\\Users\\Raphael\\Desktop\\Empraba_API\\dir_csv\\dados_vinhos_comercio.csv',
    'C:\\Users\\Raphael\\Desktop\\Empraba_API\\dir_csv\\dados_vinhos_comercio_tratado.csv'
)

print("Tratamento do arquivo CSV concluído!")
