from rest_framework_mongoengine import viewsets
from rest_framework.filters import OrderingFilter
from .models import *
from .serializers import *

class ComercVinhosViewSet(viewsets.ModelViewSet):
    queryset = ComercVinhos.objects().order_by("-Ano", "Categoria", "Produto")
    serializer_class = ComercVinhosSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['Ano', 'Categoria', 'Produto']
    ordering = ['-Ano', 'Categoria', 'Produto']

class ExportVinhosViewSet(viewsets.ModelViewSet):
    queryset = ExportVinhos.objects().order_by("-Ano", "Tipo")
    serializer_class = ExportVinhosSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['Ano', 'Tipo']
    ordering = ['-Ano', 'Tipo']

class ImportVinhosViewSet(viewsets.ModelViewSet):
    queryset = ImportVinhos.objects().order_by("-Ano", "Tipo")
    serializer_class = ImportVinhosSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['Ano', 'Tipo']
    ordering = ['-Ano', 'Tipo']

class ProdVinhosViewSet(viewsets.ModelViewSet):
    queryset = ProdVinhos.objects().order_by("-Ano", "Categoria", "Produto")
    serializer_class = ProdVinhosSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['Ano', 'Categoria', 'Produto']
    ordering = ['-Ano', 'Categoria', 'Produto']

class ProcessVinhosViewSet(viewsets.ModelViewSet):
    queryset = ProcessVinhos.objects().order_by("-Ano", "Tipo", "Cultivar")
    serializer_class = ProcessVinhosSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['Ano', 'Tipo', 'Cultivar']
    ordering = ['-Ano', 'Tipo', 'Cultivar']