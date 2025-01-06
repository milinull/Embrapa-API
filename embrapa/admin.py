from django.contrib import admin
from embrapa.models import *

@admin.register(Producao)
class ProducaoAdmin(admin.ModelAdmin):
    """Configuração da interface administrativa para o modelo Producao.

    Exibe todos os campos do modelo Producao na visualização em lista.
    """
    list_display = [field.name for field in Producao._meta.fields]

@admin.register(Comercio)
class ComercioAdmin(admin.ModelAdmin):
    """Configuração da interface administrativa para o modelo Comercio.

    Exibe todos os campos do modelo Comercio na visualização em lista.
    """
    list_display = [field.name for field in Comercio._meta.fields]

@admin.register(Processamento)
class ProcessamentoAdmin(admin.ModelAdmin):
    """Configuração da interface administrativa para o modelo Processamento.

    Exibe todos os campos do modelo Processamento na visualização em lista.
    """
    list_display = [field.name for field in Processamento._meta.fields]

@admin.register(Importacao)
class ImportacaoAdmin(admin.ModelAdmin):
    """Configuração da interface administrativa para o modelo Importacao.

    Exibe todos os campos do modelo Importacao na visualização em lista.
    """
    list_display = [field.name for field in Importacao._meta.fields]

@admin.register(Exportacao)
class ExportacaoAdmin(admin.ModelAdmin):
    """Configuração da interface administrativa para o modelo Exportacao.

    Exibe todos os campos do modelo Exportacao na visualização em lista.
    """
    list_display = [field.name for field in Exportacao._meta.fields]
