# Generated by Django 5.1.3 on 2024-11-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embrapa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comercio',
            name='origem_dados',
            field=models.CharField(default='Indefinido', max_length=100),
        ),
        migrations.AddField(
            model_name='exportacao',
            name='origem_dados',
            field=models.CharField(default='Indefinido', max_length=100),
        ),
        migrations.AddField(
            model_name='importacao',
            name='origem_dados',
            field=models.CharField(default='Indefinido', max_length=100),
        ),
        migrations.AddField(
            model_name='processamento',
            name='origem_dados',
            field=models.CharField(default='Indefinido', max_length=100),
        ),
        migrations.AddField(
            model_name='producao',
            name='origem_dados',
            field=models.CharField(default='Indefinido', max_length=100),
        ),
    ]
