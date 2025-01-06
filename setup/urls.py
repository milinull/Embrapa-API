from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from embrapa.views import *
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração da documentação interativa da API usando o drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Projeto Embrapa API",
        default_version='v1',
        description=(
            "### **Descrição da API**\n"
            "**Embrapa API** criada com Django Rest Framework, oferece acesso seguro e eficiente ao banco de dados da Embrapa, fornecendo informações sobre uvas, vinhos e derivados para integração em diversos projetos.\n\n"
            "### **Funcionalidades**\n"
            "- **Consulta de Dados**:\n"
            "  - Acesse informações detalhadas sobre produção, comércio, exportação, importação e processamento de uvas e vinhos.\n"
            "- **Filtros Personalizados**:\n"
            "  - Realize buscas específicas com suporte a filtros avançados, como ano, categoria, produto, países e tipo.\n"
            "- **Paginação de Resultados**:\n"
            "  - Navegue facilmente por grandes volumes de dados com suporte a paginação.\n"
            "- **Autenticação JWT**:\n"
            "  - Garanta a segurança das operações com autenticação baseada em tokens JWT.\n"
            "### **Informações Adicionais**\n"
            "- **Licença**: Esta API é distribuída sob a licença **BSD**, promovendo o uso livre e colaborativo.\n"
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Criação do roteador padrão do Django REST Framework para as views
router = routers.DefaultRouter()
router.register('producao', ProducaoViewSet, basename='Producao')
router.register('comercio', ComercioViewSet, basename='Comercio')
router.register('processamento', ProcessamentoViewSet, basename='Processamento')
router.register('importacao', ImportacaoViewSet, basename='Importacao')
router.register('exportacao', ExportacaoViewSet, basename='Exportacao')

# Definição das URLs e rotas da aplicação
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),  # Acesso ao painel de administração do Django

    # Endpoints da API utilizando o roteador DefaultRouter
    path('', include(router.urls)),  # Inclui os endpoints registrados no roteador

    # Rotas para autenticação JWT (JSON Web Token)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint para obter o token de acesso
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint para renovar o token de acesso

    # Endpoints para acessar a documentação da API com Swagger e ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # UI Swagger
]