from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import (
    ComercVinhos, ExportVinhos, ImportVinhos, 
    ProdVinhos, ProcessVinhos
)


class ComercVinhosViewSetTest(APITestCase):
    """Testes para o ViewSet de Comercialização de Vinhos"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('comercvinhos-list')
        
        # Criar dados de teste
        self.dados_teste = [
            ComercVinhos(
                Ano=2023,
                Categoria="Vinho de Mesa",
                Produto="Tinto",
                Quantidade_L=1000.50
            ),
            ComercVinhos(
                Ano=2023,
                Categoria="Vinho Fino",
                Produto="Branco",
                Quantidade_L=500.75
            ),
            ComercVinhos(
                Ano=2024,
                Categoria="Vinho de Mesa",
                Produto="Rosé",
                Quantidade_L=750.25
            )
        ]
        
        for dado in self.dados_teste:
            dado.save()
    
    def tearDown(self):
        ComercVinhos.objects.all().delete()
    
    def test_listar_comercio_vinhos(self):
        """Testa se consegue listar todos os registros de comércio"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_filtrar_por_ano(self):
        """Testa filtro por ano"""
        response = self.client.get(self.url, {'ano': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
    
    def test_filtrar_por_categoria(self):
        """Testa filtro por categoria"""
        response = self.client.get(self.url, {'categoria': 'Vinho de Mesa'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Vinho de Mesa', item['Categoria'])
    
    def test_filtrar_por_produto(self):
        """Testa filtro por produto"""
        response = self.client.get(self.url, {'produto': 'Tinto'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Tinto', item['Produto'])
    
    def test_filtros_combinados(self):
        """Testa múltiplos filtros simultaneamente"""
        response = self.client.get(self.url, {
            'ano': 2023,
            'categoria': 'Vinho de Mesa'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
            self.assertIn('Vinho de Mesa', item['Categoria'])
    
    def test_total_por_ano(self):
        """Testa a action customizada total_por_ano"""
        url = reverse('comercvinhos-total-por-ano')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        # Verifica estrutura dos dados
        if len(response.data) > 0:
            self.assertIn('_id', response.data[0])
            self.assertIn('total_litros', response.data[0])


class ExportVinhosViewSetTest(APITestCase):
    """Testes para o ViewSet de Exportação de Vinhos"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('exportvinhos-list')
        
        # Criar dados de teste
        self.dados_teste = [
            ExportVinhos(
                Ano=2023,
                Tipo="Vinho de Mesa",
                Países="Estados Unidos",
                Quantidade_Kg=5000.0,
                Valor_US=25000.0
            ),
            ExportVinhos(
                Ano=2023,
                Tipo="Vinho Fino",
                Países="Alemanha",
                Quantidade_Kg=3000.0,
                Valor_US=18000.0
            ),
            ExportVinhos(
                Ano=2024,
                Tipo="Espumante",
                Países="França",
                Quantidade_Kg=2000.0,
                Valor_US=15000.0
            )
        ]
        
        for dado in self.dados_teste:
            dado.save()
    
    def tearDown(self):
        ExportVinhos.objects.all().delete()
    
    def test_listar_exportacao_vinhos(self):
        """Testa se consegue listar todos os registros de exportação"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_filtrar_por_ano(self):
        """Testa filtro por ano"""
        response = self.client.get(self.url, {'ano': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
    
    def test_filtrar_por_pais(self):
        """Testa filtro por país"""
        response = self.client.get(self.url, {'pais': 'Estados Unidos'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Estados Unidos', item['Países'])
    
    def test_filtrar_por_tipo(self):
        """Testa filtro por tipo"""
        response = self.client.get(self.url, {'tipo': 'Vinho Fino'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Vinho Fino', item['Tipo'])
    
    def test_top_paises(self):
        """Testa a action customizada top_paises"""
        url = reverse('exportvinhos-top-paises')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertLessEqual(len(response.data), 5)  # Limite padrão
        
        # Verifica estrutura dos dados
        if len(response.data) > 0:
            self.assertIn('_id', response.data[0])
            self.assertIn('total_kg', response.data[0])
    
    def test_top_paises_com_limite(self):
        """Testa top_paises com limite customizado"""
        url = reverse('exportvinhos-top-paises')
        response = self.client.get(url, {'limit': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 2)


class ImportVinhosViewSetTest(APITestCase):
    """Testes para o ViewSet de Importação de Vinhos"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('importvinhos-list')
        
        # Criar dados de teste
        self.dados_teste = [
            ImportVinhos(
                Ano=2023,
                Tipo="Vinho de Mesa",
                Países="Argentina",
                Quantidade_Kg=8000.0,
                Valor_US=40000.0
            ),
            ImportVinhos(
                Ano=2023,
                Tipo="Vinho Fino",
                Países="Chile",
                Quantidade_Kg=6000.0,
                Valor_US=35000.0
            ),
            ImportVinhos(
                Ano=2024,
                Tipo="Espumante",
                Países="Itália",
                Quantidade_Kg=4000.0,
                Valor_US=28000.0
            )
        ]
        
        for dado in self.dados_teste:
            dado.save()
    
    def tearDown(self):
        ImportVinhos.objects.all().delete()
    
    def test_listar_importacao_vinhos(self):
        """Testa se consegue listar todos os registros de importação"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_filtrar_por_ano(self):
        """Testa filtro por ano"""
        response = self.client.get(self.url, {'ano': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
    
    def test_filtrar_por_pais(self):
        """Testa filtro por país"""
        response = self.client.get(self.url, {'pais': 'Argentina'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Argentina', item['Países'])
    
    def test_filtrar_por_tipo(self):
        """Testa filtro por tipo"""
        response = self.client.get(self.url, {'tipo': 'Espumante'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Espumante', item['Tipo'])


class ProdVinhosViewSetTest(APITestCase):
    """Testes para o ViewSet de Produção de Vinhos"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('prodvinhos-list')
        
        # Criar dados de teste
        self.dados_teste = [
            ProdVinhos(
                Ano=2023,
                Categoria="Vinho de Mesa",
                Produto="Tinto",
                Quantidade_L=15000.0
            ),
            ProdVinhos(
                Ano=2023,
                Categoria="Vinho Fino",
                Produto="Branco",
                Quantidade_L=10000.0
            ),
            ProdVinhos(
                Ano=2024,
                Categoria="Espumante",
                Produto="Brut",
                Quantidade_L=8000.0
            )
        ]
        
        for dado in self.dados_teste:
            dado.save()
    
    def tearDown(self):
        ProdVinhos.objects.all().delete()
    
    def test_listar_producao_vinhos(self):
        """Testa se consegue listar todos os registros de produção"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_filtrar_por_ano(self):
        """Testa filtro por ano"""
        response = self.client.get(self.url, {'ano': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
    
    def test_filtrar_por_categoria(self):
        """Testa filtro por categoria"""
        response = self.client.get(self.url, {'categoria': 'Vinho de Mesa'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Vinho de Mesa', item['Categoria'])
    
    def test_filtrar_por_produto(self):
        """Testa filtro por produto"""
        response = self.client.get(self.url, {'produto': 'Tinto'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Tinto', item['Produto'])
    
    def test_total_por_ano(self):
        """Testa a action customizada total_por_ano"""
        url = reverse('prodvinhos-total-por-ano')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        # Verifica estrutura dos dados
        if len(response.data) > 0:
            self.assertIn('_id', response.data[0])
            self.assertIn('total_litros', response.data[0])


class ProcessVinhosViewSetTest(APITestCase):
    """Testes para o ViewSet de Processamento de Uvas"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('processvinhos-list')
        
        # Criar dados de teste
        self.dados_teste = [
            ProcessVinhos(
                Ano=2023,
                Tipo="Viníferas",
                Cultivar="Cabernet Sauvignon",
                Quantidade_Kg=12000.0
            ),
            ProcessVinhos(
                Ano=2023,
                Tipo="Americanas",
                Cultivar="Isabel",
                Quantidade_Kg=8000.0
            ),
            ProcessVinhos(
                Ano=2024,
                Tipo="Viníferas",
                Cultivar="Merlot",
                Quantidade_Kg=10000.0
            )
        ]
        
        for dado in self.dados_teste:
            dado.save()
    
    def tearDown(self):
        ProcessVinhos.objects.all().delete()
    
    def test_listar_processamento_vinhos(self):
        """Testa se consegue listar todos os registros de processamento"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_filtrar_por_ano(self):
        """Testa filtro por ano"""
        response = self.client.get(self.url, {'ano': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['Ano'], 2023)
    
    def test_filtrar_por_tipo(self):
        """Testa filtro por tipo"""
        response = self.client.get(self.url, {'tipo': 'Viníferas'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Viníferas', item['Tipo'])
    
    def test_filtrar_por_cultivar(self):
        """Testa filtro por cultivar"""
        response = self.client.get(self.url, {'cultivar': 'Isabel'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn('Isabel', item['Cultivar'])


class ComparativoProducaoExportacaoTest(APITestCase):
    """Testes para o endpoint de comparativo produção x exportação"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar dados de teste para produção
        ProdVinhos(
            Ano=2023,
            Categoria="Vinho de Mesa",
            Produto="Tinto",
            Quantidade_L=10000.0
        ).save()
        
        ProdVinhos(
            Ano=2023,
            Categoria="Vinho Fino",
            Produto="Branco",
            Quantidade_L=5000.0
        ).save()
        
        # Criar dados de teste para exportação
        ExportVinhos(
            Ano=2023,
            Tipo="Vinho de Mesa",
            Países="Estados Unidos",
            Quantidade_Kg=3000.0,
            Valor_US=15000.0
        ).save()
        
        ExportVinhos(
            Ano=2023,
            Tipo="Vinho Fino",
            Países="Alemanha",
            Quantidade_Kg=2000.0,
            Valor_US=12000.0
        ).save()
    
    def tearDown(self):
        ProdVinhos.objects.all().delete()
        ExportVinhos.objects.all().delete()
    
    def test_comparativo_com_dados(self):
        """Testa comparativo com dados existentes"""
        url = '/api/comparativo/2023/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ano', response.data)
        self.assertIn('producao_total_L', response.data)
        self.assertIn('exportacao_total_Kg', response.data)
        self.assertIn('percentual_exportado', response.data)
        
        self.assertEqual(response.data['ano'], 2023)
        self.assertGreater(response.data['producao_total_L'], 0)
        self.assertGreater(response.data['exportacao_total_Kg'], 0)
    
    def test_comparativo_sem_dados(self):
        """Testa comparativo com ano sem dados"""
        url = '/api/comparativo/1900/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('erro', response.data)
    
    def test_comparativo_ano_invalido(self):
        """Testa comparativo com ano inválido (não numérico)"""
        # Como a URL espera int, o Django vai retornar 404 automaticamente
        url = '/api/comparativo/abc/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_calculo_percentual(self):
        """Testa se o cálculo do percentual está correto"""
        url = '/api/comparativo/2023/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        producao = response.data['producao_total_L']
        exportacao = response.data['exportacao_total_Kg']
        percentual = response.data['percentual_exportado']
        
        # Verifica se o cálculo está correto
        percentual_esperado = round((exportacao / producao * 100), 2)
        self.assertEqual(percentual, percentual_esperado)


class OrdenacaoTest(APITestCase):
    """Testes para verificar ordenação dos resultados"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar dados com anos diferentes para testar ordenação
        ComercVinhos(Ano=2021, Categoria="A", Produto="P1", Quantidade_L=100).save()
        ComercVinhos(Ano=2023, Categoria="B", Produto="P2", Quantidade_L=200).save()
        ComercVinhos(Ano=2022, Categoria="C", Produto="P3", Quantidade_L=300).save()
    
    def tearDown(self):
        ComercVinhos.objects.all().delete()
    
    def test_ordenacao_por_ano_decrescente(self):
        """Testa se os resultados estão ordenados por ano decrescente"""
        url = reverse('comercvinhos-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        anos = [item['Ano'] for item in response.data['results']]
        anos_ordenados = sorted(anos, reverse=True)
        
        # Verifica se está ordenado por ano decrescente
        self.assertEqual(anos, anos_ordenados)


class PaginacaoTest(APITestCase):
    """Testes para verificar paginação"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar muitos registros para testar paginação
        for i in range(25):
            ComercVinhos(
                Ano=2023,
                Categoria=f"Categoria {i}",
                Produto=f"Produto {i}",
                Quantidade_L=100.0 * i
            ).save()
    
    def tearDown(self):
        ComercVinhos.objects.all().delete()
    
    def test_paginacao_existe(self):
        """Testa se a paginação está funcionando"""
        url = reverse('comercvinhos-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        
        # Verifica se tem link para próxima página
        if response.data['count'] > len(response.data['results']):
            self.assertIsNotNone(response.data.get('next'))
    
    def test_navegacao_paginacao(self):
        """Testa navegação entre páginas"""
        url = reverse('comercvinhos-list')
        response = self.client.get(url)
        
        if response.data.get('next'):
            # Testa se consegue acessar próxima página
            next_response = self.client.get(response.data['next'])
            self.assertEqual(next_response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(next_response.data['results'], list)