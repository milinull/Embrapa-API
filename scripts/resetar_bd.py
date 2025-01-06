# EXECUTAR DENTRO DO SHELL
# python manage.py shell

from embrapa.models import *

# Deletar todos os dados das tabelas
Producao.objects.all().delete()
Comercio.objects.all().delete()
Processamento.objects.all().delete()
Importacao.objects.all().delete()
Exportacao.objects.all().delete()

print("Todos os dados foram apagados.")
