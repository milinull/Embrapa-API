import os
import sys
import django
import csv

# Adicione o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar o Django para usar o arquivo de configurações do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

# Importar o modelo após configurar o Django
from embrapa.models import *

def obter_valores_unicos():
    """
    Obtém valores únicos das colunas das tabelas Comercio, Processamento, Exportacao e Importacao.
    """
    dados = {}

    # Tabela Comercio
    categorias_unicas = Comercio.objects.values_list("categoria", flat=True).distinct()
    produtos_unicos = Comercio.objects.values_list("produto", flat=True).distinct()
    dados['Comercio'] = {
        "categorias": sorted(list(categorias_unicas)),
        "produtos": sorted(list(produtos_unicos)),
    }

    # Tabela Processamento
    tipos_unicos = Processamento.objects.values_list("tipo", flat=True).distinct()
    categorias_processamento = Processamento.objects.values_list("categoria", flat=True).distinct()
    cultivars_unicas = Processamento.objects.values_list("cultivar", flat=True).distinct()
    dados['Processamento'] = {
        "tipos": sorted(list(tipos_unicos)),
        "categorias": sorted(list(categorias_processamento)),
        "cultivars": sorted(list(cultivars_unicas)),
    }

    # Tabela Exportacao
    tipos_exportacao = Exportacao.objects.values_list("tipo", flat=True).distinct()
    paises_exportacao = Exportacao.objects.values_list("paises", flat=True).distinct()
    dados['Exportacao'] = {
        "tipos": sorted(list(tipos_exportacao)),
        "paises": sorted(list(paises_exportacao)),
    }

    # Tabela Importacao
    tipos_importacao = Importacao.objects.values_list("tipo", flat=True).distinct()
    paises_importacao = Importacao.objects.values_list("paises", flat=True).distinct()
    dados['Importacao'] = {
        "tipos": sorted(list(tipos_importacao)),
        "paises": sorted(list(paises_importacao)),
    }

    return dados


def salvar_tabela_em_csv(dados, caminho_arquivo="dados_unicos.csv"):
    """
    Salva os dados em formato CSV com codificação UTF-8 e os coloca de forma vertical.
    """
    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Cabeçalho
        writer.writerow(["Tabela", "Coluna", "Valor"])

        # Dados - Salvando de forma vertical
        for tabela, colunas in dados.items():
            for coluna, valores in colunas.items():
                for valor in valores:
                    writer.writerow([tabela, coluna, valor])

    print(f"Os dados foram salvos no arquivo '{caminho_arquivo}'.")


if __name__ == "__main__":
    dados_unicos = obter_valores_unicos()
    salvar_tabela_em_csv(dados_unicos)
