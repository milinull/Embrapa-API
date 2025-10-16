from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Embrapa Wine Data API",
        default_version="v1",
        description="""
    API RESTful para análise de dados da indústria vitivinícola brasileira.

    **Recursos disponíveis:**
    - 📊 Produção de vinhos e derivados
    - 💰 Comercialização no mercado interno
    - 🍇 Processamento de uvas
    - 📦 Importação e Exportação

    **Fonte:** Embrapa Uva e Vinho

    **Filtros:** Use `?ano=2024` para filtrar por ano específico.
        """,
        terms_of_service="https://github.com/milinull/Embrapa-API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("embrapa.urls")),
    # Swagger / ReDoc
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
