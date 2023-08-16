from operator import mod
from re import T
from tabnanny import verbose
from django.db import models


# Create your models here.
class Servico(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)
    valor_unitario = models.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f'{self.id} - {self.nome} - {self.valor_unitario}'


class Trabalho(models.Model):
    cliente = models.ForeignKey('Clinica_Dentista', on_delete=models.PROTECT)
    paciente = models.CharField(max_length=200)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    elemento = models.CharField(max_length=50)
    cor = models.CharField(max_length=50)
    entrada = models.DateField()
    observacoes = models.TextField(null=True, blank=True)
    saida_1a_prova = models.DateField(null=True, blank=True)
    retorno_1a_prova = models.DateField(null=True, blank=True)
    saida_2a_prova = models.DateField(null=True, blank=True)
    retorno_2a_prova = models.DateField(null=True, blank=True)
    saida_3a_prova = models.DateField(null=True, blank=True)
    retorno_3a_prova = models.DateField(null=True, blank=True)
    entrega = models.DateField(null=True, blank=True)

    desconto = models.DecimalField(decimal_places=2, default=0, max_digits=20)
    taxa_urgencia = models.DecimalField(decimal_places=2, default=0, max_digits=20)

    fechamento = models.ForeignKey(
        'Fechamento', null=True, blank=True, on_delete=models.SET_NULL
    )

    def get_valor_parcial(self):
        return self.servico.valor_unitario * self.quantidade

    def get_valor_total(self):
        valor_parcial = self.get_valor_parcial() + self.taxa_urgencia - self.desconto
        return max([valor_parcial, 0])

    def __str__(self):
        return f'{self.cliente} - {self.paciente} - {self.servico}'


class Fechamento(models.Model):
    nota_de_servico = models.IntegerField(primary_key=True)

    vencimento = models.DateField(blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True)

    def get_soma(self):
        return sum(
            t.get_valor_total() for t in Trabalho.objects.filter(fechamento=self)
        )

    def __str__(self):
        return f"Nt Svc {self.nota_de_servico} - R${self.get_soma()}"


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cro = models.CharField(max_length=50, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)
    telefones = models.CharField(max_length=50)

    clinicas = models.ManyToManyField('Clinica', through='Clinica_Dentista')

    def __str__(self):
        return self.nome

    def get_clinicas(self):
        return [c for c in Clinica.objects.filter(cliente=self)]


class Clinica_Dentista(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    clinica = models.ForeignKey('Clinica', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Relação Dentista-Clínica'
        verbose_name_plural = 'Relações Dentista-Clínica'
        unique_together = [['cliente', 'clinica']]

    def __str__(self):
        return f'{self.clinica.nome} - {self.cliente.nome}'


class Clinica(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=50)
    insc_estadual = models.CharField(max_length=50, null=True, blank=True)
    insc_municipal = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.CharField(max_length=200)
    telefones = models.CharField(max_length=50)
    contato = models.ForeignKey(
        'Cliente',
        on_delete=models.PROTECT,
        related_name='contato_da_clinica',
        null=True,
        blank=True,
    )
    email = models.EmailField(max_length=50, null=True, blank=True)

    clientes = models.ManyToManyField('Cliente', through='Clinica_Dentista')

    def get_clientes(self):
        return [c for c in Cliente.objects.filter(clinica=self)]

    def __str__(self):
        return f"{self.nome} - ({', '.join(str(c) for c in self.get_clientes())})"
