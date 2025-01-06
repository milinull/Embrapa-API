from django.db import models

class Producao(models.Model):
    """
    Representa os dados de produção de um produto em uma categoria específica.

    Campos:
        categoria (CharField): Categoria do produto (ex.: vinho, suco).
        produto (CharField): Nome do produto produzido.
        quantidade_litros (FloatField): Quantidade produzida em litros.
        total_categoria (FloatField): Soma total da produção da categoria.
        ano (IntegerField): Ano da produção.
    """
    categoria = models.CharField(max_length=50)
    produto = models.CharField(max_length=50)
    quantidade_litros = models.FloatField()
    total_categoria = models.FloatField()
    ano = models.IntegerField()

    def __str__(self):
        """
        Retorna uma representação legível do objeto Producao.

        Exemplo:
            "Vinhos - Tinto (2023) - 5000L"
        """
        return f"{self.categoria} - {self.produto} ({self.ano}) - {self.quantidade_litros}L"

class Comercio(models.Model):
    """
    Representa os dados comerciais de um produto.

    Campos:
        categoria (CharField): Categoria do produto (ex.: vinho, suco).
        produto (CharField): Nome do produto comercializado.
        quantidade_litros (FloatField): Quantidade comercializada em litros.
        total_categoria (FloatField): Soma total da comercialização da categoria.
        ano (IntegerField): Ano da comercialização.
    """
    categoria = models.CharField(max_length=50)
    produto = models.CharField(max_length=50)
    quantidade_litros = models.FloatField()
    total_categoria = models.FloatField()
    ano = models.IntegerField()

    def __str__(self):
        """
        Retorna uma representação legível do objeto Comercio.

        Exemplo:
            "Vinhos - Tinto (2023) - 10000L"
        """
        return f"{self.categoria} - {self.produto} ({self.ano}) - {self.quantidade_litros}L"

class Processamento(models.Model):
    """
    Representa os dados de processamento de produtos agrícolas.

    Campos:
        categoria (CharField): Categoria do produto processado.
        cultivar (CharField): Nome da cultivar processada (opcional).
        quantidade_kgs (FloatField): Quantidade processada em quilogramas.
        total_categoria (FloatField): Soma total do processamento da categoria.
        ano (IntegerField): Ano do processamento.
        tipo (CharField): Tipo de processamento (ex.: fermentação, desidratação).
    """
    categoria = models.CharField(max_length=50)
    cultivar = models.CharField(max_length=50, null=True, blank=True)
    quantidade_kgs = models.FloatField()
    total_categoria = models.FloatField()
    ano = models.IntegerField()
    tipo = models.CharField(max_length=100, default="Indefinido")

    def __str__(self):
        """
        Retorna uma representação legível do objeto Processamento.

        Exemplo:
            "Uvas - Cabernet Sauvignon (2023) - 2000kg"
        """
        return f"{self.categoria} - {self.cultivar if self.cultivar else 'Desconhecido'} ({self.ano}) - {self.quantidade_kgs}kg"

class Importacao(models.Model):
    """
    Representa os dados de importação de produtos.

    Campos:
        paises (CharField): Países de origem dos produtos importados.
        quantidade_kgs (FloatField): Quantidade importada em quilogramas.
        valor (FloatField): Valor total da importação.
        ano (IntegerField): Ano da importação.
        tipo (CharField): Tipo de produto importado.
    """
    paises = models.CharField(max_length=50)
    quantidade_kgs = models.FloatField()
    valor = models.FloatField()
    ano = models.IntegerField()
    tipo = models.CharField(max_length=100, default="Indefinido")

    def __str__(self):
        """
        Retorna uma representação legível do objeto Importacao.

        Exemplo:
            "França - 50000.0 (2023) - 2000kg"
        """
        return f"{self.paises} - {self.valor} ({self.ano}) - {self.quantidade_kgs}kg"

class Exportacao(models.Model):
    """
    Representa os dados de exportação de produtos.

    Campos:
        paises (CharField): Países de destino dos produtos exportados.
        quantidade_kgs (FloatField): Quantidade exportada em quilogramas.
        valor (FloatField): Valor total da exportação.
        ano (IntegerField): Ano da exportação.
        tipo (CharField): Tipo de produto exportado.
    """
    paises = models.CharField(max_length=50)
    quantidade_kgs = models.FloatField()
    valor = models.FloatField()
    ano = models.IntegerField()
    tipo = models.CharField(max_length=100, default="Indefinido")

    def __str__(self):
        """
        Retorna uma representação legível do objeto Exportacao.

        Exemplo:
            "EUA - 80000.0 (2023) - 3000kg"
        """
        return f"{self.paises} - {self.valor} ({self.ano}) - {self.quantidade_kgs}kg"
