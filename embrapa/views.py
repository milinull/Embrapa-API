from embrapa.models import *
from embrapa.serializers import *
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

class ProducaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo `Producao`.
    Ação padrão gerenciada pelo roteador, incluindo filtros e ordenação.

    - Filtragem por categoria, produto, ano, etc. pode ser feita usando o parâmetro de pesquisa na URL.
    - Exemplo de requisição: /producao/?search=categoria_x
    
    Filtros e ordenações:
    - Filtros podem ser aplicados aos campos `ano`, `categoria`, `produto` e `id`.
    - Ordenação pode ser feita pelos campos `ano`, `categoria`, `produto` e `id`.
    """
    queryset = Producao.objects.all().order_by("id")
    serializer_class = ProducaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ano', 'categoria', 'produto', 'id']
    search_fields = ['ano', 'categoria', 'produto', 'id']


class ComercioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo `Comercio`.
    Ação padrão gerenciada pelo roteador, incluindo filtros e ordenação.

    - Filtragem por categoria, produto, ano, etc. pode ser feita usando o parâmetro de pesquisa na URL.
    - Exemplo de requisição: /comercio/?search=categoria_x
    
    Filtros e ordenações:
    - Filtros podem ser aplicados aos campos `ano`, `categoria`, `produto` e `id`.
    - Ordenação pode ser feita pelos campos `ano`, `categoria`, `produto` e `id`.
    """
    queryset = Comercio.objects.all().order_by("id")
    serializer_class = ComercioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ano', 'categoria', 'produto', 'id']
    search_fields = ['ano', 'categoria', 'produto', 'id']


class ProcessamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo `Processamento`.
    Ação padrão gerenciada pelo roteador, incluindo filtros e ordenação.
    
    - Filtragem por categoria pode ser feita usando o parâmetro de pesquisa na URL.
    - Exemplo de requisição: /processamento/?search=categoria_x

    Filtros e ordenações:
    - Filtros podem ser aplicados aos campos `ano`, `categoria`, `cultivar`, `tipo` e `id`.
    - Ordenação pode ser feita pelos campos `ano`, `categoria`, `cultivar`, `tipo` e `id`.
    """
    queryset = Processamento.objects.all().order_by("id")
    serializer_class = ProcessamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ano', 'categoria', 'cultivar', 'tipo', 'id']
    search_fields = ['ano', 'categoria', 'cultivar', 'tipo', 'id']


class ExportacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo `Exportacao`.
    Ação padrão gerenciada pelo roteador, incluindo filtros e ordenação.
    
    - Filtragem por categoria pode ser feita usando o parâmetro de pesquisa na URL.
    - Exemplo de requisição: /exportacao/?search=categoria_x

    Filtros e ordenações:
    - Filtros podem ser aplicados aos campos `ano`, `paises`, `tipo` e `id`.
    - Ordenação pode ser feita pelos campos `ano`, `paises`, `tipo` e `id`.
    """
    queryset = Exportacao.objects.all().order_by("id")
    serializer_class = ExportacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ano', 'paises', 'tipo', 'id']
    search_fields = ['ano', 'paises', 'tipo', 'id']


class ImportacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo `Importacao`.
    Ação padrão gerenciada pelo roteador, incluindo filtros e ordenação.
    
    - Filtragem por categoria pode ser feita usando o parâmetro de pesquisa na URL.
    - Exemplo de requisição: /importacao/?search=categoria_x

    Filtros e ordenações:
    - Filtros podem ser aplicados aos campos `ano`, `paises`, `tipo` e `id`.
    - Ordenação pode ser feita pelos campos `ano`, `paises`, `tipo` e `id`.
    """
    queryset = Importacao.objects.all().order_by("id")
    serializer_class = ImportacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ano', 'paises', 'tipo', 'id']
    search_fields = ['ano', 'paises', 'tipo', 'id']
