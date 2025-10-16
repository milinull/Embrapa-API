from rest_framework_mongoengine import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ComercVinhos, ExportVinhos, ImportVinhos, ProdVinhos, ProcessVinhos
from .serializers import (
    ComercVinhosSerializer,
    ExportVinhosSerializer,
    ImportVinhosSerializer,
    ProdVinhosSerializer,
    ProcessVinhosSerializer,
)


# COMÉRCIO DE VINHOS
class ComercVinhosViewSet(viewsets.ModelViewSet):
    queryset = ComercVinhos.objects().order_by("-Ano", "Categoria", "Produto")
    serializer_class = ComercVinhosSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ComercVinhos.objects().order_by("-Ano", "Categoria", "Produto")
        ano = self.request.query_params.get("ano")
        categoria = self.request.query_params.get("categoria")
        produto = self.request.query_params.get("produto")

        if ano:
            queryset = queryset.filter(Ano=int(ano))
        if categoria:
            queryset = queryset.filter(Categoria__icontains=categoria)
        if produto:
            queryset = queryset.filter(Produto__icontains=produto)
        return queryset

    @action(detail=False, methods=["get"])
    def total_por_ano(self, request):
        pipeline = [
            {"$group": {"_id": "$Ano", "total_litros": {"$sum": "$Quantidade_L"}}},
            {"$sort": {"_id": 1}},
        ]
        dados = list(ComercVinhos.objects.aggregate(*pipeline))
        return Response(dados)


# EXPORTAÇÃO DE VINHOS
class ExportVinhosViewSet(viewsets.ModelViewSet):
    queryset = ExportVinhos.objects().order_by("-Ano", "Tipo")
    serializer_class = ExportVinhosSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ExportVinhos.objects().order_by("-Ano", "Tipo")
        ano = self.request.query_params.get("ano")
        pais = self.request.query_params.get("pais")
        tipo = self.request.query_params.get("tipo")

        if ano:
            queryset = queryset.filter(Ano=int(ano))
        if pais:
            queryset = queryset.filter(Países__icontains=pais)
        if tipo:
            queryset = queryset.filter(Tipo__icontains=tipo)
        return queryset

    @action(detail=False, methods=["get"])
    def top_paises(self, request):
        limit = int(request.query_params.get("limit", 5))
        pipeline = [
            {"$group": {"_id": "$Países", "total_kg": {"$sum": "$Quantidade_Kg"}}},
            {"$sort": {"total_kg": -1}},
            {"$limit": limit},
        ]
        dados = list(ExportVinhos.objects.aggregate(*pipeline))
        return Response(dados)


# IMPORTAÇÃO DE VINHOS
class ImportVinhosViewSet(viewsets.ModelViewSet):
    queryset = ImportVinhos.objects().order_by("-Ano", "Tipo")
    serializer_class = ImportVinhosSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ImportVinhos.objects().order_by("-Ano", "Tipo")
        ano = self.request.query_params.get("ano")
        pais = self.request.query_params.get("pais")
        tipo = self.request.query_params.get("tipo")

        if ano:
            queryset = queryset.filter(Ano=int(ano))
        if pais:
            queryset = queryset.filter(Países__icontains=pais)
        if tipo:
            queryset = queryset.filter(Tipo__icontains=tipo)
        return queryset


# PRODUÇÃO DE VINHOS
class ProdVinhosViewSet(viewsets.ModelViewSet):
    queryset = ProdVinhos.objects().order_by("-Ano", "Categoria", "Produto")
    serializer_class = ProdVinhosSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ProdVinhos.objects().order_by("-Ano", "Categoria", "Produto")
        ano = self.request.query_params.get("ano")
        categoria = self.request.query_params.get("categoria")
        produto = self.request.query_params.get("produto")

        if ano:
            queryset = queryset.filter(Ano=int(ano))
        if categoria:
            queryset = queryset.filter(Categoria__icontains=categoria)
        if produto:
            queryset = queryset.filter(Produto__icontains=produto)
        return queryset

    @action(detail=False, methods=["get"])
    def total_por_ano(self, request):
        pipeline = [
            {"$group": {"_id": "$Ano", "total_litros": {"$sum": "$Quantidade_L"}}},
            {"$sort": {"_id": 1}},
        ]
        dados = list(ProdVinhos.objects.aggregate(*pipeline))
        return Response(dados)


# PROCESSAMENTO DE UVAS
class ProcessVinhosViewSet(viewsets.ModelViewSet):
    queryset = ProcessVinhos.objects().order_by("-Ano", "Tipo", "Cultivar")
    serializer_class = ProcessVinhosSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ProcessVinhos.objects().order_by("-Ano", "Tipo", "Cultivar")
        ano = self.request.query_params.get("ano")
        cultivar = self.request.query_params.get("cultivar")
        tipo = self.request.query_params.get("tipo")

        if ano:
            queryset = queryset.filter(Ano=int(ano))
        if cultivar:
            queryset = queryset.filter(Cultivar__icontains=cultivar)
        if tipo:
            queryset = queryset.filter(Tipo__icontains=tipo)
        return queryset


# COMPARATIVO ENTRE PRODUÇÃO E EXPORTAÇÃO
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def comparativo_producao_exportacao(request, ano):
    try:
        ano = int(ano)
    except ValueError:
        return Response({"erro": "Ano inválido."}, status=status.HTTP_400_BAD_REQUEST)

    prod_total = ProdVinhos.objects(Ano=ano).sum("Quantidade_L") or 0
    export_total = ExportVinhos.objects(Ano=ano).sum("Quantidade_Kg") or 0

    if prod_total == 0:
        return Response(
            {"erro": f"Sem dados de produção para o ano {ano}."}, status=404
        )

    percentual = (export_total / prod_total * 100) if prod_total else 0
    return Response(
        {
            "ano": ano,
            "producao_total_L": prod_total,
            "exportacao_total_Kg": export_total,
            "percentual_exportado": round(percentual, 2),
        }
    )
