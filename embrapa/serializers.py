from rest_framework_mongoengine import serializers
from .models import *


class ComercVinhosSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ComercVinhos
        fields = "__all__"


class ExportVinhosSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ExportVinhos
        fields = "__all__"


class ImportVinhosSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ImportVinhos
        fields = "__all__"


class ProdVinhosSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProdVinhos
        fields = "__all__"


class ProcessVinhosSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProcessVinhos
        fields = "__all__"
