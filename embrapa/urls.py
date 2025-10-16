from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"Comercio", ComercVinhosViewSet)
router.register(r"Exportacao", ExportVinhosViewSet)
router.register(r"Importacao", ImportVinhosViewSet)
router.register(r"Producao", ProdVinhosViewSet)
router.register(r"Processamento", ProcessVinhosViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("comparativo/<int:ano>/", comparativo_producao_exportacao),
]
