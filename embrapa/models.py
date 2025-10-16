from mongoengine import Document, IntField, StringField, FloatField


# Comércio de Vinhos
class ComercVinhos(Document):
    Ano = IntField(required=True)
    Produto = StringField(max_length=100, required=True)
    Quantidade_L = FloatField()
    Categoria = StringField(max_length=100)

    meta = {"collection": "comercializacao_vinhos"}

    def __str__(self):
        return f"{self.ano} ({self.produto})"


# Exportação de Vinhos
class ExportVinhos(Document):
    Ano = IntField(required=True)
    Tipo = StringField(max_length=100)
    Países = StringField(max_length=250)
    Quantidade_Kg = FloatField()
    Valor_US = FloatField()

    meta = {"collection": "exportacao_vinhos"}

    def __str__(self):
        return f"{self.ano} ({self.paises})"


# Importação de Vinhos
class ImportVinhos(Document):
    Ano = IntField(required=True)
    Tipo = StringField(max_length=100)
    Países = StringField(max_length=250)
    Quantidade_Kg = FloatField()
    Valor_US = FloatField()

    meta = {"collection": "importacao_vinhos"}

    def __str__(self):
        return f"{self.ano} ({self.paises})"


# Produção de Vinhos
class ProdVinhos(Document):
    Ano = IntField(required=True)
    Produto = StringField(max_length=100, required=True)
    Quantidade_L = FloatField()
    Categoria = StringField(max_length=100)

    meta = {"collection": "producao_vinhos"}

    def __str__(self):
        return f"{self.ano} ({self.produto})"


# Processamento de Vinhos
class ProcessVinhos(Document):
    Ano = IntField(required=True)
    Tipo = StringField(max_length=100)
    Cultivar = StringField(max_length=100)
    Quantidade_Kg = FloatField()
    Categoria = StringField(max_length=100)

    meta = {"collection": "uvas_processadas"}

    def __str__(self):
        return f"{self.ano} ({self.cultivar})"
