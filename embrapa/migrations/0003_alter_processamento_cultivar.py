# Generated by Django 5.1.3 on 2024-11-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embrapa', '0002_comercio_origem_dados_exportacao_origem_dados_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processamento',
            name='cultivar',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
