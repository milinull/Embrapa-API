from rest_framework import serializers
from embrapa.models import *

class ProducaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Producao.

    Serializa todos os campos do modelo Producao, permitindo a conversão
    de objetos Producao para formatos como JSON e vice-versa.
    """
    class Meta:
        model = Producao
        fields = '__all__'

class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = '__all__'

class ProcessamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processamento
        fields = '__all__'

class ImportacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importacao
        fields = '__all__'

class ExportacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exportacao
        fields = '__all__'