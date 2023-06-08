from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Cliente
from .models import Fechamento
from .models import Trabalho


@registry.register_document
class FechamentoDocument(Document):
    class Index:
        name = 'fechamentos'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Fechamento
        fields = [
            'nota_de_servico',
            'vencimento',
            'data_pagamento',
        ]


@registry.register_document
class TrabalhoDocument(Document):
    class Index:
        name = 'trabalhos'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Trabalho
        fields = [
            'cliente',
            'paciente',
            'servico',
            'quantidade',
            'elemento',
            'entrada',
            'observacoes',
            'saida_1a_prova',
            'retorno_1a_prova',
            'saida_2a_prova',
            'retorno_2a_prova',
            'saida_3a_prova',
            'retorno_3a_prova',
            'entrega',
            'valor_unitario',
            'fechamento',
        ]
        related_models = [Cliente, Fechamento]
